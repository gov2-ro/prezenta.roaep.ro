tip_alegeri='locale'
# tip_alegeri='europarlamentare'

# data_scrutin='27092020'    # locale tur 1
# data_scrutin='11102020'    # locale tur 2 # FIXME: not working?!
# data_scrutin='27062021'    # locale parțiale
data_scrutin='09062024'      # euro + locale
timerange_start=19
timerange_end=22

# TODO: fetch existing timeslots from website dropdown, or check for latest timestamp?
# TODO: accomodate multi-days range (ex locale 21)

timerange = ['{:02}'.format(i) for i in range(timerange_start, timerange_end)]
timerange = ['07', '09', '11', '13', '15', '17', '19', '21', '22']


import os, requests
# import pandas as pd
from datetime import datetime

judete = ['ab','ag','ar','b','bc','bh','bn','br','bt','bv','bz','cj','cl','cs','ct','cv','db','dj','gj','gl','gr','hd','hr','if','il','is','mh','mm','ms','nt','ot','ph','sb','sj','sm','sv','tl','tm','tr','vl','vn','vs']
judete = [] # only download csvs 


data_root='data/' + data_scrutin + '/prezenta/' 

destination_dir = data_root 

os.makedirs(destination_dir + 'jsons/', exist_ok=True)
os.makedirs(destination_dir + 'csvs/', exist_ok=True)

ymd_date = datetime.strptime(data_scrutin, '%d%m%Y').strftime('%Y-%m-%d')

def download_json(url, filepath):
    if not os.path.exists(filepath):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            # print(f"Fișierul {filename} a fost descărcat și salvat.")
            return 1
        else:
            # print(f"Nu s-a putut descărca fișierul de la URL-ul {url}. Status code: {response.status_code}")
            # response.status_code
            return 0
    else:
        # print(f"Fișierul {filename} deja există în directorul de destinație.")
        return 2


for judet in judete:
    for ora in timerange:
        # https://prezenta.roaep.ro/locale09062024//data/csv/simpv/presence_2024-06-09_22-00.csv
        # https://prezenta.roaep.ro/locale09062024/data/json/simpv/presence/activity_ag.json
        # https://prezenta.roaep.ro/locale09062024/data/json/simpv/presence/presence_ag_2024-06-09_22-00.json
        url = f"https://prezenta.roaep.ro/{tip_alegeri}{data_scrutin}/data/json/simpv/presence/presence_{judet}_{ymd_date}_{ora}-00.json"
        filename = f"prezenta_{judet}_{ymd_date}_{ora}-00.json"
        filepath = os.path.join(destination_dir + 'jsons/', filename)
        try:
            dl = download_json(url, filepath)
            if dl == 1:
                print(f"Fișierul {filename} a fost descărcat și salvat.")
            elif dl == 0:
                print(f"Nu s-a putut descărca fișierul de la URL-ul {url}")
            elif dl == 2:
                print(f"Fișierul {filename} deja există în directorul de destinație.")
        except Exception as e:
            print(f"-E61 Error: {e}")
            # continue
            exit(1)
            
        
for ora in timerange:
    url_cntry = f"https://prezenta.roaep.ro/{tip_alegeri}{data_scrutin}/data/csv/simpv/presence_{ymd_date}_{ora}-00.csv"
    # https://prezenta.roaep.ro/locale09062024/data/csv/simpv/presence_2024-06-09_22-00.csv
    # print(url_cntry)
    # exit()
    filename_cntry = f"prezenta_{ymd_date}_{ora}-00.csv"
    filepath_cntry = os.path.join(destination_dir + 'csvs/', filename_cntry)
    try:
        dl = download_json(url_cntry, filepath_cntry)
        if dl == 1:
            print(f"Fișierul {filename_cntry} a fost descărcat și salvat.")
        elif dl == 0:
            print(f"Nu s-a putut descărca fișierul de la URL-ul {url_cntry}")
        elif dl == 2:
            print(f"Fișierul {filename_cntry} deja există în directorul de destinație.")
    except Exception as e:
        print(f"-E99 Error: {e}")
        # continue
        exit(1)

print("Toate fișierele potențiale au fost verificate.")