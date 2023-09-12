# Troldmand v1.1.0 (Danish QSAR Batch Bot)

Author: Tom Burns (github.com/tomdburns)

Date  : September 11th, 2023

Troldmand is a bot written in python to automate a batch mode for the Danish QSAR models:

https://qsarmodels.food.dtu.dk/runmodel/index.html

## Running the code

To run the code, add the SMILES you wish to run to a .txt file

### To run (python):

python troldmand.py -i \path\to\your\smiles\file.txt -o \path\to\output\file.csv

#### You can see the list of options by typing:

python troldmand.py --help

### To run (exe)

.\troldmand.exe -i \path\to\your\smiles\file.txt -o \path\to\output\file.csv

#### You can see the list of options by typing:

.\troldmand.exe --help

### Alternate Use:

troldmand will default to running the SMILES.txt in the code's directory
when no input file is specified. The user can simply change the SMILES in
this SMILES.txt file and double click the exe to run the code without
needing the command line.

## Models Available

There are several models this code is compatible with run via the Danish QSAR Website:

* ER alpha binding, all (human in vitro)           
* ER alpha binding, balanced (human in vitro)      
* ER alpha activation (human in vitro)             
* ER Activation (in vitro, CERAPP data)            
* AR inhibition (human in vitro)                   
* AR binding (in vitro, CoMPARA data)              
* AR activation (in vitro, CoMPARA data)           
* AR inhibition (in vitro, CoMPARA data)           
* Thyroperoxidase (TPO) inhibition QSAR1 (in vitro)
* Thyroperoxidase (TPO) inhibition QSAR2 (in vitro)
* Sodium/iodide symporter (NIS), higher sensitivity
* Sodium/iodide symporter (NIS), higher specificity

To select the models being run, change the models specified in models.ini

## Python dependencies (When running Python version)

### The following python modules are needed to run this code:

* numpy
* pandas
* selenium

### To install python module use pip. example:

pip install numpy

## Contact Information

If you have any questions, contact Tom Burns: github.com/tomdburns
