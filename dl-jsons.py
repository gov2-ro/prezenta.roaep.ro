import os

csv_file = "data/presence_urls-22-europarlamentare.csv"
destination_dir = "data/jsons-euro/"
csv_file = "data/presence_urls-22-locale.csv"
destination_dir = "data/jsons-locale/"

import pandas as pd
import requests

df = pd.read_csv(csv_file)

os.makedirs(destination_dir, exist_ok=True)

for index, row in df.iterrows():
    judet = row["judet"]
    ora = row["ora"]
    url = row["url"]
    
    filename = f"presence_{judet}_2024-06-09_{ora}-00.json"
    filepath = os.path.join(destination_dir, filename)
    
    if not os.path.exists(filepath):
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            print(f"Fișierul {filename} a fost descărcat și salvat.")
        else:
            print(f"Nu s-a putut descărca fișierul de la URL-ul {url}. Status code: {response.status_code}")
    # else:
    #     print(f"Fișierul {filename} deja există în directorul de destinație.")

print("Toate fișierele potențiale au fost verificate.")