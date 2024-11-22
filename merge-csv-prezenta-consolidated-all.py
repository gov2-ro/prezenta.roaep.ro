
data_folder = 'data/_merged/alegeri/'  # Change this if your data folder is elsewhere
output_file = 'data/_merged/prezenta-alegeri-all-merged.csv'  # Change the output file name as needed



import pandas as pd
import glob
import os

def merge_csv_files_enhanced(data_folder, output_file):
    """
    Merges all CSV files in the specified folder into a single CSV file.
    - Includes all unique columns from all CSVs.
    - Removes specified unwanted columns if they exist.
    - Adds a 'filename' column at the beginning indicating the source file.


    Parameters:
    - data_folder: Path to the folder containing CSV files.
    - output_file: Path for the output merged CSV file.
    """
    # Define the pattern to match CSV files (adjust if needed)
    pattern = os.path.join(data_folder, '*.csv')
    csv_files = glob.glob(pattern)

    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    # List to hold individual DataFrames
    df_list = []

    for file in csv_files:
        try:
            # Extract filename without directory
            filename = os.path.basename(file)

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)

            # Insert the 'filename' column at the beginning
            df.insert(0, 'filename', filename)

            # Remove unwanted columns if they exist
            columns_to_remove = ["UAT", "Localitate", "Nume sectie de votare"]
            existing_columns_to_remove = [col for col in columns_to_remove if col in df.columns]
            if existing_columns_to_remove:
                df.drop(columns=existing_columns_to_remove, inplace=True)

      

            # Append the DataFrame to the list
            df_list.append(df)

            print(f"Processed file: {filename}")

        except Exception as e:
            print(f"Error processing file {file}: {e}")
            continue

    if not df_list:
        print("No data to merge after processing files.")
        return

    # Concatenate all DataFrames, aligning columns
    merged_df = pd.concat(df_list, ignore_index=True, sort=False)

    # Ensure 'filename' is the first column and 'timestamp' is the second
    columns = merged_df.columns.tolist()
    if 'filename' in columns:
        columns.remove('filename')
        columns.insert(0, 'filename')
        merged_df = merged_df[columns]

    # Save the merged DataFrame to a CSV file
    merged_df.to_csv(output_file, index=False)
    print(f"Merged data saved to {output_file}")

if __name__ == "__main__":
    # Define the data folder and output file path
    

    merge_csv_files_enhanced(data_folder, output_file)
