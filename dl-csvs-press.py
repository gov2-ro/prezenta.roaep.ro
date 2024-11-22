DOWNLOAD_DIR = "data/csvs-presa/PREZ-20241124"

""" 
https://prezenta.roaep.ro/presa/prezenta
https://prezenta.roaep.ro/presa/pv
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()


# URL = "https://prezenta.roaep.ro/presa/pv/EUP-20240609/"
URL = "http://prezenta.roaep.ro/presa/prezenta/PREZ-20241124/"
USERNAME = os.getenv("roaep_press_USERNAME")
PASSWORD = os.getenv("roaep_press_PASSWORD")


if not USERNAME or not PASSWORD:
    print("Error: USERNAME or PASSWORD not found in .env file.")
    exit()


os.makedirs(DOWNLOAD_DIR, exist_ok=True)

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; Python Script)"})
session.adapters["http://"] = requests.adapters.HTTPAdapter(max_retries=3)
session.adapters["https://"] = requests.adapters.HTTPAdapter(max_retries=3)

# Function to check if a file already exists
def file_exists(filename):
    return os.path.exists(os.path.join(DOWNLOAD_DIR, filename))

# Get the page content
try:
    response = session.get(URL, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Failed to access URL {URL}: {e}")
    exit()

soup = BeautifulSoup(response.content, "html.parser")

# Find all links ending with .csv
for link in soup.find_all("a"):
    href = link.get("href")
    if href.endswith(".csv"):
        file_url = urljoin(URL, href)
        file_name = href.split("/")[-1]

        if file_exists(file_name):
            print(f"File {file_name} already exists. Skipping...")
            continue

        print(f"Downloading {file_name}...")
        try:
            file_response = session.get(file_url, timeout=15)
            file_response.raise_for_status()
            with open(os.path.join(DOWNLOAD_DIR, file_name), "wb") as f:
                f.write(file_response.content)
            print(f"Downloaded {file_name} successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {file_name}: {e}")
        
        time.sleep(.2)

print("All files processed.")
