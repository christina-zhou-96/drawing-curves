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
Scoring_Site_Path = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\2. Scoring Progress'

#find latest file
list_of_files = glob.glob(Scoring_Site_Path + "\\*.*")
latest_file = max(list_of_files, key=os.path.getctime)

#verify latest file
    #print(latest_file)

ScoringSiteXls = pd.ExcelFile(latest_file)
ScoringSiteDataDF = pd.read_excel(ScoringSiteXls, 'RSBS & RLBS', header=3)

#check datatypes, column indices, random rows
    # print(list(enumerate(ScoringSiteDataDF.columns)))
    # print(ScoringSiteDataDF.dtypes)
    # print(ScoringSiteDataDF.iloc[10:15])

#subset data based on criteria

ScoringSiteDataDF = ScoringSiteDataDF[ScoringSiteDataDF.Column1.notnull()]

#check that subsetting worked
    #print(ScoringSiteDataDF.columns)
    #print(ScoringSiteDataDF.iloc[10:15])

#check how many duplicates existed

ScoringSiteDataDF = ScoringSiteDataDF.groupby(['Exam+DBN+Section'])['Exam+DBN+Section'].value_counts().to_frame('count')

#check that groupby worked
print(ScoringSiteDataDF.columns)
print(ScoringSiteDataDF.iloc[10:15])
print("Maximum count: " + str(ScoringSiteDataDF['count'].max()))
