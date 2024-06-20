functie_alesi='p'
# functie_alesi='cl'
# functie_alesi='cj'
functie_alesi='pcj'

pv_type='temp'
pv_type='part'
# pv_type='final'

# uat_type='uat'
uat_type='cnty'


data_root = "data/"
csvs={
    'cnty': 'judete-siruta.csv',
    'uat': 'siruta-cod_jud.csv'
}
csv_cols={
    'cnty': 'cc',
    'uat': 'siruta'
}
csv_list = data_root + csvs[uat_type]

output_dir = data_root + "pvs/" + functie_alesi + "/" + uat_type + "/" + pv_type + "/"  
log_file = data_root + "PVs-dl-" +  functie_alesi + "-" + uat_type + "-" + pv_type + ".log"
# csv_col_siruta="uat.siruta"
csv_cols_jud=csv_cols[uat_type]
csv_col_jud="cc" #UATs
csv_col_jud="Cod" #judete


base_url = "https://prezenta.roaep.ro/locale09062024/data/csv/sicpv/pv_{}_{}_{}_{}.csv" 

# output_dir += f"_{functie_alesi}"

import pandas as pd
import requests
import os
from tqdm import tqdm


df = pd.read_csv(csv_list)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(log_file, 'w') as log:
    for index, row in tqdm(df.iterrows(), total=len(df)):
        url = base_url.format(pv_type, uat_type, functie_alesi, row[csv_col_jud].lower()) 

        try:
            response = requests.get(url)
            if response.status_code == 200:
                # file_path = os.path.join(output_dir, f"pv_part_uat_{functie_alesi}_{row[csv_col_jud]}_{row[csv_col_siruta]}.csv") #UATs
                file_path = os.path.join(output_dir, f"pv_{pv_type}_{uat_type}_{functie_alesi}_{row[csv_col_jud]}.csv") #județe
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                log.write(f"Downloaded: {url}\n")
            else:
                log.write(f"Failed: {url} - Status code: {response.status_code}\n")
        except requests.ConnectionError as e:
            log.write(f"Connection error: {url} - Error: {e}\n")
#
print("Done! " + str(len(df)) + " files downloaded to: ", output_dir)