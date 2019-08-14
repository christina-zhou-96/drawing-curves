import pandas as pd
import numpy as np
import glob
import csv
import xlrd
import os
import openpyxl
import xlsxwriter


#display options
pd.options.display.float_format = '{:.0f}'.format
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 50)

#read raw data

#TODO: test that formulas will autorun

#clone old master excel file
#sciencepath = r'R:\DAAR\Assessment\Summative Assessment\ELA-Math\ELA-Math 2019\Reporting\SCIENCE 2019'

sciencepath = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\SCIENCE 2019'
Science4filenametype = "Science Grade 4 Incomplete Report"
Science8filenametype = "Science Grade 8 Incomplete Report"

#find files based on timestamp
list_of_SCSD_4_files = glob.glob(sciencepath + "\\" + Science4filenametype + "*.*")
list_of_SCSD_8_files = glob.glob(sciencepath + "\\" + Science8filenametype + "*.*")

new_SCSD_4_DARI_file = max(list_of_SCSD_4_files, key=os.path.getctime)
# old_SCSD_4_DARI_file = min(list_of_SCSD_4_files, key=os.path.getctime)
new_SCSD_8_DARI_file = max(list_of_SCSD_8_files, key=os.path.getctime)
# old_SCSD_8_DARI_file = min(list_of_SCSD_8_files, key=os.path.getctime)

#verify files based on timestamp
    # print(new_SCSD_4_DARI_file)
    # print(old_SCSD_4_DARI_file)
    # print(new_SCSD_8_DARI_file)
    # print(old_SCSD_8_DARI_file)

#old code
    # OldScience4file = [os.path.basename(x) for x in glob.glob(sciencepath + "\\" + Science4filenametype + "*.*")]
    # OldScience8file = [os.path.basename(x) for x in glob.glob(sciencepath + "\\" + Science8filenametype + "*.*")]

#old code: test
    # print(OldScience4file[-1])
    # print(OldScience8file[-1])
    #
    # Science4df = pd.read_excel(sciencepath + "\\" + OldScience4file[-1],header=4)
    # Science8df = pd.read_excel(sciencepath + "\\" + OldScience8file[-1],header=4)


# old_SCSD_4_DARI_Dataframe = pd.read_excel(old_SCSD_4_DARI_file,header=4)
# old_SCSD_8_DARI_Dataframe = pd.read_excel(old_SCSD_8_DARI_file,header=4)


#test
    # print(Science4df.iloc[1:15])
    # print(Science8df.iloc[1:15])
    # print(list(enumerate(Science4df.columns)))
    # print(list(enumerate(Science8df.columns)))
    # print("\n")



#clear old columns of old master excel file dataframe
"""
"""

#drop in new data into columns of old master excel file dataframe
SCSDdroppath = sciencepath + "\\" + "SCSD Drops"
SCSD4filenametype = "SCSD Gr4"
SCSD8filenametype = "SCSD Gr8"

SCSD4file = [os.path.basename(x) for x in glob.glob(SCSDdroppath + "\\" + SCSD4filenametype + "*.*")]
SCSD8file = [os.path.basename(x) for x in glob.glob(SCSDdroppath + "\\" + SCSD8filenametype + "*.*")]

#test
# print(SCSD4file[-1])
# print(SCSD8file[-1])

RawSCSD4DF = pd.read_csv(SCSDdroppath + "\\" + SCSD4file[-1], header=6, skipfooter=17)
RawSCSD8DF = pd.read_csv(SCSDdroppath + "\\" + SCSD8file[-1], header=6, skipfooter=17)
#test
    # print("At line 81: should have the raw scsds")
    # print("\n")
    # print(RawSCSD4DF.iloc[1:15])
    # print(RawSCSD8DF.iloc[1:15])
    # print(list(enumerate(RawSCSD4DF.columns)))
    # print(list(enumerate(RawSCSD8DF.columns)))
    # print("\n")
"""
"""
#drop unnecessary rows and cols
RawSCSD4DF = RawSCSD4DF.iloc[7:,0:23]
RawSCSD8DF = RawSCSD8DF.iloc[7:,0:23]
#test
    # print("At line 90: should have dropped unnecessary stuff for raw scsds")
    # print("\n")
    # print(RawSCSD4DF.iloc[1:15])
    # print(RawSCSD8DF.iloc[1:15])
    # print(list(enumerate(RawSCSD4DF.columns)))
    # print(list(enumerate(RawSCSD8DF.columns)))
    # print("\n")
"""
"""
#WRITE NEW DATAFRAME INTO NEW FILE

#clear out the old data? how?

#write in new data
SCSD_4_DARI_writer = pd.ExcelWriter(new_SCSD_4_DARI_file, engine='openpyxl', mode='a')
SCSD_8_DARI_writer = pd.ExcelWriter(new_SCSD_8_DARI_file, engine='openpyxl', mode='a')
RawSCSD4DF.to_excel(SCSD_4_DARI_writer,startrow=5, startcol=13, header=False, index=False)
SCSD_4_DARI_writer.save()
RawSCSD8DF.to_excel(SCSD_8_DARI_writer,startrow=5, startcol=13, header=False, index=False)
SCSD_8_DARI_writer.save()

# append_df_to_excel(new_SCSD_4_DARI_file,RawSCSD4DF,startrow=5,startcol=13)
# append_df_to_excel(new_SCSD_8_DARI_file,RawSCSD8DF,startrow=5,startcol=13)
print("dun")

#check # of rows is same from data to excel file

#check for summary stat diffs from last time to now

#check that formulas are working properly (test in 3 rows) in excel file

