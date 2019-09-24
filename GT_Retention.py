# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:43:22 2019

@author: tgund

G&T RETENTION RIGHTS GENERATION
Purpose: Output G&T retention rights file for DIIT
Sources:
    1. bulk reports
    2. hiring data
    4. DARI_CUMULATIVE_G&T_RR

Created: 6/20/2019
Last Updated: 9/4/2019
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
STEP 1: IMPORT PANDAS AND NUMPY SO WE CAN CLEAN AND TRANSFORM OUR DATA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
import pandas as pd  # data cleaning and analysis
import numpy as np  # math
import glob  # pulling bulk files

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                STEP 2: DEFINE OUR VARIABLES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. what school year is it (hint: if 2018-19, value here should be 2019)
schoolYear = 2019
# 2. create variables for our paths and a name for our final file
bulkPath = r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\G&T\2018-19\Weekend Testing\Work ' \
           r'History\Retention Rights\QC\CZ\CZ Testing\Data Sources\Bulk Job\\'
path = r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\G&T\2018-19\Weekend Testing\Work ' \
       r'History\Retention Rights\QC\CZ\CZ Testing\Data Sources\\'
cumulative_file = 'DARI_CUMULATIVE_G&T_RR.xlsx'
applicant_file = 'Applicant Download 2.15.2019.xlsx'
summerSchool_file = 'SITC RR 2019.xlsx'
# cumulative path is where we're putting the cumulative output, for next year
cumulative_output_path = r'R:\DAAR\Assessment\Summative Assessment\G&T\2019-20\Retention Rights (for 2020-2021)\\'
# 3. create a list of dates that are credited (format: YYYY-MM-DD)
scoringDates = [  # this is actually administration for G&T
    '01/05/2019',
    '01/06/2019',
    '01/12/2019',
    '01/13/2019',
    '01/19/2019',
    '01/27/2019',
    '02/02/2019',
    '02/03/2019',
    '02/09/2019',
    '02/10/2019']
scoringDates = pd.to_datetime(scoringDates)  # set it to the right data type
# 4. create a variable containing the number of minutes of work constituting a full day
fullDay = 300
# 5. create a threshold of days worked to be considered eligible for retention rights
threshold = 5
# 6. create a list of retention rights eligible positions
eligiblePositions = ['Teacher', 'Secretary']
# 7. create a list of 'status' values corresponding to 'offer accepted'
accepted = ['Offer Accepted']
# 8. create output names
histFileName = 'GT-WorkHistory.xlsx'
rrFileName = 'GT-RetentionRights.xlsx'
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                STEP 3: IMPORT FILES FOR OUR ANALYSIS AND CLEAN OUR DATA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. import our files as dataframes in a bulk reports dictionary
all_bulk = glob.glob(bulkPath + '/*.xlsx')
bulkJobs = []
for filename in all_bulk:
    df = pd.read_excel(filename, index_col=None, header=3)
    bulkJobs.append(df)
bulkTotal = pd.concat(bulkJobs, axis=0, ignore_index=True)
# 2. add a leading 0 to emplId (first, check the character length; only items with 6 characters need a 0 added)
bulkTotal['EisId'] = bulkTotal['EisId'].astype('str')  # convert to string so we can add leading 0
bulkTotal['EisId'] = np.where(bulkTotal['EisId'].str.len() < 7,
                              '0' + bulkTotal['EisId'], bulkTotal['EisId'])
# TESTING


# 3. combine SrvHrs and SrvMns into one column called Minutes Worked, which computes the two columns into minutes
bulkTotal['SrvHrs'] = bulkTotal['SrvHrs'] * 60  # converts srvhrs to mins
timeCols = ['SrvHrs', 'SrvMns']  # creates a list of columns for us to sum
bulkTotal['Minutes Worked'] = bulkTotal[timeCols].sum(axis=1)  # sums total minutes


# 5. create a variable that determines if the EarnDt value counts as an eligible per session day, using the scoringDates list
def eligibleDate(df):
    for date in scoringDates:
        if df['EarnDt'] == date:
            return 1
        else:
            continue


bulkTotal['eligible date'] = bulkTotal.apply(eligibleDate, axis=1)
bulkTotal['eligible date'].fillna(0, inplace=True)


# 6. create a variable that determines if a full day has been worked (300 minutes/day)
def dayWorked(df):
    if df['Minutes Worked'] >= fullDay:
        return 1
    else:
        return 0


bulkTotal['full day'] = bulkTotal.apply(dayWorked, axis=1)


# 7. create a variable that determines if the entry constitutes both an eligible day and a full day of work
def credit(df):
    if df['eligible date'] == 1 and df['full day'] == 1:
        return 1
    else:
        return 0


bulkTotal['Time Worked'] = bulkTotal.apply(credit, axis=1)
# 8. import cumulative data and clean
workHistory = pd.read_excel(path + cumulative_file)
workHistory['EisID'] = workHistory['EisID'].astype(str)
workHistory['EisID'] = np.where(workHistory['EisID'].str.len() < 7,
                                '0' + workHistory['EisID'], workHistory['EisID'])
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                STEP 4: ANALYZE SUCCESSFULLY WORKED & APPEND CUMULATIVE FILE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. import and clean the applicant file so we can merge job information
cands = pd.read_excel(path + applicant_file)
eligible = cands[cands['Status'].isin(accepted)]
eligible.rename(columns={'File Number': 'EisID'},
                inplace=True)
eligible['EisID'] = eligible['EisID'].astype(str)
eligible['len'] = eligible['EisID'].str.len()
eligible['EisID'] = np.where(eligible['len'] == 6, '0' + eligible['EisID'],
                             eligible['EisID'])
eligible.set_index('EisID', inplace=True)
# 2. create a pivot table showing Time Worked per employee id
workCredits = pd.pivot_table(data=bulkTotal,
                             values=['Time Worked'],
                             index=['EisId'], aggfunc='sum')
workCredits.index.name = 'EisID'
workCredits['Unit of Time'] = 'Days'


# 3. create a column that determines whether or not that ID successfully worked
def success(df):
    if df['Time Worked'] >= 5:
        return 'Y'
    else:
        return 'N'


workCredits['RR Accrual'] = workCredits.apply(success, axis=1)
# 4. create override and school year columns so we cann append the cumulative file
workCredits['RR Override'] = np.NaN
workCredits['School Year'] = schoolYear
# 5. append new data and fix column order/index
workCredits.reset_index(inplace=True)
workCredits = workCredits.merge(eligible[['Position']],
                                on=['EisID'], how='left')
workHistory = workHistory.append(workCredits, ignore_index=True)
col_order = [0, 4, 1, 5, 6, 2, 3]  # update
workHistory = workHistory.ix[:, col_order]
workHistory.set_index('EisID', inplace=True)
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                STEP 5: CREATE DIIT WORK HISTORY FILE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. create a new frame with just the columns we need for transformation
cols = ['School Year', 'RR Accrual']
baseData = workHistory[cols]
# 2. recode the RR column to binary 1/0
baseData['RR Accrual'] = np.where(baseData['RR Accrual'] == 'Y', 1, 0)
# 3. transpose via pivot so we can do the summations we need
baseData.reset_index(inplace=True)
baseData = baseData.pivot_table(index=['EisID'],
                                values=['RR Accrual'],
                                columns=['School Year']).fillna(0)
baseData.columns = baseData.columns.droplevel()
# 4. create Total Years Worked and Consecutive Previous Five Years columns
baseData['Total Years Worked'] = baseData[list(baseData.columns)].sum(axis=1)


def consecutive_five(df):
    if df[schoolYear] == 1 and df[schoolYear - 1] == 0:
        return 1
    elif df[schoolYear] == 1 and df[schoolYear - 1] == 1 and \
            df[schoolYear - 2] == 0:
        return 2
    elif df[schoolYear] == 1 and df[schoolYear - 1] == 1 and \
            df[schoolYear - 2] == 1 and df[schoolYear - 3] == 0:
        return 3
    elif df[schoolYear] == 1 and df[schoolYear - 1] == 1 and \
            df[schoolYear - 2] == 1 and df[schoolYear - 3] == 1 and \
            df[schoolYear - 4] == 0:
        return 4
    elif df[schoolYear] == 1 and df[schoolYear - 1] == 1 and \
            df[schoolYear - 2] == 1 and df[schoolYear - 3] == 1 and \
            df[schoolYear - 4] == 1:
        return 5
    else:
        return 0


baseData['Consecutive Previous Five Years'] = baseData.apply(consecutive_five,
                                                             axis=1)
# 5. pare down to just EisID (index), Total Years Worked, Consecutive Five
diitHist = baseData[list(baseData.columns[-2:])]
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                STEP 6: CREATE DIIT RETENTION RIGHTS FILE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. determine who has retention rights for the coming year
diitRR = baseData[[schoolYear - 1, schoolYear]]
positionWorked = workHistory[workHistory['School Year'].isin([schoolYear - 1,
                                                              schoolYear])]
positionWorked = positionWorked[positionWorked['Position'].isin \
    (eligiblePositions)]
positionWorked.reset_index(inplace=True)
positionWorked = positionWorked.pivot_table(index=['EisID'],
                                            columns=['School Year'],
                                            values=['Position'],
                                            aggfunc=lambda x: ' '.join(x))
positionWorked.columns = positionWorked.columns.droplevel()
positionWorked.rename(columns={schoolYear - 1: '2 Admins Ago',
                               schoolYear: 'Retention Eligible Position'},
                      inplace=True)
diitRR = diitRR.merge(positionWorked, on=['EisID'], how='left')


def retention_rights(df):
    if df[schoolYear - 1] == 1 and df[schoolYear] == 1:
        return 'Y'
    else:
        return 'N'


diitRR['Retention Rights Eligible'] = diitRR.apply(retention_rights,
                                                   axis=1)
# 2. pare down frame to just retention rights holders
diitRR = diitRR[diitRR['Retention Rights Eligible'] == 'Y']
diitRR = diitRR[list(diitRR.columns[-3:])]
# 3. ensure we're only looking at folks who worked the same position for 2 yrs
diitRR['Same Position'] = diitRR['2 Admins Ago'] == \
                          diitRR['Retention Eligible Position']
diitRR = diitRR[diitRR['Same Position'] == True]
diitRR.drop(columns=['2 Admins Ago', 'Retention Rights Eligible', 'Same Position'], inplace=True)
# 4. merge summer school info & pare down diitRR to not include thos folks
summerSchool = pd.read_excel(path + summerSchool_file)
summerSchool.rename(columns={'EISID': 'EisID'}, inplace=True)
summerSchool['Claimed retention on other per session'] = 'Yes'
summerSchool['Claimed retention program name'] = 'Summer School'
keep_cols = list(summerSchool.columns[-2:])
summerSchool.set_index('EisID', inplace=True)
summerSchool = summerSchool[keep_cols]
diitRR = diitRR.merge(summerSchool, on=['EisID'], how='left')

# 5. merge up-to-date name info from stars int
import pyodbc

stars = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=ES00VADOSQL001;'
    'Database=STARS_INT;'
    'Trusted_Connection=yes;')
# 5b. run our sql query to grab eisid, first name, and last name
eisid = pd.read_sql_query(
    'SELECT FirstName, LastName, EisID \
    FROM STARS_INT.dbo.Personnel',
    stars)
# 5c. create a fullname column
eisid['Name'] = eisid['LastName'].str.upper() + \
                ', ' + eisid['FirstName'].str.upper()
eisid = eisid[eisid['Name'] != ', ']  # get rid of rows we don't need
# 5d. delete FirstName and LastName columns
eisid.drop(columns=['FirstName', 'LastName'], inplace=True)
# 5e. merge to diitRR
diitRR = diitRR.merge(eisid, on=['EisID'], how='left')
diitRR.set_index('EisID', inplace=True)
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                STEP 7: OUTPUT NEW LOOKUP FILE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# don't worry about this section, Christina!
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                STEP 8: EXPORT TO EXCEL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# # 1. update cumulative DARI file used for analysis
# workHistory.to_excel(cumulative_output_path + cumulative_file,
#                      sheet_name='G&T RR ACCUMULATION')
# # 2. output work history file and rr for diit
# diitHist.to_excel(path + histFileName)
# diitRR.to_excel(path + rrFileName)