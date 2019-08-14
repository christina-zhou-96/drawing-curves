import pandas as pd
import numpy as np
import glob
import csv
import xlrd
import os

#TODO: refactor into its own function, make generic, pass in specific args
#TODO: error checks in raw data

#display options
pd.options.display.float_format = '{:.0f}'.format
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 50)

#paths
path = r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\Regents\DSS_Pilots\June 2019\Reporting\1. Box Tracking'
masterfilename = "\Box Tracking Report 6.23 0200pm.xlsm"
outputfilename = "\Box Tracking LOTE Report 6.23 0200pm.xlsm"

#read master excel file
masterdf = pd.read_excel(path + masterfilename, sheet_name=None)

#copy df
#delete old sheets from master

#clone to a new one


#delete sheets not relevant to new one
