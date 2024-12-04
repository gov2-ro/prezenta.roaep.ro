 
data_root = "data/"
db = data_root + "_merged/prezenta-alegeri-all.db"
index_tari = data_root + 'static/countries.csv'
table_name = 'prezenta_sv'

""" 
# TODOs
- [x] unpivot data
- [x] drop tables with LT = 0
- [x] column synonims
- [x] better/faster check if exists
- [ ] add Localitate - remove closing number, if any
- [ ] create reference tables - external script
- [ ] debugging level

Înscriși pe liste permanente = Votanti lista = Votanti pe lista permanenta
Înscriși pe liste complementare = Votanti pe lista complementara

"""

import pandas as pd
import glob, os, re, logging, sqlite3, argparse, logging

def create_table_if_not_exists(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    create_table_sql = f'''
    CREATE TABLE IF NOT EXISTS "{table_name}" (
      timestamp TEXT,
      alegeri TEXT,      
      diaspora INTEGER,
      Judet TEXT,
      Localitate TEXT,
      Siruta INTEGER,
      Mediu TEXT,
      Nrsectiedevotare INTEGER,      
      inscrisi_L_permanente INTEGER,
      inscrisi_L_complementare INTEGER,
      LP INTEGER,
      LS INTEGER,
      LSC INTEGER,
      UM INTEGER,
      LT INTEGER,
      M_1824 INTEGER,
      M_2534 INTEGER,
      M_3544 INTEGER,
      M_4564 INTEGER,
      "M_65+" INTEGER,
      F_1824 INTEGER,
      F_2534 INTEGER,
      F_3544 INTEGER,
      F_4564 INTEGER,
      "F_65+" INTEGER
    );
    '''

    try:
        # print(f"Table '{table_name}' is ready.")
        cursor.execute(create_table_sql)
    except Exception as e:
        print(f"E53 Error creating table '{table_name}': {e}")
    finally:
        
        conn.commit()
        cursor.close()
        conn.close()

def create_tracking_table(db_path):
    """Create table to track processed CSV files"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    create_sql = '''
    CREATE TABLE IF NOT EXISTS "processed_files" (
        filename TEXT,
        folder TEXT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (filename, folder)
    );
    '''
    
    cursor.execute(create_sql)
    conn.commit()
    conn.close()

def file_was_processed(db_path, filename, folder):
    """Check if CSV file was already processed"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    check_sql = '''
    SELECT 1 FROM "processed_files"
    WHERE filename = ? AND folder = ?
    LIMIT 1
    '''
    
    cursor.execute(check_sql, (filename, folder))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

def mark_file_processed(db_path, filename, folder, timestamp):
    """Mark CSV file as processed"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    insert_sql = '''
    INSERT INTO "processed_files" (filename, folder)
    VALUES (?, ?)
    '''
    
    cursor.execute(insert_sql, (filename, folder))
    conn.commit()
    conn.close()

def process_csv(csv_file, alegeri, db, index_tari, columns_to_remove_demographics, table_name, COLUMN_MAPPING):
    
    create_tracking_table(db)
    
    # Get filename and parent folder
    filename = os.path.basename(csv_file)
    folder = os.path.basename(os.path.dirname(csv_file))
    
    # Check if file was already processed
    if file_was_processed(db, filename, folder):
        logging.info(f"File {filename} from folder {folder} was already processed. Skipping.")
        return
    
    # Read the CSV file
    csvdata = pd.read_csv(csv_file)

    # Intersect the desired columns with the existing columns in the dataframe
    desired_columns = ['Siruta','Nr sectie de votare', 'Mediu','Judet','alegeri','Judet', 'timestamp', 'Localitate',
        'diaspora', 'Votanti pe lista permanenta', 'Votanti pe lista complementara', 'Votanti pe lista speciala',
        'Înscriși pe liste permanente', 'Înscriși pe liste complementare', 'LP', 'LS', 'LSC', 'UM', 'LT', 'LC',
        'Barbati 18-24', 'Barbati 25-34', 'Barbati 35-44', 'Barbati 45-64', 'Barbati 65+',
        'Femei 18-24', 'Femei 25-34', 'Femei 35-44', 'Femei 45-64', 'Femei 65+'
    ]
    existing_columns = list(set(desired_columns) & set(csvdata.columns))
    
    filename = os.path.basename(csv_file)
    filename = filename.replace('prezenta_', '')
    parts = filename.split('_')

    csvdata = csvdata.drop(columns=columns_to_remove_demographics, errors='ignore')

    date_part = parts[0]  # <yyyy>-<mm>-<dd>
    time_part = parts[1].split('-')[0]  # <hh>
    timestamp = f"{date_part} {time_part}:00"
    csvdata['timestamp'] = timestamp
    csvdata['alegeri'] = alegeri
    tari = pd.read_csv(index_tari)
    
    # if Localitate ends with a number, remove it
    csvdata['Localitate'] = csvdata['Localitate'].str.replace(r'\d+$', '', regex=True)
    
    if 'Judet' in csvdata.columns:
        csvdata['diaspora'] = csvdata['Judet'].apply(lambda x: 1 if x == 'SR' else 0)
    else:
        csvdata['diaspora'] = 0  # Default value if Judet column doesn't exist
    
    # Get existing columns for pivot
    mask = csvdata['Judet'] == 'SR'
    tara_to_alpha2 = dict(zip(tari['tara'], tari['alpha2']))
    mapped_alpha2 = csvdata.loc[mask, 'UAT'].map(tara_to_alpha2)
    csvdata.loc[mask, 'Judet'] = mapped_alpha2.fillna(csvdata.loc[mask, 'UAT'])
    existing_columns = list(set(desired_columns) & set(csvdata.columns))
    
    # remove rows from csvdata where LT = 0
    csvdata = csvdata[csvdata['LT'] != 0]
    
    # keep only the columns that are in the desired_columns list
    csvdata = csvdata[existing_columns]
    
    # breakpoint()
    create_table_if_not_exists(db_path=db, table_name=table_name)
    
    if csvdata.empty:
        logging.info(f"Data for {timestamp} already exists in the database for the given 'alegeri' and 'Judet'. Skipping.")
    else:
        append_to_db(db, table_name, csvdata, COLUMN_MAPPING)
        mark_file_processed(db, filename, folder, timestamp)
        
    
    # TODO: check if data already exists in the database for the given 'alegeri', 'Judet', 'timestamp' and 'diaspora' 

    """
    Check if a row exists with the given criteria
    """
    cursor = conn.cursor()
    
    check_sql = f'''
    SELECT 1 FROM "{table_name}" 
    WHERE timestamp = ? 
    AND Judet = ?
    AND diaspora = ?
    AND Nrsectiedevotare = ?
    LIMIT 1
    '''
    
    cursor.execute(check_sql, (timestamp, judet, diaspora, nrsectiedevotare))
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists

def append_to_db(db_path, table_name, dataframe, COLUMN_MAPPING):


    # Apply column mapping
    dataframe.rename(columns=COLUMN_MAPPING, inplace=True)

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?;', (table_name,))
    table_exists = cursor.fetchone()

    if not table_exists:
        logging.info(f"Table '{table_name}' does not exist in the database.")
        conn.close()
        return
 

    # Iterate over DataFrame rows
    for index, row in dataframe.iterrows():
        alegeri = str(row.get('alegeri', '')).strip()
        Judet = str(row.get('Judet', '')).strip()
        timestamp = str(row.get('timestamp', '')).strip()
        Nrsectiedevotare = str(row.get('Nrsectiedevotare', '')).strip()
        diaspora = str(row.get('diaspora', '')).strip()

        # Prepare columns and values
        columns = ', '.join([f'"{col}"' for col in dataframe.columns])
        placeholders = ', '.join(['?'] * len(dataframe.columns))
        sql = f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders})'
        values = tuple(row[col] for col in dataframe.columns)

        # Insert the record
        try:
            cursor.execute(sql, values)
            logging.info(f"Inserted row {index} into the database.")
        except Exception as e:
            logging.error(f"Error inserting row {index}: {e}")
            conn.close()
            return

    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Data appended to the database successfully.")

create_table_if_not_exists(db_path=db, table_name=table_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and append CSV data to the database.')
    parser.add_argument('csv_file', help='Path to the CSV file to process.')
    parser.add_argument('alegeri', help='id alegeri, ex: 2024-prez-1')
    args = parser.parse_args()
    alegeri= args.alegeri

    columns_to_remove_demographics = ['Barbati 18','Barbati 19','Barbati 20','Barbati 21','Barbati 22','Barbati 23','Barbati 24','Barbati 25','Barbati 26','Barbati 27','Barbati 28','Barbati 29','Barbati 30','Barbati 31','Barbati 32','Barbati 33','Barbati 34','Barbati 35','Barbati 36','Barbati 37','Barbati 38','Barbati 39','Barbati 40','Barbati 41','Barbati 42','Barbati 43','Barbati 44','Barbati 45','Barbati 46','Barbati 47','Barbati 48','Barbati 49','Barbati 50','Barbati 51','Barbati 52','Barbati 53','Barbati 54','Barbati 55','Barbati 56','Barbati 57','Barbati 58','Barbati 59','Barbati 60','Barbati 61','Barbati 62','Barbati 63','Barbati 64','Barbati 65','Barbati 66','Barbati 67','Barbati 68','Barbati 69','Barbati 70','Barbati 71','Barbati 72','Barbati 73','Barbati 74','Barbati 75','Barbati 76','Barbati 77','Barbati 78','Barbati 79','Barbati 80','Barbati 81','Barbati 82','Barbati 83','Barbati 84','Barbati 85','Barbati 86','Barbati 87','Barbati 88','Barbati 89','Barbati 90','Barbati 91','Barbati 92','Barbati 93','Barbati 94','Barbati 95','Barbati 96','Barbati 97','Barbati 98','Barbati 99','Barbati 100','Barbati 101','Barbati 102','Barbati 103','Barbati 104','Barbati 105','Barbati 106','Barbati 107','Barbati 108','Barbati 109','Barbati 110','Barbati 111','Barbati 112','Barbati 113','Barbati 114','Barbati 115','Barbati 116','Barbati 117','Barbati 118','Barbati 119','Barbati 120','Femei 18','Femei 19','Femei 20','Femei 21','Femei 22','Femei 23','Femei 24','Femei 25','Femei 26','Femei 27','Femei 28','Femei 29','Femei 30','Femei 31','Femei 32','Femei 33','Femei 34','Femei 35','Femei 36','Femei 37','Femei 38','Femei 39','Femei 40','Femei 41','Femei 42','Femei 43','Femei 44','Femei 45','Femei 46','Femei 47','Femei 48','Femei 49','Femei 50','Femei 51','Femei 52','Femei 53','Femei 54','Femei 55','Femei 56','Femei 57','Femei 58','Femei 59','Femei 60','Femei 61','Femei 62','Femei 63','Femei 64','Femei 65','Femei 66','Femei 67','Femei 68','Femei 69','Femei 70','Femei 71','Femei 72','Femei 73','Femei 74','Femei 75','Femei 76','Femei 77','Femei 78','Femei 79','Femei 80','Femei 81','Femei 82','Femei 83','Femei 84','Femei 85','Femei 86','Femei 87','Femei 88','Femei 89','Femei 90','Femei 91','Femei 92','Femei 93','Femei 94','Femei 95','Femei 96','Femei 97','Femei 98','Femei 99','Femei 100','Femei 101','Femei 102','Femei 103','Femei 104','Femei 105','Femei 106','Femei 107','Femei 108','Femei 109','Femei 110','Femei 111','Femei 112','Femei 113','Femei 114','Femei 115','Femei 116','Femei 117','Femei 118','Femei 119','Femei 120']

    COLUMN_MAPPING = {
        'alegeri': 'alegeri',
        'Judet': 'Judet',
        'Mediu': 'Mediu',
        'Localitate': 'Localitate',
        'timestamp': 'timestamp',
        'Nr sectie de votare': 'Nrsectiedevotare',
        'Votanti pe lista permanenta': 'inscrisi_L_permanente',
        'Votanti pe lista complementara': 'inscrisi_L_complementare',
        'Votanti pe lista speciala': 'Votantipelistaspeciala',
        'Înscriși pe liste permanente': 'inscrisi_L_permanente',
        'Înscriși pe liste complementare': 'inscrisi_L_complementare',
        'LP': 'LP',
        'LS': 'LS',
        'LSC': 'LSC',
        'UM': 'UM',
        'LT': 'LT',
        'LC': 'LC',
        'Barbati 18-24': 'M_1824',
        'Barbati 25-34': 'M_2534',
        'Barbati 35-44': 'M_3544',
        'Barbati 45-64': 'M_4564',
        'Barbati 65+': 'M_65+',
        'Femei 18-24': 'F_1824',
        'Femei 25-34': 'F_2534',
        'Femei 35-44': 'F_3544',
        'Femei 45-64': 'F_4564',
        'Femei 65+': 'F_65+',
    }

    # Configure logging
    logging.basicConfig(
        filename=data_root + '/alegeri' + alegeri + '-append_to_db.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Call the processing function
    process_csv(args.csv_file, alegeri, db, index_tari, columns_to_remove_demographics, table_name, COLUMN_MAPPING)
