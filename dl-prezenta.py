
""" 
# TODO: 
-[ ] fetch existing timeslots from website dropdown, or check for available / latest timestamp?
-[ ] accomodate multi-days range (ex locale 21)
-[ ] add logging, already downloaded files
-[ ] add error handling

"""

alegeri = '2020-parl'

data_root = "data/"
index_alegeti = 'data/static/prezenta-alegeri-roaep.csv'
overwrite = False

judete = ['ab','ag','ar','b','bc','bh','bn','br','bt','bv','bz','cj','cl','cs','ct','cv','db','dj','gj','gl','gr','hd','hr','if','il','is','mh','mm','ms','nt','ot','ph','sb','sj','sm','sv','tl','tm','tr','vl','vn','vs','sr'] # 'sr' for strainatate
# judete = [] # only download csvs 


""" 
['2024-local-3', '2024-local-2', '2024-euparl', '2024-local', '2024-refloc', '2022-refloc', '2021-refloc-4', '2021-refloc-3', '2021-refloc-2', '2021-refloc-1', '2021-local-2', '2021-local-1', '2020-parl', '2019-prez-1', '2019-prez-1', '2020-local-2', '2020-local', '2019-ref', '2019-euparl', '2016-parl']
"""

domain_pattern = {
'prezenta.roaep.ro':  {'json': '/data/json/simpv/presence/presence_','csv': '/data/csv/simpv/presence_'},
'prezenta.bec.ro': {'json': '/data/presence/json/presence_','csv': '/data/presence/csv/presence_'}}

scrutin_pattern = {
'locale07072024':{          'id':'2024-local-3', 'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'locale23062024':{          'id':'2024-local-2', 'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'europarlamentare09062024':{'id':'2024-euparl',  'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'locale09062024':{          'id':'2024-local',   'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'referendum26052024':{      'id':'2024-refloc',  'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'referendum19062022':{      'id':'2022-refloc',  'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'referendum26092021_3':{    'id':'2021-refloc-4','json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'referendum26092021_2':{    'id':'2021-refloc-3','json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'referendum26092021_1':{    'id':'2021-refloc-2','json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'referendum15082021':{      'id':'2021-refloc-1','json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'locale27062021':{          'id':'2021-local-2' ,'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'locale24012021':{          'id':'2021-local-1' ,'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'parlamentare06122020':{    'id':'2020-parl',    'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'prezidentiale24112019':{   'id':'2019-prez-2',  'json':'/data/presence/json/presence_',       'csv':'/data/presence/csv/presence_', 'platform': 'prezenta.bec.ro'},
'prezidentiale10112019':{   'id':'2019-prez-1',  'json':'/data/presence/json/presence_',       'csv':'/data/presence/csv/presence_', 'platform': 'prezenta.bec.ro'},
'locale11102020':{          'id':'2020-local-2', 'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'locale27092020':{          'id':'2020-local',   'json':'/data/json/simpv/presence/presence_', 'csv':'/data/csv/simpv/presence_',    'platform': 'prezenta.aep.ro'},
'referendum26052019':{      'id':'2019-ref',     'json':'/data/presence/json/presence_',       'csv':'/data/presence/csv/presence_', 'platform': 'prezenta.bec.ro'},
'europarlamentare26052019':{'id':'2019-euparl',  'json':'/data/presence/json/presence_',       'csv':'/data/presence/csv/presence_', 'platform': 'prezenta.bec.ro'},
'parlamentare2016':{        'id':'2016-parl',    'json':'/json/presence_',            'csv':'/csv/presence_',      'platform': 'prezenta.bec.ro'}
} 


 
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
baseurl = scrutin['url'].iloc[0]
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

xdata_root = data_root + str(data_scrutin) + '-' + alegeri + '/prezenta/'

destination_dir = xdata_root 

os.makedirs(destination_dir, exist_ok=True)
os.makedirs(destination_dir + 'jsons/', exist_ok=True)
os.makedirs(destination_dir + 'csvs/', exist_ok=True)

setup_logging(destination_dir)

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
 

total = len(judete) * len(timerange) + len(timerange)
logging.info(f"found {len(judete)} judete, {len(timerange)} timeslots")

tqdm.write('----- JUDEȚE -----');

# extract domain from baseurl
platform1 = baseurl.split('/')[2] #domain
platform2 = baseurl.split('/')[3] #slug-alegeri



for judet in tqdm(judete, total=len(judete)):
    tqdm.write(f"---- JUDEȚ: {judet} ----")
    for ora in timerange:
        # url = f"https://prezenta.roaep.ro/{tip_alegeri}{ymd_date_folder}/data/json/simpv/presence/presence_{judet}_{ymd_date}_{ora}-00.json"
        # url = f"{baseurl}/data/json/simpv/presence/presence_{judet}_{ymd_date}_{ora}-00.json"
        if platform1 == 'prezenta.bec.ro':
            # capitalize judet for BEC
            judet = judet.upper()
        # url = f"{baseurl}{domain_pattern[platform]['json']}{judet}_{ymd_date}_{ora}-00.json"
        url = f"{baseurl}{scrutin_pattern[platform2]['json']}{judet}_{ymd_date}_{ora}-00.json"
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

tqdm.write('----- CSVS -----');            
        
for ora in timerange:
    # url_cntry = f"{baseurl}/data/csv/simpv/presence_{ymd_date}_{ora}-00.csv"
    # url_cntry = f"{baseurl}{domain_pattern[platform]['csv']}{ymd_date}_{ora}-00.csv"
    url_cntry = f"{baseurl}{scrutin_pattern[platform2]['csv']}{ymd_date}_{ora}-00.csv"
    
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