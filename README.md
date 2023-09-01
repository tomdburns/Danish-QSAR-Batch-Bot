# Danish QSAR Batch Bot
 A Bot that runs chemicals through the Danish QSAR Models in batch mode

================================================================
Troldmand v1.0.0

Author: Tom Burns
Date  : August 31st, 2023
================================================================

Troldmand is a code written in python that was written with the
goal of automating a batch mode for the Danish QSAR models:

https://qsarmodels.food.dtu.dk/runmodel/index.html

To run the code, add the SMILES you wish to run to a .txt file


To run (python):

python troldmand.py -i \path\to\your\smiles\file.txt -o \path\to\output\file.csv

You can see the list of options by typing:

python troldmand.py --help

================================================================

Python dependencies

The following python modules are needed to run this code:

numpy
pandas
selenium

To install python module use pip. example:

pip install numpy

================================================================

If you have any questions, contact Tom Burns: tom.burns@ec.gc.ca
