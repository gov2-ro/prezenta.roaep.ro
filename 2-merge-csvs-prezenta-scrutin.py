import pandas as pd
import glob
import os

data_root = 'data/'
alegeri = '22112024-2024-prez-1.1'

def merge_csv_files(data_folder, output_file):
    """
    Merges CSV files from the specified folder, removes certain columns,
    adds a timestamp column extracted from filenames, and saves the merged data.

    Parameters:
    - data_folder: Path to the folder containing CSV files.
    - output_file: Path for the output merged CSV file.
    """
    # Define the pattern to match the CSV files
    pattern = os.path.join(data_folder, 'prezenta_????-??-??_??-00.csv')
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
            if len(parts) < 3:
                print(f"Filename {filename} does not match the expected pattern. Skipping.")
                continue
            date_part = parts[1]  # <yyyy>-<mm>-<dd>
            time_part = parts[2].split('-')[0]  # <hh>
            timestamp = f"{date_part} {time_part}:00"
            
            
            # Read the CSV file
            df = pd.read_csv(file)
            
            # Drop unwanted columns if they exist
            columns_to_drop = ["UAT", "Localitate", "Nume sectie de votare"]
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
    
    data_folder = data_root + alegeri + '/prezenta/csvs'  
    output_file = data_root + alegeri + '/prezenta/' + alegeri + '--merged'  
    
    merge_csv_files(data_folder, output_file)
