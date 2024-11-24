""" 
tip_alegeri='locale'
functie_alesi='p'
uat_type='judet'


pv_type='final'
data_scrutin='09062024'      # euro + locale

data_root = "data/" + data_scrutin + '-' + tip_alegeri + '/pvs/'

uatx={
    # 'sectie': 'sv',
    'judet': 'cnty',
    'tara': 'cntry',
}

xlsx_file = data_root + 'merged-' + functie_alesi + '-' + uatx[uat_type] + '-' + pv_type + '.xlsx'
sqlite_db = data_root + 'merged-' + functie_alesi + '-' + uatx[uat_type] + '-' + pv_type + '.db'
 """

import pandas as pd
import sqlite3, sys

xlsx_file = sys.argv[1]
sqlite_db = sys.argv[2]

def xlsx_to_sqlite(xlsx_file, sqlite_db):
    # Load the Excel file
    excel_data = pd.ExcelFile(xlsx_file)
    
    # Connect to the SQLite database (it will create one if it doesn't exist)
    conn = sqlite3.connect(sqlite_db)
    
    for sheet_name in excel_data.sheet_names:
        # Read each sheet into a DataFrame
        df = excel_data.parse(sheet_name)
        
        # Convert the DataFrame to a SQL table
        df.to_sql(sheet_name, conn, if_exists='replace', index=False)
        
        print(f'Sheet {sheet_name} has been written to the database {sqlite_db}.')

    # Close the database connection
    conn.close()
    print(f'Conversion complete. The data is stored in {sqlite_db}.')

xlsx_to_sqlite(xlsx_file, sqlite_db)
