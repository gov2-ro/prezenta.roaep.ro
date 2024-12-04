data_root = "data/"
db = data_root + "_merged/prezenta-alegeri-all.db"
# index_tari = data_root + 'static/countries.csv'
table_name = 'sectii_vot'
table_prezenta = 'prezenta_sv'
runda_alegeri = '2019-prez-1'


""" 
creates sv reference table
looks for one csv file in target folder with the following pattern ????-??-??_??-00.csv
selects distinct
alegeri*, Judet, Localitate, Mediu, Siruta, Nr sectie de votare, Nume sectie de votare
write to db if it doesn't exist

batch: get lista alegeri from db, then look for folders in data/alegeri

*where alegeri == target folder name
diaspora - where judet = SR and read from tari
    
"""

import os, glob, sqlite3, csv
from tqdm import tqdm
import pandas as pd

# Connect to the database
conn = sqlite3.connect(db)
c = conn.cursor()

# Create the table if it doesn't exist
c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (alegeri TEXT, judet TEXT, localitate TEXT, mediu TEXT, siruta TEXT, nr_sectie TEXT, nume_sectie TEXT)")


# get unique alegergi from db table table_prezenta 
c.execute(f"SELECT DISTINCT alegeri FROM {table_prezenta}")
alegeri = c.fetchall()
alegeri = [x[0] for x in alegeri]

# loop for folders
# for runda_alegeri in alegeri:
for runda_alegeri in tqdm(alegeri, desc="Processing Elections", unit="election"):

    
    target_folder = data_root + 'alegeri/' + runda_alegeri
    pattern1 = os.path.join(target_folder, '*????-??-??_??-00.csv')

    csv_files = glob.glob(pattern1)

    if not csv_files:
        tqdm.write("No files found matching the pattern. " + target_folder)
        exit()
    else:
        tqdm.write(f"Found {len(csv_files)} CSV files")
        
    # Read the CSV file
    csv_file = csv_files[0]
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        df = pd.read_csv(csv_file)
        df['alegeri'] = runda_alegeri
        unique_records = df[['alegeri', 'Judet', 'Localitate', 'Mediu', 'Siruta', 'Nr sectie de votare', 'Nume sectie de votare']].drop_duplicates()
        unique_records.to_sql('reference_table', conn, if_exists='replace', index=False) 
        
        for index, row in tqdm(unique_records.iterrows(), total=unique_records.shape[0], desc="Processing CSV rows", unit="file", leave=False):
            alegeri = row['alegeri']
            judet = row['Judet']
            localitate = row['Localitate']
            mediu = row['Mediu']
            siruta = row['Siruta']
            nr_sectie = row['Nr sectie de votare']
            nume_sectie = row['Nume sectie de votare']
            
            c.execute(f"INSERT OR IGNORE INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?)", (alegeri, judet, localitate, mediu, siruta, nr_sectie, nume_sectie))
        
# Commit the changes
conn.commit()
conn.close()
tqdm.write(' -- DONE 👌🏻 --')