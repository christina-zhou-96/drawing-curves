import pandas as pd

''''
Read from excel file.
Create columns for new df based on 1st row column names.
Create column tests based on the 3rd row-? test df.
Create documentation that puts into notes the 2nd row into the docs.


def project():
    pass
'''
source_path = 'r'
header = 1
source_df = pd.read_excel(source_path,header)

new_df = pd.DataFrame()

