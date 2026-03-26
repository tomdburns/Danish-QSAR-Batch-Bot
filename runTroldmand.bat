@echo off
call "C:\ProgramData\anaconda3\condabin\conda.bat" activate danish
call python troldmand.py
call "C:\ProgramData\anaconda3\condabin\conda.bat" deactivate