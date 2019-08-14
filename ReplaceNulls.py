import pandas as pd
import numpy as np
import glob
import csv
import xlrd


original = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\SQL FXTS.csv'
modified = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\SQL FXTS No Nulls.csv'

reps = {
    'NULL' : ''
}

def replace_all(text, dic):
    for i, j in reps.items():
            text = text.replace(i, j)
    return text

with open(original,'r') as f:
    text=f.read()
    text=replace_all(text,reps)

with open(modified, 'w') as w:
    w.write(text)
