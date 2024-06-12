import pandas as pd
import os
import glob

# Define the directory where the CSV files are stored
input_dir = "data/pvs/cl"  # Change this to your actual directory if needed
output_file = "data/merged_pvs-cl.csv"  # Change this to your desired output path if needed

# Define the common columns
common_columns = [
    "precinct_county_nce", "precinct_county_name", "precinct_name", "precinct_nr",
    "uat_name", "uat_siruta", "report_version", "report_stage_code",
    "report_type_scope_code", "report_type_category_code", "report_type_code",
    "created_at", "a", "a1", "a2", "a3", "a4", "b", "b1", "b2", "b3", "b4", 
    "c", "d", "e", "f"
]

# Get a list of all CSV files in the directory
csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

# Initialize an empty DataFrame to hold the merged data
merged_df = pd.DataFrame()

# Iterate over each CSV file
for file_path in csv_files:
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Extract the county code from the filename
    county_code = file_path.split('_')[-2]
    
    # Add the county_code column
    df['county_code'] = county_code
    
    # Keep only the common columns
    df = df[common_columns + ['county_code']]
    
    # Append to the merged DataFrame
    merged_df = pd.concat([merged_df, df], ignore_index=True)

# Save the merged DataFrame to a CSV file
merged_df.to_csv(output_file, index=False)

print(f"Merged CSV saved to {output_file}")
