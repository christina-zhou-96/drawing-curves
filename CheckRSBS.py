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
ATSpath = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\ATS Analysis'
RSBSfilename = r'\New RSBS Analysis.xlsx'
Routingsfilename = r'\2019 All Exam Routings.xlsx'
LCGMSfilename = r'\LCGMS_SchoolData_20190702_1325.xls'

# print(desktoppath + "\\" + RSBSfilename)
RSBSdf = pd.read_csv(ATSpath + RSBSfilename)
Routingsdf = pd.read_excel(ATSpath + Routingsfilename)
LCGMSdf = pd.read_excel(ATSpath + LCGMSfilename)

LCGMSdf
# print(Routingsdf)
#
# print(RSBSdf.columns)
# print(RSBSdf.describe())
# print(RSBSdf.iloc[2])
# print(RSBSdf.describe())
# print("\n")

#make a column for dbn, exam, and section
RSBSdf['DBNExamSection'] = RSBSdf['School DBN'].map(str) + RSBSdf['Exam'].map(str) + RSBSdf['Section'].map(str)
print("RSBS df now has new column with tag.")
print(RSBSdf.iloc[2])
print("\n")

#make column for DBN - Exam
RSBSdf['DBNExam'] = RSBSdf['School DBN'].map(str) + " - " + RSBSdf['Exam'].map(str)
print("RSBS df now has new column with abbreviated tag.")
print(RSBSdf.iloc[2])
print("\n")

RSBSdf
#make a column for how many times record appears (ability to find duplicates)
# print(RSBSdf.DBNExamSection.value_counts(sort=False).tolist())
# RSBSdf['Count'] = RSBSdf.DBNExamSection.value_counts(sort=False).tolist()
# print(RSBSdf['Count'])
#
# print("RSBS df now has new column with count.")
# print(RSBSdf.iloc[2])
# print("\n")

#drop all times record appears 0 times (only leaving duplicates)
# RSBSdfduplicates = RSBSdf[RSBSdf.Count > 1]
# print("RSBS duplicates df now only contains duplicates.")
# print(RSBSdfduplicates.iloc[2])
# print(RSBSdfduplicates.describe())
# print("\n")

#if the newer duplicate is a home school, what happens?



'''Questions'''
# Do all routed DBN - Exams appear in RSBS without an *?

# Does every record in the Routings file appear in RSBS?
# When the record does appear, is there at least one instance without a *?
# When the record does appear, and it is with a *, is its new routed building different than its originally routed building?


# Does every record in the Routings file appear in RSBS?
# NO - see 02M575 - HXRC. This is unexpected.
Routingsdf['In RSBS?'] = Routingsdf['DBN - Exam'].isin(RSBSdf['DBNExam'])
Routingsdf[Routingsdf['In RSBS?'] == False]
Routingsdf
# When the record does appear, is there at least one instance without a *?
# YES. This is as expected.
RSBSdf['In Routings?'] = RSBSdf['DBNExam'].isin(Routingsdf['DBN - Exam'])
RSBSdf[(RSBSdf['In Routings'] == True) & (RSBSdf.iloc[:, 0].isnull())]


# When the record does appear, and it is with a *, is its new routed building different than its originally routed building?
# YES. This is unexpected. This occurs for 1 case with 13 records. Ex: 03M402 - HXRC from RCSR was routed to M855. In actuality,
# from the 2019 Routings File, it was supposed to be routed to M600. In the asterisked record, it is routed to M600.


# Does the asterisk appear when the section is scanned at the home DBN instead of at its routed building code? Always?
#process notes:
#make a mapping for DBN to building code
#tag duplicates using column = df.duplicated()
#find the duplicate tag and matching dbnexam, without asterisk <- original record
#where the section is scanned at home dbn, and the routed building for the original record was not the home dbn
#does the asterisk appear any times?
#does the asterisk appear all times?

#There are 1007 cases where the asterisk appears when the section is scanned at the home dbn instead of at its routed building.
#22K425 MXRC

#There are cases where the school's routing was originally at its home school. (7 sections for 32K564 - EXRC). In this case,
#the asterisk does not appear, which is expected.


# Does the asterisk appear when the section is scanned at another scoring site instead of a routed building code? Always?
#Yes: there are 222 instances of this. This seems smaller than expected.

# Does the asterisk appear when the section is scanned at another location neither scoring nor home? Always?
#Yes: there are 3976 instances of this. This seems larger than expected.

#There are 5412 records of 48,928 records that have an asterisk.

#197 of these don't have a corresponding building code with LCGMS for me to perform analysis on. Here are the DBNs:
# '75R505', '79Q344', '88K952', '17K467', '02M473', '79X695', '14K923', '79M973', '13K657', '10X668', '08X507', '19K431', '75K503', '10X503', '75X502', '11X417', '75Q504'

