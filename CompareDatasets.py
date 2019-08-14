import pandas as pd
import numpy as np
import glob
import csv
import xlrd
import os


#download datasets
path = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop'
ATSfile2 = glob.glob(path + "/*ATS.*")
ATSfile = [os.path.basename(x) for x in glob.glob(path + "/*ATS.*")]
SQLfile = [os.path.basename(x) for x in glob.glob(path + "/*SQL.*")]

ATSdf = pd.read_csv(r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\School Direct from ATS.csv', header=2)

SQLdf = pd.read_csv(r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\School from SQL.csv')


fulldf = pd.concat([ATSdf,SQLdf])


#find similar columns
df = pd.reset_index(drop=TRUE)
df_gpby = df.groupby(list(df.columns))
idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]


#check for differences in similar columns only