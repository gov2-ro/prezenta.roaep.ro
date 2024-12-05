file_path = 'data/static/Anexa-2-Situatie-alegatori-pe-sectii-Referendum_25052019.xlsx'

""" 
http://www.roaep.ro/prezentare/wp-content/uploads/2019/05/Anexa-2-Situatie-alegatori-pe-sectii-Referendum_25052019.xlsx
having this table (Anexa-2-Situatie-alegatori-pe-sectii.xlsx) I want to compute
columns "Barbati 18-24","Barbati 25-34","Barbati 35-44","Barbati 45-64","Barbati 65+",
"Femei 18-24","Femei 25-34","Femei 35-44","Femei 45-64","Femei 65+"

where 
"Barbati 18-24" = SUM(vb18, vb19, vb20, vb21, vb22, vb23, vb24)
....
"Femei 65+" = SUM(vf65, vf66, ..., vf99, vf100plus)
"""

import pandas as pd

# Load the Excel file

data = pd.ExcelFile(file_path)

# Load the relevant sheet into a DataFrame
sheet_name = 'situatie_alegatori pe sectie re'
df = data.parse(sheet_name)

# Compute the new columns for Barbati and Femei based on the specified ranges

# Barbati
df['Barbati 18-24'] = df[['vb18', 'vb19', 'vb20', 'vb21', 'vb22', 'vb23', 'vb24']].sum(axis=1)
df['Barbati 25-34'] = df[['vb25', 'vb26', 'vb27', 'vb28', 'vb29', 'vb30', 'vb31', 'vb32', 'vb33', 'vb34']].sum(axis=1)
df['Barbati 35-44'] = df[['vb35', 'vb36', 'vb37', 'vb38', 'vb39', 'vb40', 'vb41', 'vb42', 'vb43', 'vb44']].sum(axis=1)
df['Barbati 45-64'] = df[[f'vb{x}' for x in range(45, 65)]].sum(axis=1)
df['Barbati 65+'] = df[[f'vb{x}' for x in range(65, 100)] + ['vb100plus']].sum(axis=1)

# Femei
df['Femei 18-24'] = df[['vf18', 'vf19', 'vf20', 'vf21', 'vf22', 'vf23', 'vf24']].sum(axis=1)
df['Femei 25-34'] = df[['vf25', 'vf26', 'vf27', 'vf28', 'vf29', 'vf30', 'vf31', 'vf32', 'vf33', 'vf34']].sum(axis=1)
df['Femei 35-44'] = df[['vf35', 'vf36', 'vf37', 'vf38', 'vf39', 'vf40', 'vf41', 'vf42', 'vf43', 'vf44']].sum(axis=1)
df['Femei 45-64'] = df[[f'vf{x}' for x in range(45, 65)]].sum(axis=1)
df['Femei 65+'] = df[[f'vf{x}' for x in range(65, 100)] + ['vf100plus']].sum(axis=1)

# Select relevant columns to display
computed_columns = [
    'Barbati 18-24', 'Barbati 25-34', 'Barbati 35-44', 'Barbati 45-64', 'Barbati 65+',
    'Femei 18-24', 'Femei 25-34', 'Femei 35-44', 'Femei 45-64', 'Femei 65+'
]
result_df = df[computed_columns]

columns_to_remove = [col for col in df.columns if col.startswith('vb') or col.startswith('vf')]
df = df.drop(columns=columns_to_remove)

df.to_csv('data/static/demographics-ranges.csv', index=False)
print("Updated dataset with aggregated columns and without vb*/vf* has been saved to 'demographics_with_aggregated_columns.csv'.")
 