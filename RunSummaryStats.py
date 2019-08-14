import pandas as pd
import numpy as np
from FilesToAnalyze import ATS_path
from FilesToAnalyze import dls_to_analyze_dict
from tabulate import tabulate

# TODO: Print out all different dtypes in a column.
# TODO: better printing to word for tabulate
# TODO: include date time of analysis

#display options
pd.options.display.float_format = '{:.0f}'.format
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 50)

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
print("Dimensions: " + str(df.shape))
FitToWord(df)
print("\n")

# meta attributes
print("Field Meta Attributes & Summary Statistics")
print("\n")

# types as raw download
dtype_df = df.dtypes.to_frame().T

# types after soft inference
inferred_df = df.infer_objects().dtypes.to_frame().T

# summary stats
sum_df = df.sum(axis=0, numeric_only=True).to_frame().T
mean_df = df.mean(axis=0, numeric_only=True).to_frame().T

summary_frames = [dtype_df, inferred_df, sum_df, mean_df]

col_summary_df = (pd.concat(summary_frames, axis=0, join='outer', sort=False, ignore_index=True)
                    .rename(index={0: 'DType',
                                   1: 'Inferred Type',
                                   2: 'Sum',
                                   3: 'Mean'})
                 )

# already sorted from highest to lowest
hist_col_vals = {col: df[col].value_counts() for col in df}

all_col_vals = {col: {*df[col]} for col in df}
# TODO: print all col vals to see all headers
for keys,vals in hist_col_vals.items():
    print(f"~* {keys} *~")
    print("# of Returned Values: " + str(vals.count()))
    # TODO: next line is not accurate
    # print("Any NAs?: " + str(vals.isna().any()))
    try:
        if vals.count() < 10:
            print("All Returned Values:")
            print(tabulate(vals.to_frame(),headers=('Value','Freq'),tablefmt='psql'))
        else:
            print("Most Frequent:")
            print(tabulate(vals[0:5].reset_index(),headers=('Value','Freq'),tablefmt='psql',showindex=False))
            print("Least Frequent:")
            # TODO: what if there are many 1 frequency values
            print(tabulate(vals[-5:].reset_index(),headers=('Value','Freq'),tablefmt='psql',showindex=False))
    except:
        print("Unknown Exception occurred.")
    print(tabulate(col_summary_df[keys].to_frame(),tablefmt='psql'))
    print("\n")

# average #s of each column for each cluster?
# cluster_means_df = df.groupby(['Cluster']).mean()