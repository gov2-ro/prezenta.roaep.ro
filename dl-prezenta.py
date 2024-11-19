
""" 
# TODO: 
-[ ] fetch existing timeslots from website dropdown, or check for available / latest timestamp?
-[ ] accomodate multi-days range (ex locale 21)
-[ ] add logging, already downloaded files
-[ ] add error handling

"""

data_root = "data/"
index_alegeti = 'data/static/prezenta-alegeri-roaep.csv'
alegeri = '2024-euparl'

overwrite = False

# logfile = data_root + alegeri + '/download.log'

import os, requests, logging
# import argparse
import pandas as pd
from datetime import datetime
from tqdm import tqdm

# read csv from external path
df = pd.read_csv(index_alegeti)

#  select row wher id matches alegeri
scrutin = df.loc[df['id'] == alegeri]

data_scrutin = scrutin['ddmmyyyy'].iloc[0]
data_scrutin_ymd = scrutin['yymmdd'].iloc[0]
 


tip_alegeri = scrutin['Tip'].iloc[0]

def setup_logging(destination_dir):
    log_file = os.path.join(destination_dir, 'download.log')
    logging.basicConfig(
        filename=log_file,
        filemode='a',  # Append mode
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Logging initialized.")

def extract_timerange(timerange_str):
    # Split the string by hyphen and strip whitespace
    start_str, end_str = [t.strip() for t in timerange_str.split('-')]
    
    # Parse the times into datetime objects
    time_format = '%H:%M'
    start_time = datetime.strptime(start_str, time_format)
    end_time = datetime.strptime(end_str, time_format)
    
    # Determine min and max times
    min_time = min(start_time, end_time).time()
    max_time = max(start_time, end_time).time()
    
    # Return integer hours
    return min_time.hour, max_time.hour

ore_str = scrutin['ore'].iloc[0]

timerange_start, timerange_end = extract_timerange(ore_str)

judete = ['ab','ag','ar','b','bc','bh','bn','br','bt','bv','bz','cj','cl','cs','ct','cv','db','dj','gj','gl','gr','hd','hr','if','il','is','mh','mm','ms','nt','ot','ph','sb','sj','sm','sv','tl','tm','tr','vl','vn','vs','sr'] # 'sr' for strainatate
# tari=["za","dz","ao","ar","am","au","at","az","be","ba","br","bg","ca","cu","dk","eg","ch","ae","ee","et","ru","ph","fi","fr","ge","de","gr","in","iq","ie","is","il","it","jp","ke","kw","lv","lt","lu","mk","my","mt","ma","mx","me","ng","no","nz","nl","ps","pe","pl","pt","mc","qa","co","kz","sa","jo","gb","al","by","cz","cl","cy","kr","hr","id","ir","pk","lb","md","cn","sk","vn","sn","rs","sg","sy","si","es","lk","us","se","om","tz","th","tn","tr","tm","ua","hu","uy","uz","zw"]
# judete = [] # only download csvs 

xdata_root = data_root + str(data_scrutin) + '-' + tip_alegeri + '/prezenta/'

destination_dir = xdata_root 


os.makedirs(destination_dir, exist_ok=True)
os.makedirs(destination_dir + 'jsons/', exist_ok=True)
os.makedirs(destination_dir + 'csvs/', exist_ok=True)

# ymd_date = datetime.strptime(data_scrutin, '%d%m%Y').strftime('%Y-%m-%d')

ymd_date = datetime.strptime(str(data_scrutin_ymd), '%y%m%d').strftime('%Y-%m-%d')
ymd_date_folder = datetime.strptime(str(data_scrutin_ymd), '%y%m%d').strftime('%d%m%Y')

timerange = ['{:02}'.format(i) for i in range(timerange_start, timerange_end)]
# timerange = ['07', '09', '11', '13', '15', '17', '19', '21', '22']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Chrome/112.0.0.0 Safari/537.36',
    'Referer': f'https://prezenta.roaep.ro/{tip_alegeri}{ymd_date_folder}/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;' \
              'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}


def download_file(url, destination):
    if not overwrite and os.path.exists(destination):
        logging.info(f"SKIPPED: File {destination} already exists and overwrite=False.")
        return 2  # Skipped due to existing file
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(destination, 'wb') as f:
            f.write(response.content)
        logging.info(f"SUCCESS: Downloaded {url} to {destination}")
        return 1  # Success
    except requests.exceptions.RequestException as e:
        logging.error(f"FAILED: Failed to download {url}. Error: {e}")
        return 0  # Failed

""" def download_json(url, filepath): #obsolete?!
    if not os.path.exists(filepath):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            tqdm.write(f"Fișierul {filename} a fost descărcat și salvat.")
            return 1
        else:
            tqdm.write(f"Nu s-a putut descărca fișierul de la URL-ul {url}. Status code: {response.status_code}")
            # response.status_code
            return 0
    else:
        tqdm.write(f"Fișierul {filename} deja există în directorul de destinație.")
        return 2 """

total = len(judete) * len(timerange) + len(timerange)

for judet in tqdm(judete, total=total):
    tqdm.write(f"---- JUDEȚ: {judet} ----")
    for ora in timerange:
        url = f"https://prezenta.roaep.ro/{tip_alegeri}{ymd_date_folder}/data/json/simpv/presence/presence_{judet}_{ymd_date}_{ora}-00.json"
        filename = f"prezenta_{judet}_{ymd_date}_{ora}-00.json"
        filepath = os.path.join(destination_dir + 'jsons/', filename)
        try:
            # dl = download_json(url, filepath)
            dl = download_file(url, filepath)
            if dl == 1:
                tqdm.write(f"-  {filename} [saved]")
            elif dl == 0:
                tqdm.write(f"Nu s-a putut descărca fișierul de la URL-ul {url}")
            elif dl == 2:
                tqdm.write(f"- c {filename} [cached]")
        except Exception as e:
            tqdm.write(f"-E61 Error: {e} -- {url}")
            # continue
            exit(1)

tqdm.write('------------');            
        
for ora in timerange:
    url_cntry = f"https://prezenta.roaep.ro/{tip_alegeri}{ymd_date_folder}/data/csv/simpv/presence_{ymd_date}_{ora}-00.csv"
    
    filename_cntry = f"prezenta_{ymd_date}_{ora}-00.csv"
    filepath_cntry = os.path.join(destination_dir + 'csvs/', filename_cntry)
    try:
        # dl = download_json(url_cntry, filepath_cntry)
        dl = download_file(url_cntry, filepath_cntry)
        if dl == 1:
            tqdm.write(f"Fișierul {filename_cntry} a fost descărcat și salvat.")
        elif dl == 0:
            tqdm.write(f"Nu s-a putut descărca fișierul de la URL-ul {url_cntry}")
        elif dl == 2:
            tqdm.write(f"Fișierul {filename_cntry} deja există în directorul de destinație.")
    except Exception as e:
        tqdm.write(f"-E99 Error: {e}")
        # continue
        exit(1)

tqdm.write("Toate fișierele potențiale au fost verificate.")