csv_list='data/siruta-cod_jud.csv' #UATs
csv_list='data/judete-siruta.csv' #județe
output_dir = "data/pvs/jud/p"
log_file = "data/pv-dl2jud.log"
# csv_col_siruta="uat.siruta"
csv_col_jud="cc" #UATs
csv_col_jud="Cod" #judete
functie_aleasa='p'
# functie_aleasa='cl'

# base_url = "https://prezenta.roaep.ro/locale09062024/data/csv/sicpv/pv_part_uat_{}_{}_{}.csv" #uats
base_url = "https://prezenta.roaep.ro/locale09062024/data/csv/sicpv/pv_part_cnty_{}_{}.csv" #județe

output_dir += f"_{functie_aleasa}"

import pandas as pd
import requests
import os
from tqdm import tqdm


df = pd.read_csv(csv_list)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(log_file, 'w') as log:
    for index, row in tqdm(df.iterrows(), total=len(df)):
        # url = base_url.format(functie_aleasa, row[csv_col_jud], row[csv_col_siruta]) #UATs
        url = base_url.format(functie_aleasa, row[csv_col_jud]) #județe
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # file_path = os.path.join(output_dir, f"pv_part_uat_{functie_aleasa}_{row[csv_col_jud]}_{row[csv_col_siruta]}.csv") #UATs
                file_path = os.path.join(output_dir, f"pv_part_uat_{functie_aleasa}_{row[csv_col_jud]}.csv") #județe
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                log.write(f"Downloaded: {url}\n")
            else:
                log.write(f"Failed: {url} - Status code: {response.status_code}\n")
        except requests.ConnectionError as e:
            log.write(f"Connection error: {url} - Error: {e}\n")
