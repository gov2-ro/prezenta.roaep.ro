import pandas as pd
import sqlite3
import os

# Variables
DB_NAME = 'data/_merged/prezenta-alegeri-all.db'
CSV_FILE = 'data/_merged/prezenta-alegeri-all-merged.csv'
# CSV_FILE = 'data/_merged/prezenta-alegeri-first1000.csv'
TMP_TABLE_NAME = 'prezenta_alegeri_tmp'
TARGET_TABLE = 'prezenta-alegeri'
VIEW_NAME = 'prezenta_judete'

# Check if CSV file exists
if not os.path.isfile(CSV_FILE):
    print(f"Error: CSV file '{CSV_FILE}' not found!")
    exit(1)

try:
    # Read CSV into a pandas DataFrame
    df = pd.read_csv(CSV_FILE)

    # Optional: Clean column names (replace spaces with underscores, etc.)
    df.columns = [col.strip().replace(' ', '_').replace('"', '').replace("'", "") for col in df.columns]

    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Write DataFrame to SQLite table
    df.to_sql(TMP_TABLE_NAME, conn, if_exists='replace', index=False)
    print(f"Successfully imported {len(df)} rows into '{TMP_TABLE_NAME}' table.")
    # conn.commit()
    # Post-import SQL Operations

    # 1. Create [prezenta-alegeri-1] with date and time
    create_new_table_sql = f'''
    DROP TABLE IF EXISTS "{TARGET_TABLE}";
    CREATE TABLE "{TARGET_TABLE}" AS
    SELECT alegeri,
        Judet, 
        substr(timestamp, 1, 10) AS date,
        substr(timestamp, 12, 5) AS time,
        SUM(Votanti_lista) AS Votantilista,
        Mediu,
        SUM(Votanti_pe_lista_permanenta) AS Votantipelistapermanenta,
        SUM(Votanti_pe_lista_complementara) AS Votantipelistacomplementara,
        SUM(Înscriși_pe_liste_permanente) AS inscrisi_L_permanente,
        SUM(Înscriși_pe_liste_complementare) AS inscrisi_L_complementare,
        SUM(LP) AS LP,
        SUM(LS) AS LS,
        SUM(LSC) AS LSC,
        SUM(UM) AS UM,
        SUM(LT) AS LT,
        SUM([Barbati_18-24]) as "M_1824",
        SUM([Barbati_25-34]) as "M_2534",
        SUM([Barbati_35-44]) as "M_3544",
        SUM([Barbati_45-64]) as "M_4564",
        SUM([Barbati_65+]) as "M_65+",
        SUM([Femei_18-24]) as "F_1824",
        SUM([Femei_25-34]) as "F_2534",
        SUM([Femei_35-44]) as "F_3544",
        SUM([Femei_45-64]) as "F_4564",
        SUM([Femei_65+]) as "F_65+"
   
    FROM "{TMP_TABLE_NAME}"
    GROUP BY 
        alegeri,
        date,
        time,
        Judet
    ORDER by  
        date,
        time,
        alegeri,
        Judet
        ;
    '''
    cursor.executescript(create_new_table_sql)
    print(f"Table '{TARGET_TABLE}' created successfully.")
    

    # 2. Delete [prezenta-alegeri]
    cursor.execute(f'DROP TABLE "{TMP_TABLE_NAME}";')
    print(f"Table '{TMP_TABLE_NAME}' deleted successfully.")

    # # 3. Create view prezenta_judete based on [prezenta-alegeri-1]
    # create_view_sql = f'''
    # DROP VIEW IF EXISTS "{VIEW_NAME}";
    # CREATE VIEW "{VIEW_NAME}" AS
    # SELECT alegeri,
    #        Judet,
    #     date,
    #     time,
    #      Votantilista,
    #     Mediu,
    #      Votantipelistapermanenta,
    #     inscrisi_L_permanente,
    #     inscrisi_L_complementare,
    #      Votantipelistacomplementara,
    #      LP,
    #      LS,
    #      LSC,
    #      UM,
    #      LT,
    #      "M_1824",
    #      "M_2534",
    #      "M_3544",
    #      "M_4564",
    #      "M_65+",
    #      "F_1824",
    #      "F_2534",
    #      "F_3544",
    #      "F_4564",
    #      "F_65+"
    # FROM "{TARGET_TABLE}"
    # GROUP BY 
    #     alegeri,
    #     date,
    #     time,
    #     Judet  
    # ORDER BY Judet,
    #     date,
    #     time;
    # '''
    # cursor.executescript(create_view_sql)
    # print(f"View '{VIEW_NAME}' created successfully.")
    
    cursor.executescript('VACUUM;')
    print(f"VACUUMed the database")

    # Commit all changes
    conn.commit()

except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()

finally:
    conn.close()
