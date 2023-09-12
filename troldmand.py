"""
Code to run the Danish QSAR models in batch mode

This code uses Selenium to open an Edge browser window
and manually inputs and executes the models using
normal browser operations

Author: Tom Burns
Date  : September 12th, 2023
"""

import os
import numpy as np
import pandas as pd
from time import sleep
from sys import argv, exit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


__VERSION__ = (1,1,2)
file_path   = '\\'.join(os.path.realpath(__file__).split('\\')[:-1])
#file_path = '.'


class Paths(object):
    """gets the paths needed to find the elements on the webpage"""
    
    def __init__(self, default='%s\\xpaths.ini' % file_path):
        """initializes script"""
        self.ini   = default
        self.paths = {}
        self.read_file()

    def read_file(self):
        """reads the ini file"""
        _f = open(self.ini, 'r').readlines()
        for _l in _f:
            _n = _l.split('=')[0].strip().lower()
            if len(_l.split('=')) == 2:
                _m = _l.split('=')[1].strip()
            else:
                _m = '='.join(_l.split('=')[1:]).strip()
            if _n in self.paths:
                print('Warning: duplicate element name in %s:' % self.ini, _n)
                print('         path is being overridden!')
            self.paths[_n] = _m

    def get(self, item):
        """checks the paths"""
        item = item.lower()
        if item in self.paths:
            return self.paths[item]
        else:
            print('FATAL ERROR: No path specified for element named:', item)


class Options(object):
    """options to controlling the running of the code"""

    def __init__(self, args=argv):
        self.args      = args
        self.version   = __VERSION__
        self.infile    = '%s\\SMILES.txt' % file_path
        self.wizard    = '%s\\images\\wizard.txt' % file_path
        self.batch     = True
        self.ofile     = None
        self.limit     = False
        self.timeout   = 10
        self.pause     = 5
        self.url       = 'https://qsarmodels.food.dtu.dk/runmodel/index.html'
        self.models    = [_m.strip() for _m in open('%s\\models.ini' % file_path, 'r').readlines()]
        self.import_arguments()
        self.import_modelpaths()

    def import_arguments(self):
        """imports the arguments"""
        self.opts_infile  = ['-i', '-I', '--i'  , '--I', '-infile', '--infile']
        self.opts_outfile = ['-o', '-O', '--o'  , '--O', '-ofile' , '--ofile' ]
        self.help_args    = ['-h', '-H', '-help', '--h', '--H'    , '--help'  ]
        for _i, _arg in enumerate(self.args):
            if _i == 0:
                continue
            if _arg in self.help_args:
                self.show_help()
            if _arg in self.opts_infile:
                try:
                    self.infile = self.args[_i + 1]
                except IndexError:
                    print('!'*80)
                    print('Warning: Incorrect use of input argument!')
                    print('!'*80)
                    self.show_help()
            if _arg in self.opts_outfile:
                try:
                    self.ofile = self.args[_i + 1]
                except IndexError:
                    print('!'*80)
                    print('Warning: Incorrect use of output argument!')
                    print('!'*80)
                    self.show_help()
        if self.ofile is None:
            self.ofile = self.infile.split('.txt')[0] + '.csv'

    def import_modelpaths(self):
        """imports a full list of model paths"""
        try:
            _mfile = open('modelxpaths.ini', 'r').readlines()
        except FileNotFoundError:
            print('FATAL ERROR: modelxpaths.ini file not found!')
            exit()
        self.modelpaths = {}
        for _line in _mfile:
            if '=' not in _line:
                continue
            _model = _line.split('=')[0].strip()
            _xpath = _line.split('=')[1].strip()
            self.modelpaths[_model] = _xpath

    def show_help(self):
        """shows the help options"""
        print('='*80)
        print('Troldman (version %s) Help Menu' % '.'.join([str(__j) for __j in self.version]))
        print('='*80)
        print('\nTroldman: The Danish word for Wizard. This code allows the user to run')
        print('          the Danish QSAR Models in batch mode.')
        print('\n          (%s)' % self.url)
    
        print('\n\nUsage: SCRIPT(.py, .exe) [OPTIONS]')
        print('\n== Options ==')
        print('\nInfile :\t', self.opts_infile, '\tusage: -i $FILEPATH')
        print('\t\t (default: SMILES.txt)')
        print('\nOutfile:\t', self.opts_outfile, '\tusage: -o $FILEPATH')
        print('\t\t (default: $INFILE.csv)')
        print('\nHelp   :\t', self.help_args)
        print('='*80)
        exit()


def import_smiles(options):
    """imports the list of SMILES from a text file"""
    return [s.strip() for s in open(options.infile, 'r').readlines()]


def format_results(results, options):
    """formats the data for the output file"""
    out  = {'MolID': [], 'SMILES': []}
    smis = [s for s in results]
    cols = list(results[smis[0]]['Model'].unique())
    for col in cols:
        if col not in options.models:
            continue
        out['%s - Experimental' % col] = []
        #out['%s - Probability'  % col] = []
        out['%s - Prediction'   % col] = []
        #out['%s - Report'       % col] = []
    for i, smi in enumerate(smis):
        out['MolID' ].append(i+1)
        out['SMILES'].append(smi)
        for i in results[smi].index:
            mod = results[smi]['Model'       ][i]
            if mod not in options.models:
                continue
            exp = results[smi]['Experimental'][i]
            prd = results[smi]['Prediction'  ][i]
            prb = results[smi]['Probability' ][i]
            #rep = results[smi]['Report'      ][i]
            out['%s - Experimental' % mod].append(exp)
            #out['%s - Probability'  % mod].append(prd)
            out['%s - Prediction'   % mod].append(prd)
            #out['%s - Report'       % mod].append(rep)
    return pd.DataFrame.from_dict(out)


def run(options, smiles, paths):
    """run the calculations"""

    results = {}

    for smi in smiles:
        # Step 1: Connect to the website
        print('\nPython connecting to browser\n')
        browser = webdriver.Edge()
        browser.maximize_window()
        browser.get(options.url)

        print('\nAccepting terms of use\n')
        # Accept the terms of use
        accept = browser.find_element(By.CLASS_NAME, paths.get('accept'))
        accept.click()

        print('\nSelecting models\n')
        # Select the tab with the correct models
        model_tab = browser.find_element(By.XPATH, paths.get('model_tab'))
        model_tab.click()

        # Select the models to run. Prototype version of this code
        # will just run all available models since it was faster to find
        # the "select all" checkbox in the elements for the site"
        for model in options.models:
            check = browser.find_element(By.XPATH, options.modelpaths[model])
            check.click()

        print('\nInserting SMILES:', smi, '\n')

        # Select Option to Insert SMILES
        smi_tab = browser.find_element(By.XPATH, paths.get('smitab'))
        smi_tab.click()

         # Insert the smiles
        smi_box = browser.find_element(By.XPATH, paths.get('smibox'))
        smi_box.send_keys(smi)
        go      = browser.find_element(By.XPATH, paths.get('smigo'))
        go.click()

        # Execute models
        print('\tpausing for %i seconds' % options.pause)
        sleep(options.pause)
        print('\nPushing execute button\n')
        _fail = True
        while _fail:
            try:
                predict = browser.find_element(By.XPATH, paths.get('predict'))
                predict.click()
                _fail = False
                print('\tSubmission Successful!')
            except:
                print('\tFailed. Retrying in 5 seconds...')
                sleep(5)

        print('\nCalculating running...\n')
        # run the models
        timeout = options.timeout # seconds
        total   = 0
        tstep   = 5
        running = True

        while running:
            status = browser.find_element(By.XPATH, paths.get('status'))
            if 'processing' in str(status.text).lower():
                print('Calculation still running after %i seconds' % total)
                total += tstep
                sleep(tstep)
            else:
                print('Calculation finished after %i seconds' % total)
                endok = browser.find_element(By.XPATH, paths.get('endok'))
                endok.click()
                break
            if total >= timeout and options.limit:
                print("Calculation timed out after %i seconds" % timeout)
                running = False
        if total < timeout:
            print("Calculation successful")

        print('\nformatting results\n')
        # Extract the results from the table
        per   = 5
        table = browser.find_element(By.XPATH, paths.get('table'))
        data  = str(table.text)
        data  = data.split('\n')
        mres, mcur = {}, None
        for item in data[5:]:
            if item in options.models:
                mcur = item
                mres[mcur] = []
            elif mcur is None:
                continue
            else:
                mres[mcur].append(item)
        refr = {'Model': [], 'Experimental': [], 'Probability': [], 'Prediction': []}
        for model in mres:
            n = len(mres[model])
            refr['Model'].append(model)
            if n == 2:
                refr['Experimental'].append(None)
                refr['Probability'].append(mres[model][0])
                refr['Prediction'].append(mres[model][1])
            elif n == 3:
                refr['Experimental'].append(mres[model][0])
                refr['Probability'].append(mres[model][1])
                refr['Prediction'].append(mres[model][2])
        refr = pd.DataFrame.from_dict(refr)
        browser.close()
        results[smi] = refr

    return results


def welcome(options):
    """displays the welcome message"""
    print('='*100)
    print('Troldmand (v%s) - Danish QSAR Batch Bot' % '.'.join([str(vi) for vi in __VERSION__]))
    print('-'*100)
    wizz = open(options.wizard, 'r').readlines()
    for line in wizz:
        print(line.strip())
    print('-'*100)
    print('Author: Tom Burns')
    print('='*100)
    print('Options Selected:\n')
    print('Input File        :', options.infile)
    print('Output File       :', options.ofile, '\n')
    print('Models Selected   :')
    for model in options.models:
        print('\t>', model)
    smi_list = [smi.strip() for smi in open(options.infile, 'r').readlines()]
    print('\nRunning %i SMILES :' % len(smi_list))
    for smi in smi_list :
        print('\t>', smi)
    print('='*100)


def main():
    """main"""
    options = Options()
    welcome(options)
    results = run(options, import_smiles(options), Paths())
    results = format_results(results, options)
    results.to_csv(options.ofile, index=False)
    print('\n', options.ofile, 'written')


if __name__ in '__main__':
    main()
    print('\nCode terminated normally.')
    input('\nThis window can be closed.\n')
