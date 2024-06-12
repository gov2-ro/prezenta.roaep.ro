csv_list='data/siruta-cod_jud.csv'
output_dir = "data/pvs"
log_file = "data/pv-dl.log"
csv_col_siruta="uat.siruta"
csv_col_jud="cc"
# functie_aleasa='p'
functie_aleasa='cl'

output_dir += f"_{functie_aleasa}"

import pandas as pd
import requests
import os
from tqdm import tqdm


base_url = "https://prezenta.roaep.ro/locale09062024/data/csv/sicpv/pv_part_uat_{}_{}_{}.csv"


df = pd.read_csv(csv_list)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(log_file, 'w') as log:
    for index, row in tqdm(df.iterrows(), total=len(df)):
        url = base_url.format(functie_aleasa, row[csv_col_jud], row[csv_col_siruta])
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = os.path.join(output_dir, f"pv_part_uat_p_{row[csv_col_jud]}_{row[csv_col_siruta]}.csv")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                log.write(f"Downloaded: {url}\n")
            else:
                log.write(f"Failed: {url} - Status code: {response.status_code}\n")
        except requests.ConnectionError as e:
            log.write(f"Connection error: {url} - Error: {e}\n")
