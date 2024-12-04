data_root = "data/alegeri"
lista_alegeri = ['2016-parl', '2019-euparl', '2019-prez-1', '2019-prez-2', '2019-ref', '2020-parl', '2024-euparl', '2024-local', '2024-parl', '2024-prez-1']

import os, glob, subprocess
from tqdm import tqdm

count_alegeri = len(lista_alegeri)
counter = 0

for alegeri in lista_alegeri:
    counter += 1
    tqdm.write(f"--- Processing ::{alegeri}:: ({counter}/{count_alegeri}) --- ")
    
    data_folder = os.path.join(data_root, alegeri)

    pattern1 = os.path.join(data_folder, 'prezenta_????-??-??_??-00.csv')
    pattern2 = os.path.join(data_folder, '????-??-??_??-00.csv')

    csv_files = glob.glob(pattern1) + glob.glob(pattern2)

    if not csv_files:
        tqdm.write("No files found matching the pattern. " + data_folder)
        exit()
    else:
        tqdm.write(f"Found {len(csv_files)} CSV files")

    for csv_file in tqdm(csv_files, desc="Processing CSV files", unit="file"):
        subprocess.run(['python', 'append2db-sv.py', csv_file, alegeri])

tqdm.write(' -- DONE 👌🏻 --')