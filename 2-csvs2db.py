import os, glob, subprocess
from tqdm import tqdm

# Configuration variables
# alegeri = '2024-prez-1'
alegeri = '2024-parl'
data_root = "data/"
data_folder = os.path.join(data_root, 'alegeri', alegeri)

pattern1 = os.path.join(data_folder, 'prezenta_????-??-??_??-00.csv')
pattern2 = os.path.join(data_folder, '????-??-??_??-00.csv')

# Collect files matching both patterns
csv_files = glob.glob(pattern1) + glob.glob(pattern2)

if not csv_files:
    print("No files found matching the pattern. " + data_folder)
    exit()
else:
    print(f"Found {len(csv_files)} CSV files to process.")

# Adding a progress bar with tqdm
for csv_file in tqdm(csv_files, desc="Processing CSV files", unit="file"):
    # Call append2db.py with the CSV file as an argument
    subprocess.run(['python', 'append2db-sv.py', csv_file, alegeri], check=False)
    # subprocess.run(['python', 'append2db-jud.py', csv_file, alegeri], check=False)
    # subprocess.run(['python', 'append2db.py', csv_file, alegeri])
