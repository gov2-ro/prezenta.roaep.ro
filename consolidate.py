import json
import pandas as pd
import os
import re

# Directory containing JSON files
json_dir = 'data/jsons-euro/'
output_xlsx = 'data/consolidated-euro.xlsx'
json_dir = 'data/jsons-locale/'
output_xlsx = 'data/consolidated-locale.xlsx'

def flatten_json(json_obj, parent_key='', sep='.'):
    items = []
    for k, v in json_obj.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_json(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Function to extract xcounty and xhour from filename
def extract_county_hour(filename):
    match = re.match(r'presence_([a-z]+)_[\d-]+_(\d+)-00.json', filename)
    if match:
        xcounty = match.group(1)
        xhour = match.group(2)
        return xcounty, xhour
    return None, None

# Initialize a list to store DataFrames
dfs = []

# Loop through all JSON files in the directory
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(json_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract 'precinct' data
        precinct_data = data['precinct']
        
        # Flatten the JSON data
        flattened_data = [flatten_json(precinct) for precinct in precinct_data]
        
        # Convert to DataFrame
        df = pd.DataFrame(flattened_data)
        
        # Extract xcounty and xhour
        xcounty, xhour = extract_county_hour(filename)
        
        # Add xcounty and xhour columns
        df['xcounty'] = xcounty
        df['xhour'] = xhour
        
        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames
final_df = pd.concat(dfs, ignore_index=True)

# Save the final DataFrame to a CSV file (optional)


# I need to delete the following columns from result: age_ranges.men_18_24,age_ranges.men_25_34,age_ranges.men_35_44,age_ranges.men_45_64,age_ranges.men_65+,age_ranges.women_18_24,age_ranges.women_25_34,age_ranges.women_35_44,age_ranges.women_45_64,age_ranges.women_65+
ignore_columns = ['age_ranges.men_18_24','age_ranges.men_25_34','age_ranges.men_35_44','age_ranges.men_45_64','age_ranges.men_65+','age_ranges.women_18_24','age_ranges.women_25_34','age_ranges.women_35_44','age_ranges.women_45_64','age_ranges.women_65+']
final_df.drop(columns=ignore_columns, inplace=True)

# final_df.to_csv(output_csv, index=False)
# save xlsx instead

final_df.to_excel(output_xlsx, index=False)
# Display the DataFrame (optional)
# print(final_df.head())
