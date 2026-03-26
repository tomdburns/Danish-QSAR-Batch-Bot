@echo off
REM Create the environment from the YAML file
conda env create -f data\environment.yml

REM Activate the environment
call conda activate danish

REM Verify the installation
conda list