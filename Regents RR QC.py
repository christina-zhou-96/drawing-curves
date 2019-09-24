# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 13:11:15 2019

@author: tgund

Purpose: Output January Regents retention rights file for DIIT
Sources:
    1. Per Session Hours Matrix (excel)
    2. Review Candidates (excel)
    3. Bulk Job Reports
    4. DARI_CUMULATIVE_REGENTS_RR

Created: 8/20/2019
Last Updated: 8/20/2019
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 1: IMPORT LIBRARIES WE WILL NEED
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
import pandas as pd  # data transformation
import numpy as np  # calculation functions
import glob

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 2: CHANGE THESE VARS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 0. PREVIOUS ADMINISTRATION
admin = 'Jan2019'
# 1. path to files we are using
path = r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\Regents\DSS_Pilots\January 2020\Retention ' \
       r'Rights\Python\QC\Data Sources\\'
# 2. per session hours matrix file name
matrixfile = 'Per Session Hours Matrix.xlsx'
# 3. review cands file name
candsfile = 'RGNTReviewCandidates.xlsx'
# 4. bulk job path
bulkPath = r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\Regents\DSS_Pilots\January 2020\Retention ' \
           r'Rights\Python\QC\Data Sources\Bulk Jobs\BulkJobDetailReport - Teachers.xlsx'
# 5. cumulative retention rights file name
rrfile = 'DARI_CUMULATIVE_REGENTS_RR.xlsx'
# 6. output location
outputPath = r'\\CENTRAL.NYCED.ORG\DoE$\DAAR\Assessment\Summative Assessment\Regents\DSS_Pilots\January ' \
             r'2020\Retention Rights\Python\QC\\'
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 2: IMPORT FILES WITH DATA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. import per session hours matrix
psHours = pd.read_excel(path + matrixfile)
rrHours = psHours  # so we can always ref the original
# 2. import review cands
reviewCands = pd.read_excel(path + candsfile, header=1)
accepted = reviewCands  # so we can always ref the original
# 3. import bulk job reports
bulkData = pd.read_excel(bulkPath, index_col=None, header=3)
# 4. import cumulative retention rights info
retentionRights = pd.read_excel(
    path + rrfile)
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 3: PREPARE VARIABLES & CONSTRAINTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. qualifying dates
scoringDates = {'ALL': list(pd.date_range(start='1/22/2019', end='1/27/2019')),
                'HXRU': list(pd.date_range(start='1/23/2019', end='1/27/2019')),
                'SXRK': list(pd.date_range(start='1/23/2019', end='1/27/2019')),
                'EXRC': list(pd.date_range(start='1/22/2019', end='1/27/2019')),
                'MXRC': list(pd.date_range(start='1/24/2019', end='1/27/2019')),
                'HXRT': list(pd.date_range(start='1/25/2019', end='1/27/2019')),
                'HXRC': [],
                'SXRU': list(pd.date_range(start='1/25/2019', end='1/27/2019')),
                'MXRN': list(pd.date_range(start='1/25/2019', end='1/27/2019')),
                'SXRX': list(pd.date_range(start='1/25/2019', end='1/27/2019')),
                'SXRP': list(pd.date_range(start='1/25/2019', end='1/27/2019'))}
for exam in list(scoringDates.keys()):
    scoringDates[exam] = pd.to_datetime(scoringDates[exam])
# 2. all positions + positions to drop
positions = {'ATS Specialist': 'AS',
             'Content Trainer': 'CL',
             'Lead Content Trainer': 'LC',
             'Organizational Team Lead': 'OL',
             'Organizational Team Member': 'OT',
             'Retired Site Supervisor': 'RSS',
             'Scorer': 'SC',
             'Site Supervisor': 'SS',
             'Translator': 'TL'}
dropPositions = {'Retired Site Supervisor': 'RSS',
                 'Site Supervisor': 'SS'}
# 3. columns we need from dataframes
bulkCols = {'EisId': 'EisID',  # key
            'EarnDt': 'Date',
            'SrvHrs': 'Hours',
            'SrvMns': 'Minutes'}
candsCols = {'File #': 'EisID',
             'App Status': 'Status',
             'Position Applied': 'Position',
             'Exam ID': 'Exam ID',
             'Exam': 'Exam',
             'Site': 'Scoring Site'}
# 4. variable to set threshold as a certain pct of the modes for position/exam
threshold = .9
# 5. methods we are looking at for analyzing retention rights
method1 = 'Mode by Position'
method2 = 'Mode by Position - Site'
method3 = 'Mode by Earliest Close - Position'
methodOrder = [method1, method2, method3]
# 6. exam administrations considered by exam for rrs; update if necessary
lastPS_admin = {'EXRC': 'Jan2018',
                'HXRT': 'Jan2018',
                'HXRU': 'Jan2018',
                'MXRC': 'Jan2018',
                'MXRN': 'Jan2018',
                'SXRK': 'Jan2018',
                'SXRP': 'Jan2018',
                'SXRU': 'Jan2018',
                'SXRX': 'Jan2018',
                'ALL': 'Jan2018'}
currentPS_admin = {'EXRC': 'Jan2018',
                   'HXRT': 'Jan2018',
                   'HXRU': 'Jan2018',
                   'MXRC': 'Jan2018',
                   'MXRN': 'Jan2018',
                   'SXRK': 'Jan2018',
                   'SXRP': 'Jan2018',
                   'SXRU': 'Jan2018',
                   'SXRX': 'Jan2018',
                   'ALL': 'Jan2018'}
# 7. for multiindex work
idx = pd.IndexSlice
# 8. output col order
outputCols = ['File', 'PositionID', 'ExamID', 'Last', 'First']
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 4: TRANSFORM OUR DATA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. eschew the columns we do not need in the bulk frame & rename cols
bulk = bulkData[list(bulkCols.keys())]
bulk.rename(columns=bulkCols, inplace=True)
# 2. combine hrs & minutes into hours w/ decimal
bulk['Time Worked'] = round(bulk['Hours'] + (bulk['Minutes'] / 60), 1)
bulk.drop(columns=list(bulkCols.values())[2:4], inplace=True)
# 3. eschew the columns we do not need from reviewCands & rename cols
cands = reviewCands[list(candsCols.keys())]
cands.rename(columns=candsCols, inplace=True)
# 3b. pare down Scoring Site so it's just the DBN
cands['Scoring Site'] = cands['Scoring Site'].str[:6]
cands['Scoring Site'] = cands['Scoring Site'].str.strip()
# 4. merge both these dfs so we have a unified df
candsBulk = cands.merge(bulk, on=['EisID'], how='inner')
# 5. drop the dates we're not interested in
subsets = []
for exam in list(candsBulk['Exam ID'].unique()):
    subset = candsBulk[candsBulk['Exam ID'] == exam]
    subset = subset[subset['Date'].isin(scoringDates[exam])]
    subsets.append(subset)
candsBulk = pd.concat(subsets, axis=0, ignore_index=True)
# 6. create a column with position and exam id as an identifier
candsBulk['Exam ID - Position'] = candsBulk['Exam ID'] + ' - ' + \
                                  candsBulk['Position']
# 7. create a pivoted frame with all time worked/id
candsBulkPivot = candsBulk.pivot_table(values=['Time Worked'],
                                       index=['EisID', 'Exam ID', 'Position',
                                              'Exam ID - Position',
                                              'Scoring Site'],
                                       aggfunc=sum)
candsBulkPivot.reset_index(inplace=True)
candsBulkPivot['EisID'] = candsBulkPivot['EisID'].astype(str)
candsBulkPivot['len'] = candsBulkPivot['EisID'].str.len()
candsBulkPivot['EisID'] = np.where(candsBulkPivot['len'] == 6,
                                   '0' + candsBulkPivot['EisID'], candsBulkPivot['EisID'])
candsBulkPivot.drop(columns=['len'], inplace=True)
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 5: DETERMINE THRESHOLD GENERATING METHODLOGY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
"""~~~                       5a: MODES                                   ~~~"""
# 8. derive mode of time worked for each position; cut off at pct to create
# threshold
modes = pd.DataFrame(candsBulkPivot.groupby('Exam ID - Position') \
                         ['Time Worked'].apply(pd.Series.mode))
modes['Threshold'] = modes['Time Worked'] * threshold
modes.reset_index(level=1, drop=True, inplace=True)
modes.reset_index(inplace=True)
modes.drop(columns='Time Worked', inplace=True)
# 9. create a frame that shows accrual information
rrAccrual = candsBulkPivot.merge(modes, on=['Exam ID - Position'], how='left')
rrAccrual['RR Accrual_mode'] = np.where(
    rrAccrual['Time Worked'] >= rrAccrual['Threshold'], 'Y', 'N')
# 10. ensure the threshold / methodology makes sense
rrSummary = pd.DataFrame(rrAccrual.groupby(['Exam ID - Position',
                                            'RR Accrual_mode']) \
                             ['Exam ID'].count())
rrSummary.reset_index(level=1, inplace=True)
personnelTotals = pd.DataFrame(rrAccrual.groupby(
    ['Exam ID - Position'])['Exam ID'].count())
rrSummary = rrSummary.merge(personnelTotals, on=['Exam ID - Position'],
                            how='left')
rrSummary.rename(columns={'Exam ID_x': 'N',
                          'Exam ID_y': 'Total'}, inplace=True)
rrSummary['%/Total'] = round(rrSummary['N'] / rrSummary['Total'], 3) * 100
rrSummary['Method'] = 'Mode by Position'
rrSummary.rename(columns={'RR Accrual_mode': 'RR Accrual'}, inplace=True)
# visualize
vizFrame = rrSummary.reset_index()
import seaborn as sns
import matplotlib as plt

sns.set(style="darkgrid")
plt.rcParams['figure.figsize'] = (10, 14)
viz_modesRR = sns.barplot(x='%/Total', y='Exam ID - Position',
                          hue='RR Accrual', data=vizFrame)
# viz_modesRR.get_figure().savefig(path+'Jan 2020 RR with Modes.png',
#                      bbox_inches="tight")
"""~~~                       5b: SOME VISUALIZATION                      ~~~"""
# 1. lets take a look at the distribution of hours worked for positions
# boxpolot
timeBoxes = sns.boxplot(x='Time Worked', y='Exam ID - Position', data=rrAccrual)
# timeBoxes.get_figure().savefig(path+'Jan 2020 Time Worked Box Plots.png',
#                      bbox_inches="tight")
timeViolins = sns.violinplot(x='Time Worked', y='Exam ID - Position',
                             data=rrAccrual)
# timeViolins.get_figure().savefig(path+'Jan 2020 Time Worked Violin Plots.png',
#                      bbox_inches="tight")
timeSwarm = sns.factorplot(x='Time Worked',
                           y='Position',
                           data=rrAccrual,
                           row='Exam ID',
                           kind='swarm')
# timeSwarm.get_figure().savefig(path+'Jan 2020 Time Worked Swarm Plots.png',
#                      bbox_inches="tight")
"""~~~                 5c: MODE / POSITION AND SITE                      ~~~"""
modes_SS = pd.DataFrame(candsBulkPivot.groupby(['Exam ID - Position',
                                                'Scoring Site']) \
                            ['Time Worked'].apply(pd.Series.mode))
modes_SS.reset_index(inplace=True)
modes_SS = modes_SS[modes_SS['level_2'] < 1]
modes_SS['Threshold_ss'] = modes_SS['Time Worked'] * threshold
modes_SS.drop(columns=['Time Worked', 'level_2'], inplace=True)
rrAccrual = rrAccrual.merge(modes_SS, on=['Exam ID - Position',
                                          'Scoring Site'], how='left')
rrAccrual['RR Accrual_modeXsite'] = np.where(rrAccrual['Time Worked'] >= \
                                             rrAccrual['Threshold_ss'], 'Y', 'N')
# 10. ensure the threshold / methodology makes sense
rrSummary2 = pd.DataFrame(rrAccrual.groupby(['Exam ID - Position',
                                             'RR Accrual_modeXsite']) \
                              ['Exam ID'].count())
rrSummary2.reset_index(level=1, inplace=True)
rrSummary2 = rrSummary2.merge(personnelTotals, on=['Exam ID - Position'],
                              how='left')
rrSummary2.rename(columns={'Exam ID_x': 'N',
                           'Exam ID_y': 'Total'}, inplace=True)
rrSummary2['%/Total'] = round(rrSummary2['N'] / rrSummary2['Total'], 3) * 100
rrSummary2['Method'] = 'Mode by Position - Site'
rrSummary2.rename(columns={'RR Accrual_modeXsite': 'RR Accrual'}, inplace=True)
rrSummaryFull = rrSummary.append(rrSummary2)
"""THIS COMMENTED OUT CODE VISUALIZES THE DIFFERENCES BET METHODS 1&2"""
# vizFrame2 = rrSummary2.reset_index()
# viz_modes_ssRR = sns.barplot(x='%/Total',y='Exam ID - Position',
#                  hue='RR Accrual_modeXsite',data=vizFrame2)
# viz_modes_ssRR.get_figure().savefig(path+'Jan 2020 RR with Modes by site.png',
#                      bbox_inches="tight")
"""~~~                 5d: MODE BY EARLIEST CLOSE FOR POSITION/EXAM      ~~~"""
candsBulk['EisID'] = candsBulk['EisID'].astype(str)
candsBulk['len'] = candsBulk['EisID'].str.len()
candsBulk['EisID'] = np.where(candsBulk['len'] == 6,
                              '0' + candsBulk['EisID'], candsBulk['EisID'])
# grab max dates by eisID
maxDates = pd.DataFrame(candsBulk.groupby(['EisID', 'Exam ID - Position',
                                           'Exam ID', 'Position',
                                           'Scoring Site'])['Date'] \
                        .max()).reset_index()
# grab max dates by exam id - position and scoring site
maxDates_positionSS = pd.DataFrame(maxDates.groupby(['Exam ID - Position',
                                                     'Scoring Site'])['Date'] \
                                   .max()).reset_index()
# grab minimum dates among those maximum dates, by position
minDates_closed = pd.DataFrame(maxDates_positionSS.groupby(
    'Exam ID - Position')['Date'].min()).reset_index()
minDates_closed.rename(columns={'Date': 'Earliest Close'}, inplace=True)
# match minDates_closed to scoring sites so we can pick our clusters
earliestClose = maxDates_positionSS.merge(minDates_closed, on=[
    'Exam ID - Position'], how='left')
earliestClose = earliestClose[earliestClose['Date'] \
                              == earliestClose['Earliest Close']]
earliestClose['Inclusion'] = 'Yes'
# merge with candsBulkPivot so we can find modes
method3data = candsBulkPivot.merge(earliestClose, on=['Exam ID - Position',
                                                      'Scoring Site'], \
                                   how='left')
method3data = method3data[method3data['Inclusion'] == 'Yes']
# find modes
modes_EC = pd.DataFrame(method3data.groupby(['Exam ID - Position']) \
                            ['Time Worked'].apply(pd.Series.mode))
modes_EC.reset_index(inplace=True)
modes_EC = modes_EC[modes_EC['level_1'] < 1]
modes_EC['Threshold_ec'] = modes_EC['Time Worked'] * threshold
modes_EC.drop(columns=['Time Worked', 'level_1'], inplace=True)
rrAccrual = rrAccrual.merge(modes_EC, on=['Exam ID - Position'], how='left')
rrAccrual['RR Accrual_modeXearliest'] = np.where(rrAccrual['Time Worked'] >= \
                                                 rrAccrual['Threshold_ec'], 'Y', 'N')
# 10. ensure the threshold / methodology makes sense
rrSummary3 = pd.DataFrame(rrAccrual.groupby(['Exam ID - Position',
                                             'RR Accrual_modeXearliest']) \
                              ['Exam ID'].count())
rrSummary3.reset_index(level=1, inplace=True)
rrSummary3 = rrSummary3.merge(personnelTotals, on=['Exam ID - Position'],
                              how='left')
rrSummary3.rename(columns={'Exam ID_x': 'N',
                           'Exam ID_y': 'Total'}, inplace=True)
rrSummary3['%/Total'] = round(rrSummary3['N'] / rrSummary3['Total'], 3) * 100
rrSummary3['Method'] = 'Mode by Earliest Close - Position'
rrSummary3.rename(columns={'RR Accrual_modeXearliest': 'RR Accrual'},
                  inplace=True)
rrSummaryFull = rrSummaryFull.append(rrSummary3)
# visualize the differences in impact between our three methods
full = rrSummaryFull.reset_index()
full['Accrual - Method'] = full['RR Accrual'] + ' - ' + full['Method']
fullViz = sns.catplot(x='%/Total', y='Exam ID - Position',
                      hue='RR Accrual', col='Method', data=full, kind='bar')
# fullViz.savefig(path+'Jan 2020 RR Method Impact Graphs.png',
#                     bbox_inches="tight")
# tabulate the differences in impact between our methods
rrSummaryFull.reset_index(inplace=True)
rrSummaryPivot = rrSummaryFull.pivot_table(values=['%/Total'],
                                           index=['Exam ID - Position'],
                                           columns=['Method', 'RR Accrual']) \
    .fillna(0)
# change the order of methods in our table, for presentation
rrSummaryPivot = rrSummaryPivot.reindex(methodOrder, axis=1, level=1)
# add avg pcts
rrSummaryMeans = pd.DataFrame(rrSummaryPivot.mean(axis=0))
rrSummaryMeans.reset_index(inplace=True)
rrSummaryMeans['Exam ID - Position'] = 'Exam-level Average'
rrSummaryMeans = rrSummaryMeans.pivot_table(values=[0],
                                            index=['Exam ID - Position'],
                                            columns=['level_0', 'Method',
                                                     'RR Accrual'])
rrSummaryMeans.columns = rrSummaryMeans.columns.droplevel(0)
rrSummaryMeans = rrSummaryMeans.round(1)
rrSummaryPivot = rrSummaryPivot.append(rrSummaryMeans)
# NOW TOTAL %
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 6: APPEND INTERNAL WORK HISTORY FILE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. update the eisid information in history file
retentionRights['EisID'] = retentionRights['EisID'].astype(str)
retentionRights['len'] = retentionRights['EisID'].str.len()
retentionRights['EisID'] = np.where(retentionRights['len'] == 6,
                                    '0' + retentionRights['EisID'], retentionRights['EisID'])
del retentionRights['len']
# 2. format this year's info to update file
appendData = rrAccrual.replace({'Position': positions})
appendData['Administration'] = admin
appendData.rename(columns={'Exam ID': 'Exam',
                           'Time Worked': 'Hours',
                           'Position': 'Posting ID'}, inplace=True)
appendData.drop(columns=['Exam ID - Position',
                         'Scoring Site',
                         'Threshold',
                         'Threshold_ss',
                         'Threshold_ec'], inplace=True)
# 3. cut different internal files so we can analyze each for options
appendDict = {}
cumul_RRs = {}
methodCols = ['RR Accrual_mode', 'RR Accrual_modeXsite',
              'RR Accrual_modeXearliest']
for col, method in zip(methodCols, methodOrder):
    appendDict[method] = appendData.rename(columns={col: 'RR Accrual'})
    appendDict[method] = appendDict[method][list(retentionRights.columns)]
    cumul_RRs[method] = retentionRights.append(appendDict[method])
    cumul_RRs[method].replace({'ALL Exams': 'ALL'}, inplace=True)
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 7: ANALYZE RETENION RIGHTS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. grab name info to merge
import pyodbc

stars = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=ES00VADOSQL001;'
    'Database=STARS_INT;'
    'Trusted_Connection=yes;')
# 5b. run our sql query to grab eisid, first name, and last name
eisid = pd.read_sql_query(
    'SELECT LastName, FirstName, EisID \
    FROM STARS_INT.dbo.Personnel',
    stars)
# 5c. create a fullname column
eisid['EisID'] = eisid['EisID'].astype(str)
eisid['len'] = eisid['EisID'].str.len()
eisid['EisID'] = np.where(eisid['len'] == 6, '0' + eisid['EisID'], eisid['EisID'])
eisid['LastName'] = eisid['LastName'].str.upper()
eisid['FirstName'] = eisid['FirstName'].str.upper()
eisid.rename(columns={'LastName': 'Last', 'FirstName': 'First'}, inplace=True)
del eisid['len']
# 5d. delete FirstName and LastName columns
rrPivots = {}
adminOrder = ['Previous', 'Most Recent']
for method in list(cumul_RRs.keys()):
    cumul_RRs[method]['Inclusion'] = cumul_RRs[method]['Exam']
    cumul_RRs[method]['Inclusion'].replace(lastPS_admin, inplace=True)
    cumul_RRs[method]['Inclusion'] = np.where(
        cumul_RRs[method]['Administration'] == admin, admin,
        cumul_RRs[method]['Inclusion'])
    cumul_RRs[method] = cumul_RRs[method][cumul_RRs[method]['Administration'] \
                                          == cumul_RRs[method]['Inclusion']]
    cumul_RRs[method].drop(columns=['Inclusion'], inplace=True)
    cumul_RRs[method]['Admin_simple'] = np.where(
        cumul_RRs[method]['Administration'] == admin, 'Most Recent', 'Previous')
    rrPivots[method] = cumul_RRs[method].pivot_table(
        values=['RR Accrual'], index=['EisID',
                                      'Exam', 'Posting ID'], columns=['Admin_simple'],
        aggfunc=lambda x: ' '.join(x))
    rrPivots[method].columns = rrPivots[method].columns.droplevel(0)
    rrPivots[method] = rrPivots[method][rrPivots[method]['Most Recent'] == \
                                        rrPivots[method]['Previous']]
    rrPivots[method] = rrPivots[method][rrPivots[method]['Most Recent'] == 'Y']
    rrPivots[method].reset_index(inplace=True)
    rrPivots[method] = rrPivots[method][~rrPivots[method]['Posting ID'].isin \
        (list(dropPositions.values()))]
    rrPivots[method] = rrPivots[method].merge(eisid, on=['EisID'], how='left')
    rrPivots[method].rename(columns={'Exam': 'ExamID',
                                     'Posting ID': 'PositionID',
                                     'EisID': 'File'}, inplace=True)
    rrPivots[method] = rrPivots[method][outputCols]
    rrPivots[method].set_index('File', inplace=True)
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 8: QC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. each eisid only represented once
"""
methodDuplicates = {}
for method in list(cumul_RRs.keys()):
    rrPivots[method].reset_index(inplace=True)
    rrPivots[method]['dupes'] = rrPivots[method].duplicated(subset=['file'],
            keep=False)
    methodDuplicates[method] = rrPivots[method][rrPivots[method]['dupes']==\
                     True]
    rrPivots[method].drop(columns=['dupes'],inplace=True)
    rrPivots[method].set_index('file',inplace=True)
# 2. all eligible exams and positions are accounted for
for method in list(cumul_RRs.keys()):
    print(rrPivots[method]['ExamID'].unique())
    print(rrPivots[method]['PostingID'].unique())
"""
"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            STEP 9: OUTPUT FILES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
# 1. file for diit
for method in list(rrPivots.keys()):
    fn = method + '_test.xlsx'
    rrPivots[method].to_excel(outputPath + fn)
# 2. thresholds for qc
modeFrames = [modes, modes_EC, modes_SS]
modeFrames2 = ['modes', 'modes_EC', 'modes_SS']
for thresholds, names in zip(modeFrames, modeFrames2):
    fn = names
    thresholds.to_excel(outputPath + names + '.xlsx')