import pandas as pd
import numpy as np
from FilesToAnalyze import ATS_path
from FilesToAnalyze import dls_to_analyze_dict
from datetime import datetime
from zhou_utils import view_utils as view
from tabulate import tabulate

# TODO: Print out all different dtypes in a column.
# TODO: better printing to word for tabulate
# TODO: include date time of analysis

#display options
view.display_options()

# Parameters:
# -must be csv

def FitToWord(df):
    col_fit_to_word = 6
    tables_to_print = int(np.ceil(df.shape[1] / col_fit_to_word))
    for col_slice in range(1, tables_to_print + 1):
        print(tabulate(df.iloc[0:5, (col_slice * col_fit_to_word) - col_fit_to_word:col_slice * col_fit_to_word],
                       headers=('keys'), tablefmt='psql'))
        print(col_slice)

# def run_summary(filepath, filename, header):

# can run the below line by line for quick data exploration in console

filepath = ATS_path
filename = dls_to_analyze_dict.get('RCSD')[0]
header = dls_to_analyze_dict.get('RCSD')[1]

df = pd.read_csv(filepath + filename, header=header)

# snapshot: first 5 rows
print(f"{filename} Snapshot")
print(datetime.now())
print("Dimensions: " + str(df.shape))
FitToWord(df)
print("\n")

# meta attributes
print("Field Meta Attributes & Summary Statistics")
print("\n")

# types as raw download
dtype_df = df.dtypes.to_frame().T

# summary stats
sum_df = df.sum(axis=0, numeric_only=True).to_frame().T
mean_df = df.mean(axis=0, numeric_only=True).to_frame().T

summary_frames = [dtype_df, sum_df, mean_df]

col_summary_df = (pd.concat(summary_frames, axis=0, join='outer', sort=False, ignore_index=True)
                    .rename(index={0: 'DType',
                                   1: 'Sum',
                                   2: 'Mean'})
                 )

# create dictionary of column to frequency
# value_counts() already sorted from highest to lowest
df.fillna('NaN', inplace=True)
hist_col_vals = {col: df[col].value_counts() for col in df}

# create dictionary of column names to all their values
all_col_vals = {col: {*df[col]} for col in df}

# print all column names
print('\n')
for key in all_col_vals.keys():
    print(key)
print('\n')

for keys,vals in hist_col_vals.items():
    print(f"~* {keys} *~")
    print("# of Returned Values: " + str(vals.count()))
    vals_nan = 'NaN' in vals.index
    print("Any NAs?: " + str(vals_nan))
    try:
        if vals.count() < 10:
            print("All Returned Values:")
            print(tabulate(vals.to_frame(),headers=('Value','Freq'),tablefmt='psql'))
        else:
            print("Sample of Most Frequent:")
            print(tabulate(vals[0:5].reset_index(),headers=('Value','Freq'),tablefmt='psql',showindex=False))
            print("Sample of Least Frequent:")
            print(tabulate(vals[-5:].reset_index(),headers=('Value','Freq'),tablefmt='psql',showindex=False))
    except:
        print("Unknown Exception occurred.")
    print(tabulate(col_summary_df[keys].to_frame(),tablefmt='psql'))
    print("\n")

# average #s of each column for each cluster?
# cluster_means_df = df.groupby(['Cluster']).mean()