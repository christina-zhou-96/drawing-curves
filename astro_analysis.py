import pandas as pd
import numpy as np


path = r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\MVPs\astro\Data Source\virgo libra.xlsx'
source = pd.read_excel(path)

# test_path=r'\\es04cifs00\users$\czhou2\Winnt\System\Desktop\MVPs\astro\Test\Data Source\virgo libra.xlsx'
# source = pd.read_excel(test_path)

df = pd.DataFrame(columns=['Avg'], index=['Libra','Virgo'])

virgo = source[source['BIRTH_DTE'] < 19961001]
virgo['index'] = 'Virgo'
virgo.set_index('index',inplace=True)
libra = source[source['BIRTH_DTE'] > 19961001]
libra['index'] = 'Libra'
libra.set_index('index',inplace=True)

virgo = virgo.replace(['ABS','INV'],0).dropna()
virgo['FINAL_SCORE'] = virgo['FINAL_SCORE'].astype(int)
virgo_avg = virgo['FINAL_SCORE'].mean()

libra = libra.replace(['ABS','INV'],0).dropna()
libra['FINAL_SCORE'] = libra['FINAL_SCORE'].astype(int)
libra_avg = libra['FINAL_SCORE'].mean()

df['Avg'] = [virgo_avg,libra_avg]
