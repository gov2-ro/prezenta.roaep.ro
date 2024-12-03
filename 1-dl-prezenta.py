""" 
- reads hours.json
- checks if any new csvs, if yes, add to db
- drops unwanted columns, adds timestamp and alegeri columns and adds to the db
- also add tara diaspora
"""

alegeri = '2024-prez-1'
# alegeri = '2024-parl'

data_root = "data/"
db = data_root + "alegeri/_merged/prezenta-alegeri-judete.db"
index_alegeti = data_root + 'static/prezenta-alegeri-roaep.csv'
dlog = data_root + "download-log.csv"


app_pattern = {
'aep':  {'json': 'data/json/simpv/presence','csv': '/data/csv/simpv/presence_'},
'bec1': {'json': 'data/presence/json','csv': '/data/presence/csv/presence_'},
'bec0': {'json': 'json','csv': '/csv/presence_'}
}


import os, requests, logging
# import argparse
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                  'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                  'Chrome/112.0.0.0 Safari/537.36',
    'Referer': f'https://prezenta.roaep.ro/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;' \
              'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

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

setup_logging(data_root)

def download_file(url, destination, overwrite = False, logfile = ''):
    # download file, write to logs (2), overwrites or not, returns 0, 1, 2
    if (not logfile or logfile == ''):
        # get 2 directories up
        logfile = os.path.join(os.path.dirname(os.path.dirname(destination)), 'download.log')
        # logfile = destination + 'download.log'
    if not overwrite and os.path.exists(destination):
        logging.info(f"SKIPPED: File {destination} already exists and overwrite=False.")
        return 2  # Skipped due to existing file
    # check if url exists in logfile, it yes, skip
    if os.path.exists(logfile):
        with open(logfile, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if url in line:
                    logging.info(f"SKIPPED: URL {url} found in dl log")
                    print(f"SKIPPED: URL {url} found in dl log")
                    return 2  # Skipped due to existing file
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        response_status = response.status_code
        with open(destination, 'wb') as f:
            f.write(response.content)
            # get filesize
            filesize = os.path.getsize(destination)
        logging.info(f"SUCCESS: Downloaded {url} to {destination}")
        # write to download log, add reponse header
        with open(logfile, 'a') as f:
            # f.write(f"{datetime.now()},{url}\n")
            f.write(f"{datetime.now()},{url},{response_status},{round(int(response.headers['Content-Length'])/1000)}, {round(filesize/1048576),1}\n")
            # print('written to log ' + logfile)
        return 1  # Success
    except requests.exceptions.RequestException as e:
        logging.error(f"FAILED: Failed to download {url}. Error: {e}")
        return 0  # Failed

df = pd.read_csv(index_alegeti)

scrutin = df.loc[df['id'] == alegeri]
data_scrutin = scrutin['ddmmyyyy'].iloc[0]
data_scrutin_ymd = scrutin['yymmdd'].iloc[0]
baseurl = scrutin['url'].iloc[0]
tip_alegeri = scrutin['Tip'].iloc[0]
app_version = scrutin['app-version'].iloc[0]

hours_json_url = baseurl + app_pattern[app_version]['json'] + '/hours.json'

try:
    response = requests.get(hours_json_url, headers=headers, timeout=10)
    response.raise_for_status()
    hours_json = response.json()
    logging.info("Successfully fetched hours_json.")

except requests.exceptions.RequestException as e:
    print('failed getting hours' )
    print(e)
    breakpoint
    exit(1)
    logging.error(f"Failed to fetch hours_json: {e}")


os.makedirs(data_root + alegeri, exist_ok=True)
for node in hours_json:
    # check if file exists
    csvurl = baseurl + app_pattern[app_version]['csv'] + node['key'] + '.csv'
    zifile = data_root + 'alegeri/' + alegeri + '/' + node['key'] + '.csv'
    # get the zifile from the url
    filename = csvurl.split('/')[-1]
    if filename == 'now.csv':
        continue
    dl = download_file(csvurl, zifile, False, dlog)
    if dl == 1:
        tqdm.write(f"-  {zifile} [saved]")
    elif dl == 0:
        tqdm.write(f"Nu s-a putut descărca fișierul de la URL-ul {hours_json_url}")
    elif dl == 2:
        tqdm.write(f"- c {zifile} [cached]")
    


