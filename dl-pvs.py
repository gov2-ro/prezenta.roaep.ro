tip_alegeri='locale'
# tip_alegeri='europarlamentare'

# diaspora="abroad"

functie_alesi='p'
# functie_alesi='cl'
# functie_alesi='cj'
# functie_alesi='pcj'
# functie_alesi='eup'

# pv_type='temp'
# pv_type='part'
pv_type='final'

# uat_type='uat'
uat_type='cnty'
# uat_type='cntry'

data_scrutin='09062024'

data_root = "data/"
csvs={
    'cnty': 'judete-siruta.csv',
    'uat': 'siruta-cod_jud.csv'
}
csv_cols_jud={
    'cnty': 'Cod',
    'uat': 'Cod'
}

import pandas as pd
import requests, os, argparse
from tqdm import tqdm

base_url = "https://prezenta.roaep.ro/{}{}/data/csv/sicpv/pv_{}_{}_{}_{}.csv" 

parser = argparse.ArgumentParser(description='Download PVs based on specified criteria.')
parser.add_argument('--functie', type=str, help='Function type (e.g., pcj)', default=functie_alesi)
parser.add_argument('--pv-type', type=str, help='PV type (e.g., part)', default=pv_type)
parser.add_argument('--uat', type=str, help='UAT type (e.g., cnty)', default=uat_type)
parser.add_argument('--alegeri', type=str, help='Tip alegeri (e.g., locale, europarlamentare)', default=uat_type)

args = parser.parse_args()

# Use the provided arguments or defaults
functie_alesi = args.functie
pv_type = args.pv_type
uat_type = args.uat
tip_alegeri = args.alegeri

csv_list = data_root + csvs[uat_type]

output_dir = data_root + "pvs/" + functie_alesi + "/" + uat_type + "/" + pv_type + "/"  
log_file = data_root + "logs/PVs-dl-" +  functie_alesi + "-" + uat_type + "-" + pv_type + ".log"
# csv_col_siruta="uat.siruta"
csv_col_jud=csv_cols_jud[uat_type]


df = pd.read_csv(csv_list)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(log_file, 'w') as log:
    for index, row in tqdm(df.iterrows(), total=len(df)):
        url = base_url.format(tip_alegeri, data_scrutin, pv_type, uat_type, functie_alesi, row[csv_col_jud].lower()) 

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