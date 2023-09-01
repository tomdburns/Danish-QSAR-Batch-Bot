# Troldmand v1.0.0 (Danish QSAR Batch Bot)

Author: Tom Burns (github.com/tomdburns)
Date  : August 31st, 2023

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

## Python dependencies (When running Python version)

### The following python modules are needed to run this code:

* numpy
* pandas
* selenium

### To install python module use pip. example:

pip install numpy

## Contact Information

If you have any questions, contact Tom Burns: github.com/tomdburns
