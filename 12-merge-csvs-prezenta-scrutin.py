import pandas as pd
import glob, os

data_root =  'data/'
alegeri = '2024-parl'

def merge_csv_files(data_folder, output_file):
    """
    Merges CSV files from the specified folder, removes certain columns,
    adds a timestamp column extracted from filenames, and saves the merged data.

    Parameters:
    - data_folder: Path to the folder containing CSV files.
    - output_file: Path for the output merged CSV file.
    """
    # Define the pattern to match the CSV files
    # pattern = os.path.join(data_folder, 'prezenta_????-??-??_??-00.csv')
    pattern = os.path.join(data_folder, '????-??-??_??-00.csv')
    # pattern = os.path.join(data_folder, '????-??-??_??-00')
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        print("No files found matching the pattern.")
        return

    # List to hold individual DataFrames
    df_list = []

    for file in csv_files:
        try:
            # Extract filename without directory
            filename = os.path.basename(file)
            
            # Extract timestamp using string manipulation
            # Expected filename format: prezenta_<yyyy>-<mm>-<dd>_<hh>-00.csv
            parts = filename.replace('.csv', '').split('_')
            if len(parts) < 2:
                print(f"Filename {filename} does not match the expected pattern. Skipping.")
                continue
            date_part = parts[0]  # <yyyy>-<mm>-<dd>
            time_part = parts[1].split('-')[0]  # <hh>
            timestamp = f"{date_part} {time_part}:00"
            
            
            # Read the CSV file
            df = pd.read_csv(file)
            
            # Drop unwanted columns if they exist
            columns_to_drop = ["UAT", "Localitate", "Nume sectie de votare","Barbati 18","Barbati 19","Barbati 20","Barbati 21","Barbati 22","Barbati 23","Barbati 24","Barbati 25","Barbati 26","Barbati 27","Barbati 28","Barbati 29","Barbati 30","Barbati 31","Barbati 32","Barbati 33","Barbati 34","Barbati 35","Barbati 36","Barbati 37","Barbati 38","Barbati 39","Barbati 40","Barbati 41","Barbati 42","Barbati 43","Barbati 44","Barbati 45","Barbati 46","Barbati 47","Barbati 48","Barbati 49","Barbati 50","Barbati 51","Barbati 52","Barbati 53","Barbati 54","Barbati 55","Barbati 56","Barbati 57","Barbati 58","Barbati 59","Barbati 60","Barbati 61","Barbati 62","Barbati 63","Barbati 64","Barbati 65","Barbati 66","Barbati 67","Barbati 68","Barbati 69","Barbati 70","Barbati 71","Barbati 72","Barbati 73","Barbati 74","Barbati 75","Barbati 76","Barbati 77","Barbati 78","Barbati 79","Barbati 80","Barbati 81","Barbati 82","Barbati 83","Barbati 84","Barbati 85","Barbati 86","Barbati 87","Barbati 88","Barbati 89","Barbati 90","Barbati 91","Barbati 92","Barbati 93","Barbati 94","Barbati 95","Barbati 96","Barbati 97","Barbati 98","Barbati 99","Barbati 100","Barbati 101","Barbati 102","Barbati 103","Barbati 104","Barbati 105","Barbati 106","Barbati 107","Barbati 108","Barbati 109","Barbati 110","Barbati 111","Barbati 112","Barbati 113","Barbati 114","Barbati 115","Barbati 116","Barbati 117","Barbati 118","Barbati 119","Barbati 120","Femei 18","Femei 19","Femei 20","Femei 21","Femei 22","Femei 23","Femei 24","Femei 25","Femei 26","Femei 27","Femei 28","Femei 29","Femei 30","Femei 31","Femei 32","Femei 33","Femei 34","Femei 35","Femei 36","Femei 37","Femei 38","Femei 39","Femei 40","Femei 41","Femei 42","Femei 43","Femei 44","Femei 45","Femei 46","Femei 47","Femei 48","Femei 49","Femei 50","Femei 51","Femei 52","Femei 53","Femei 54","Femei 55","Femei 56","Femei 57","Femei 58","Femei 59","Femei 60","Femei 61","Femei 62","Femei 63","Femei 64","Femei 65","Femei 66","Femei 67","Femei 68","Femei 69","Femei 70","Femei 71","Femei 72","Femei 73","Femei 74","Femei 75","Femei 76","Femei 77","Femei 78","Femei 79","Femei 80","Femei 81","Femei 82","Femei 83","Femei 84","Femei 85","Femei 86","Femei 87","Femei 88","Femei 89","Femei 90","Femei 91","Femei 92","Femei 93","Femei 94","Femei 95","Femei 96","Femei 97","Femei 98","Femei 99","Femei 100","Femei 101","Femei 102","Femei 103","Femei 104","Femei 105","Femei 106","Femei 107","Femei 108","Femei 109","Femei 110","Femei 111","Femei 112","Femei 113","Femei 114","Femei 115","Femei 116","Femei 117","Femei 118","Femei 119","Femei 120"]
            existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
            df = df.drop(columns=existing_columns_to_drop)
            
            # Add the timestamp column
            df['timestamp'] = timestamp
            df['alegeri'] = alegeri
            
            # Append the DataFrame to the list
            df_list.append(df)
            
            print(f"Processed file: {filename}")
        
        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    if not df_list:
        print("No data to merge after processing files.")
        return

    # Concatenate all DataFrames
    merged_df = pd.concat(df_list, ignore_index=True)
    
    print(merged_df.head())
    print('-----')
    print('preparing aggregate data ... ')
    
    merged_df.to_csv(output_file + '.csv', index=False)
    print(f"CSV: Merged data saved to {output_file}")
    
    # merged_df.to_excel(output_file + '.xlsx', index=False)
    # print(f"XLSX: Merged data also saved to {output_file}.xlsx")

if __name__ == "__main__":
    
    data_folder = data_root + 'alegeri/' + alegeri + '/'  
    output_file = data_root + 'alegeri/' + alegeri + '/' + alegeri + '--merged'  
    
    merge_csv_files(data_folder, output_file)
