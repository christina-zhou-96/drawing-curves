#https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html#boolean-indexing
# merges
# practical business python
# excel to python
# python under the hood
# python compared to OOP
# https://docs.python.org/3/tutorial/
# regex
# functional python


# To quickly grab a list of all possible values from a filter drop down in Excel:
# in Excel, use a formula like this =CONCATENATE("'",F3242,"'",",") down a column to convert the strings for list formatting
# copy paste all the values into list = [copy paste]
# convert to set: list = set(list)
# print out the list and now it's a set

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


DARI_team_members = pd.Series(["Anthony", "Phil", "Christina", "Tyler", "Ronli", np.nan])

grades = np.random.randint(100,size=(10,6))

exam_dates = pd.date_range(start='20000615', end='20010615', periods=10)

DARI_exam_scores_df = pd.DataFrame(grades,index=exam_dates,columns=DARI_team_members)

Regents_Dict = pd.DataFrame({'New Global': "HXRC",
                             'US History': "HXRU",
                             'Living Environment': "SXRK",
                             'Algebra I': "MXRC",
                             'All Exams': pd.Categorical(["New Global", "US History", "Living Environment", "Algebra I"]),
                             'Year': 2019}, index=pd.Series("Exam Code", index=list(range(4))))
# print(Regents_Dict)
# print("\n")
# print(Regents_Dict.dtypes)
# print(Regents_Dict.head())
# print(Regents_Dict.tail(3))
# print(Regents_Dict.index)
# print(Regents_Dict.columns)

# print(DARI_exam_scores_df.describe())
# print(DARI_exam_scores_df.transpose())

# print(DARI_exam_scores_df.sort_index(axis=0, ascending=False))

# print(DARI_exam_scores_df.sort_values(by='Phil', ascending=False))

# print(DARI_exam_scores_df.Phil)
# print(DARI_exam_scores_df['Phil'])
#
# print(DARI_exam_scores_df[1:2])
# print(DARI_exam_scores_df['2000-06-15 00:00:00':'2000-06-22 12:00:00'])

# print(DARI_exam_scores_df.loc[exam_dates[2]])
# print(DARI_exam_scores_df.loc[:, ['Phil','Christina']])

# DARI_exam_scores_df.loc['2000-06-15 00:00:00':'2000-06-22 12:00:00',['Phil', 'Christina']]
# DARI_exam_scores_df.loc['2000-06-15 00:00:00', ['Phil', 'Christina']]

# DARI_exam_scores_df.loc['2000-06-15 00:00:00', 'Phil']

# DARI_exam_scores_df.at[exam_dates[0], 'Phil']

# DARI_exam_scores_df.iloc[0]
# DARI_exam_scores_df.iloc[1]
# DARI_exam_scores_df.iloc[2]
#
# DARI_exam_scores_df.iloc[0:2,0:2]
# DARI_exam_scores_df.iloc[0:3,1:3]
#
# DARI_exam_scores_df.iloc[[0,1],[1,2]]
# DARI_exam_scores_df.iloc[[1,2],[0,4]]
#
# DARI_exam_scores_df.iloc[0:1,]
# DARI_exam_scores_df.iloc[:,1:3]
#
# DARI_exam_scores_df.iloc[0,1]
#
# DARI_exam_scores_df.iat[0,1]
#
#
# DARI_exam_scores_df[DARI_exam_scores_df.Christina<20]
#
# DARI_exam_scores_df[DARI_exam_scores_df<80]
#
# DARI_exam_scores_df[DARI_exam_scores_df>80]


DARI_2ndtryaround_df = DARI_exam_scores_df.copy()
print(DARI_2ndtryaround_df)

DARI_2ndtryaround_df.shape

DARI_2ndtryaround_df['Lunch Break?'] = ['Y', 'Y', 'Y', 'Y', 'N', 'N', 'N', 'N', 'N', 'N']

# DARI_2ndtryaround_df['Lunch Break?'] = ['Y', 'Y', 'Y', 'Y', 'N', 'N', 'N', 'N', 'N', 'N']
# DARI_2ndtryaround_df['Lunch Break?'] = np.array[['Y'] * 4] + np.array[['N'] * 6]


DARI_2ndtryaround_df

DARI_2ndtryaround_df[DARI_2ndtryaround_df['Lunch Break?'].isin(['N'])]

s1 = pd.Series(np.array(['100'] * 10), index=exam_dates)
s1

DARI_2ndtryaround_df['Salary Per Hour'] = s1
DARI_2ndtryaround_df

DARI_2ndtryaround_df.at[exam_dates[9], 'Christina']='100'
DARI_2ndtryaround_df

DARI_2ndtryaround_df.iat[2,1]=100
DARI_2ndtryaround_df

DARI_2ndtryaround_df.loc[:, 'Christina'] = np.array([100] * len(DARI_2ndtryaround_df))
DARI_2ndtryaround_df

list(enumerate(exam_dates))
DARI_Reindexed = DARI_2ndtryaround_df.reindex(index=exam_dates[5:9], columns=list(DARI_2ndtryaround_df.columns) + ['Supervisor Role'])
DARI_Reindexed.loc[exam_dates[5:7], 'Supervisor Role'] = 'Licensed'
DARI_Reindexed

DARI_Reindexed.dropna(how='any')
DARI_Reindexed.fillna('Not Licensed')
DARI_Reindexed

pd.isna(DARI_Reindexed)
# # why doesn't this work?
# DARI_Everything_Is_Negative_df = DARI_2ndtryaround_df.copy
# DARI_Everything_Is_Negative_df[DARI_Everything_Is_Negative_df<50] = -DARI_Everything_Is_Negative_df
# DARI_Everything_Is_Negative_df

'''
tutorial stuff
'''
# dates = pd.date_range('20130101', periods=6)
# df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
#
# df1 = df.reindex(index=dates[0:4], columns = list(df.columns) + ['E'])
#
# df1.loc[dates[0]:dates[1], 'E'] = 1
# df1
#
# df1.dropna(how='any')
# df1
#
# df1.fillna(value=5)
#
# pd.isna(df1)
#
# df.mean()
# df.mean(1)

'''back to DARI'''

DARI_exam_scores_df.mean()

DARI_exam_scores_df.mean(1)

CurveSubtractGrades = pd.Series([2, 1, 0, 3, 1] * 2, index=exam_dates).shift(-2)
CurveSubtractGrades

DARI_exam_scores_df.sub(CurveSubtractGrades, axis='index')

DARI_exam_scores_df.apply(np.cumsum)

DARI_exam_scores_df.apply(lambda x: x.max() - x.min())

s = pd.Series(np.random.randint(0, 7, size=10))
s

s.value_counts()

DARI_exam_scores_df['Anthony'].value_counts()

DARI_Reindexed['Supervisor Role'].str.lower()

'''
Tutorial stuff.... again
'''
df = pd.DataFrame(np.random.randn(10, 4))
df

pieces = [df[:3],df[3:7],df[7:]]

pd.concat(pieces)

left = pd.DataFrame({'key': ['MXRU', 'HXRK'], 'lval': ['Algebra I', 'History']})

right = pd.DataFrame({'key': ['MXRU', 'HXRK'], 'rval': ['June 17', 'June 18']})


pd.merge(left, right, on='key')

'''
but back to DARI
'''
# Appending
DARI_exam_scores_df.shape
last_row = DARI_exam_scores_df.iloc[9]

DARI_exam_scores_df.append(last_row, ignore_index=True)

# Grouping

'''
tutorial stuff
'''

df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar',
                         'foo', 'bar', 'foo', 'foo'],
                   'B': ['one', 'one', 'two', 'three',
                         'two', 'two', 'one', 'three'],
                   'C': np.random.randn(8),
                   'D': np.random.randn(8)})

df.groupby('A').sum()

df.groupby(['A', 'B']).sum()

#Reshaping

'''
tutorial
'''
tuples = list(zip(*[['bar', 'bar', 'baz', 'baz',
                     'foo', 'foo', 'qux', 'qux'],
                    ['one', 'two', 'one', 'two',
                     'one', 'two', 'one', 'two']]))

index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])

df = pd.DataFrame(np.random.randn(8, 2), index=index, columns = ['A', 'B'])

df2 = df[:4]

df2

stacked = df2.stack()

stacked.unstack()

stacked.unstack(1)

stacked.unstack(0)


#Pivot Tables
df = pd.DataFrame({'A': ['one', 'one', 'two', 'three'] * 3,
                   'B': ['A', 'B', 'C'] * 4,
                   'C': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
                   'D': np.random.randn(12),
                   'E': np.random.randn(12)})
df

pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C'])

#Time Series
rng = pd.date_range('1/1/2012', periods=100, freq='S')
ts=pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
ts
rsts = ts.resample('5Min').sum()
rsts

#At time zone representation





