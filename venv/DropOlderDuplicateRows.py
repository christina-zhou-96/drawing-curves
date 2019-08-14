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
desktoppath = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop'
SchoolFromSQLfilename = "\School from SQL.csv"
NewSQLFilename = "\SQL Without Duplicates.csv"

SQLdf = pd.read_csv(desktoppath + SchoolFromSQLfilename)

#grab column indices
cols = np.array(SQLdf.columns)
print(SQLdf.columns)

#dependency: SQL query must be "all"
#only keep relevant columns
SQLdf = SQLdf.iloc[:,[64,44,45,63]]

#check: return datatypes
    #print(SQLdf.dtypes)

#create new column that concatenates date and time for sorting
SQLdf['P2_TIMESTAMP'] = [int(str(date) + str(time)) for date, time in zip(SQLdf['SCAN_P2_DTE'], SQLdf['SCAN_P2_TIME'])]

#check: new column has been added, old columns are there
    # print('\n')
    # print(SQLdf.columns)
    # print('\n')
    # print(SQLdf[SQLdf['STUDENT_NAM'] == "SCOZZARI,MARCELLA"])
    # print("Original value")
    # # print(SQLdf.iloc[10:15])
    # # print("Rows 10-15")
    # print('\n')
    # print('\n')

#sort based on timestamp
SQLdf.sort_values(['P2_TIMESTAMP'], inplace=True, ascending=False)

#check: sort worked
    # print(SQLdf[SQLdf['STUDENT_NAM'] == "SCOZZARI,MARCELLA"])
    # print("Ascending by both p2 date and time")
    # print(SQLdf.iloc[10:15])
    # print("Rows 10-15")
    # print('\n')
    # print('\n')

#drop older rows which are now appearing last
SQLdf = SQLdf.drop_duplicates(subset='STUDENT_ID', keep='first')

#check final dataframe
    # print(SQLdf[SQLdf['STUDENT_NAM'] == "SCOZZARI,MARCELLA"],"SCAN_P2_DTE")
    # print('\n')
    # print(SQLdf.iloc[10:15])
    # print("Rows 10-15")

#TODO: write to new file]
SQLdf.to_csv(desktoppath + NewSQLFilename)


