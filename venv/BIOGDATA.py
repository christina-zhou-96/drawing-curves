import pandas as pd
import numpy as np
import glob
import csv
import xlrd
import os
import openpyxl
import xlsxwriter

pd.options.display.float_format = '{:.0f}'.format
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 50)

#paths
desktoppath = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop'
biogdatafilename = r"\all stuy students born in 1998 from biogdata.csv"


biogdf = pd.read_csv(desktoppath + biogdatafilename)

#grab column indices
cols = np.array(biogdf.columns)
print(biogdf.columns)

biogdf.dropna()

print(biogdf.columns)

#BIOG.DATA
#query all in BIOG.DATA

#note any possible discrepancies

#Max:
#series of grades over time (4 time series for high school years)
    #ELA grades for grade 9
    #Math grades for grade 9
    #ELA grades for grade 10
    #Math grades for grade 10
    #...
#histogram of late arrivals (4 bars for each high school year)
    #Late arrivals in grade 9
#Regents English scores compared to Stuy
#Regents English scores compared to state wide















#Grace:
#series of absences over months (K vs 6th grade)
#ELA scores compared to rest of her grade (scatterplot)
#math scores compared to rest of her grade (scatterplot)
#math scores compared to NYC as a whole (scatterplot)
#math scores compared to Bayside as a whole (scatterplot)



#School Data Trends
#how many immigrant kids?
#how many Chinese/Japanese/Korean kids?
#are better grades correlated with teachers who have been teaching for longer years?

#Stuy




#PS188

