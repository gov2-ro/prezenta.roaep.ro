import pandas as pd
import os
import glob
from tqdm import tqdm

# Define the directory where the CSV files are stored
input_dir = "data/pvs/cl"  # Change this to your actual directory if needed
output_file = "data/complementary_merged_pvs-x.csv"  # Change this to your desired output path if needed
log_file = "data/merged-candidates.log"  # Log file path

# Define the reference columns to keep
reference_columns = [
    "precinct_county_nce", "precinct_county_name", "precinct_name", "precinct_nr",
    "uat_name", "uat_siruta", "report_version", "county_code"
]

# Get a list of all CSV files in the directory
csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

# Initialize an empty DataFrame to hold the merged data
merged_df = pd.DataFrame()

# Open log file
with open(log_file, 'w') as log:
    # Iterate over each CSV file with progress bar
    for file_path in tqdm(csv_files, total=len(csv_files), desc="Processing CSV files"):
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Extract the county code from the filename
        county_code = file_path.split('_')[-2]
        
        # Add the county_code column
        df['county_code'] = county_code
        
        # Keep only the reference columns and non-common columns
        common_cols = list(set(reference_columns).intersection(df.columns))
        extra_cols = list(set(df.columns) - set(reference_columns))
        
        # Melt the dataframe to have candidate_name and count_votes
        df_melted = df.melt(id_vars=common_cols, value_vars=extra_cols, 
                            var_name='candidate_name', value_name='count_votes')
        
        # Append to the merged DataFrame
        merged_df = pd.concat([merged_df, df_melted], ignore_index=True)
        
        # Log the merged file
        log.write(f"Merged: {file_path}\n")

# Save the merged DataFrame to a CSV file
merged_df.to_csv(output_file, index=False)

print(f"Complementary merged CSV saved to {output_file}")
print(f"Log of merged files saved to {log_file}")
