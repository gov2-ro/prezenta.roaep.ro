# append single csv to db, after transformation
# check if exists in the db, if yes, skip
# skip empty rows
# guess country from UAT  

alegeri = '2024-prez-1.1'
data_root = "data/"
db = data_root + "_merged/prezenta-alegeri-all.db"
index_alegeti = data_root + 'static/prezenta-alegeri-roaep.csv'
index_tari = data_root + 'static/countries.csv'
dlog = data_root + "download-log.csv"
data_folder = data_root + 'alegeri/' + alegeri + '/prezenta/csvs'  
table_name = 'prezenta-alegeri'

columns_to_remove_demographics = ['Barbati 18','Barbati 19','Barbati 20','Barbati 21','Barbati 22','Barbati 23','Barbati 24','Barbati 25','Barbati 26','Barbati 27','Barbati 28','Barbati 29','Barbati 30','Barbati 31','Barbati 32','Barbati 33','Barbati 34','Barbati 35','Barbati 36','Barbati 37','Barbati 38','Barbati 39','Barbati 40','Barbati 41','Barbati 42','Barbati 43','Barbati 44','Barbati 45','Barbati 46','Barbati 47','Barbati 48','Barbati 49','Barbati 50','Barbati 51','Barbati 52','Barbati 53','Barbati 54','Barbati 55','Barbati 56','Barbati 57','Barbati 58','Barbati 59','Barbati 60','Barbati 61','Barbati 62','Barbati 63','Barbati 64','Barbati 65','Barbati 66','Barbati 67','Barbati 68','Barbati 69','Barbati 70','Barbati 71','Barbati 72','Barbati 73','Barbati 74','Barbati 75','Barbati 76','Barbati 77','Barbati 78','Barbati 79','Barbati 80','Barbati 81','Barbati 82','Barbati 83','Barbati 84','Barbati 85','Barbati 86','Barbati 87','Barbati 88','Barbati 89','Barbati 90','Barbati 91','Barbati 92','Barbati 93','Barbati 94','Barbati 95','Barbati 96','Barbati 97','Barbati 98','Barbati 99','Barbati 100','Barbati 101','Barbati 102','Barbati 103','Barbati 104','Barbati 105','Barbati 106','Barbati 107','Barbati 108','Barbati 109','Barbati 110','Barbati 111','Barbati 112','Barbati 113','Barbati 114','Barbati 115','Barbati 116','Barbati 117','Barbati 118','Barbati 119','Barbati 120','Femei 18','Femei 19','Femei 20','Femei 21','Femei 22','Femei 23','Femei 24','Femei 25','Femei 26','Femei 27','Femei 28','Femei 29','Femei 30','Femei 31','Femei 32','Femei 33','Femei 34','Femei 35','Femei 36','Femei 37','Femei 38','Femei 39','Femei 40','Femei 41','Femei 42','Femei 43','Femei 44','Femei 45','Femei 46','Femei 47','Femei 48','Femei 49','Femei 50','Femei 51','Femei 52','Femei 53','Femei 54','Femei 55','Femei 56','Femei 57','Femei 58','Femei 59','Femei 60','Femei 61','Femei 62','Femei 63','Femei 64','Femei 65','Femei 66','Femei 67','Femei 68','Femei 69','Femei 70','Femei 71','Femei 72','Femei 73','Femei 74','Femei 75','Femei 76','Femei 77','Femei 78','Femei 79','Femei 80','Femei 81','Femei 82','Femei 83','Femei 84','Femei 85','Femei 86','Femei 87','Femei 88','Femei 89','Femei 90','Femei 91','Femei 92','Femei 93','Femei 94','Femei 95','Femei 96','Femei 97','Femei 98','Femei 99','Femei 100','Femei 101','Femei 102','Femei 103','Femei 104','Femei 105','Femei 106','Femei 107','Femei 108','Femei 109','Femei 110','Femei 111','Femei 112','Femei 113','Femei 114','Femei 115','Femei 116','Femei 117','Femei 118','Femei 119','Femei 120']

import pandas as pd
import glob, os, re, logging, sqlite3

# pattern = os.path.join(data_folder, 'prezenta_????-??-??_??-00.csv')
# csv_files = glob.glob(pattern)

csv_file = 'data/alegeri/2024-prez-1.1/2024-11-23_23-00.csv'

filename = os.path.basename(csv_file)
csvdata = pd.read_csv(csv_file)

# Expected filename format: prezenta_<yyyy>-<mm>-<dd>_<hh>-00.csv
filename = filename.replace('prezenta_', '')
pattern = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])_([01]\d|2[0-3])-00\.csv$')
parts = filename.split('_')


# if len(parts) < 3:
if not pattern.match(filename):
    print(f"Filename {filename} does not match the expected pattern. Skipping.")
    breakpoint()
    exit(1)

csvdata = csvdata.drop(columns=columns_to_remove_demographics, errors='ignore')

date_part = parts[0]  # <yyyy>-<mm>-<dd>
time_part = parts[1].split('-')[0]  # <hh>
timestamp = f"{date_part} {time_part}:00"

csvdata['timestamp'] = timestamp
csvdata['alegeri'] = alegeri
tari = pd.read_csv(index_tari)
# check judet
if 'Judet' in csvdata.columns:
    csvdata['diaspora'] = csvdata['Judet'].apply(lambda x: 1 if x == 'SR' else 0)
    
    # csvdata.loc[csvdata['Judet'] == 'SR', 'diaspora'] += 1

# reaplace tari for judet = SR / diaspora = 1
mask = csvdata['Judet'] == 'SR'
tara_to_alpha2 = dict(zip(tari['tara'], tari['alpha2']))
mapped_alpha2 = csvdata.loc[mask, 'UAT'].map(tara_to_alpha2)
csvdata.loc[mask, 'Judet'] = mapped_alpha2.fillna(csvdata.loc[mask, 'UAT'])
 
# - - - - - - - - - - - - - - - - - - - - -  

desired_columns = ['Votanti pe lista permanenta','Votanti pe lista complementara','Votanti pe lista complementara','Înscriși pe liste permanente','Înscriși pe liste complementare','LP','LS','LSC','UM','LT','LC','Barbati 18-24','Barbati 25-34','Barbati 35-44','Barbati 45-64','Barbati 65+','Femei 18-24','Femei 25-34','Femei 35-44','Femei 45-64','Femei 65+']

# Intersect the desired columns with the existing columns in the dataframe
existing_columns = list(set(desired_columns) & set(csvdata.columns))

# Create a pivot table using only the existing columns
pivot_data = csvdata.pivot_table(
    index=['timestamp', 'alegeri', 'Judet'], 
    values=existing_columns,  # Only include the columns that exist
    aggfunc='sum',  # Aggregation function: sum
    fill_value=0  # Fill missing values with 0
).reset_index()  # Reset index for a clean DataFrame


pivot_data.to_csv('aggregated_judet_data2.csv', index=False, encoding='utf-8')
csvdata.to_csv('csvdata.csv', index=False, encoding='utf-8')

# - - - - - - - - - - - - - - - - - - - - -  
# Append to db

COLUMN_MAPPING = {
    'alegeri': 'alegeri',
    'Judet': 'Judet',
    'Votanti lista': 'Votantilista',
    'Mediu': 'Mediu',
    'Votanti pe lista permanenta': 'Votantipelistapermanenta',
    'Votanti pe lista complementara': 'Votantipelistacomplementara',
    'Înscriși pe liste permanente': 'inscrisi_L_permanente',
    'Înscriși pe liste complementare': 'inscrisi_L_complementare',
    'LP': 'LP',
    'LS': 'LS',
    'LSC': 'LSC',
    'UM': 'UM',
    'LT': 'LT',
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

logging.basicConfig(
    filename='append_to_db.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def append_dataframe_to_sqlite(db_path, table_name, dataframe, if_exists='append'):
    print('appending to db')
    """
    Appends a pandas DataFrame to a SQLite database table.

    Parameters:
    - db_path (str): Path to the SQLite database file.
    - table_name (str): Name of the table to append data to.
    - dataframe (pd.DataFrame): The DataFrame to append.
    - if_exists (str): What to do if the table already exists.
                       Options: 'fail', 'replace', 'append'.
    """
    conn = None  # Initialize conn to None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        logging.info(f"Connected to database at {db_path}.")

        # Append DataFrame to the specified table
        dataframe.to_sql(table_name, conn, if_exists=if_exists, index=False)
        logging.info(f"Successfully appended data to table '{table_name}'.")
        print(f"Successfully appended data to table '{table_name}'.")

    except Exception as e:
        print(f"Error appending data to SQLite database: {e}")
        logging.error(f"Error appending data to SQLite database: {e}")
    finally:
        # Close the database connection if it was opened
        if conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    # Example usage

    
    # Call the function to append the DataFrame
    append_dataframe_to_sqlite(db, table_name, pivot_data)