import pandas as pd
import numpy as np
import glob
import csv
import xlrd
import os
import docx
import sys

#display options
pd.options.display.float_format = '{:.0f}'.format
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 50)

#paths
ATSpath = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\ATS Analysis'
Detailed_Analysis_Path = ATSpath + "\\" + "Detailed Analysis"
RCSRfilename = r'\RCSR.csv'
RCSRReportfilename = r'\RCSR Report.docx'

RCSRdf = pd.read_csv(ATSpath + RCSRfilename, header=3)


# what are the possible values in every column?
all_col_vals = {col: {*RCSRdf[col]} for col in RCSRdf}

for keys,vals in all_col_vals.items():
    print(keys)
    print(vals)
    print("\n")


# in total, how many not scanneds were there at the end?
print(RCSRdf['Not Scanned'].sum())

# compared to # of generated?
print(RCSRdf['Generated'].sum())

# compared to # of absences?
print(RCSRdf['ABS'].sum())

# compared to # of fully scanned?
print(RCSRdf['Fully Scanned'].sum())

# what is the average #s of generated and not scanned for each cluster?
cluster_means_df = RCSRdf.groupby(['Cluster']).mean()
clean_cluster_means_df = cluster_means_df[['Generated', 'Not Scanned']]

clean_cluster_means_df.columns = ['Mean Generated', 'Mean Not Scanned']
clean_cluster_means_df

# does ABS:MIS always sum up to Fully Scanned?
scan_investigation_df = pd.DataFrame()

scan_investigation_df['DBN'] = RCSRdf['School DBN']
scan_investigation_df['Exam'] = RCSRdf['Exam']
scan_investigation_df['Are there 0s in P1 and P2?']=(RCSRdf['Page-1 Scanned'] == 0) & (RCSRdf['Page-2 Scanned'] == 0)
scan_investigation_df['Sum of ABS:MIS']=RCSRdf.loc[:, ['ABS', 'INC', '0-54', '55-64', '65-84', '85-100', 'INV', 'MIS']].sum(axis=1)
scan_investigation_df['Fully Scanned']=RCSRdf['Fully Scanned']

# based on understanding, sum should equal fully scanned, as long as there are 0s
scan_investigation_df['Sum = Fully Scanned?']=(scan_investigation_df.loc[scan_investigation_df['Are there 0s in P1 and P2?'] == True])['Sum of ABS:MIS'] == (scan_investigation_df.loc[scan_investigation_df['Are there 0s in P1 and P2?'] == True])['Fully Scanned']

# # example of where this is not the case

scan_investigation_df_false = scan_investigation_df[scan_investigation_df['Sum = Fully Scanned?'] == False]
print(scan_investigation_df_false.shape)
scan_investigation_df_false['Difference'] = scan_investigation_df_false.loc[:, 'Sum of ABS:MIS'] - scan_investigation_df_false.loc[:, 'Fully Scanned']
print(scan_investigation_df_false.head(2))
print(scan_investigation_df_false['Difference'].mean())
print(scan_investigation_df_false['Difference'].mode())

with pd.ExcelWriter(Detailed_Analysis_Path + "\\" + "RCSR.xlsx") as writer:
    scan_investigation_df.to_excel(writer, sheet_name='All Scans')
    scan_investigation_df_false.to_excel(writer, sheet_name='Scans Not Adding Up')


# full summary statistics by cluster
cluster_description_df = RCSRdf.groupby(['Cluster']).describe()

'''TODO: check #s with a PM and note anything that seems off'''
XXXX = RCSRdf.mask(RCSRdf['Cluster'] == str("XXXX"))
RCSRdf.where(RCSRdf.loc[:,'Cluster'] == "XXXX")