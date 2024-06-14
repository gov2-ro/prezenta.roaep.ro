import pandas as pd
import json

# List of CSV files (assuming the files are in the same folder)
csv_files = ['data/pvs/p/pv_part_uat_p_tm_159482.csv', 'data/pvs/p/pv_part_uat_p_tm_159259.csv', 'data/pvs/p/pv_part_uat_p_tm_157834.csv']

# Read and concatenate all CSV files
df_list = [pd.read_csv(file) for file in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Define standard columns
standard_columns = [
    'precinct_county_nce','precinct_county_name','precinct_name','precinct_nr',
    'uat_name','uat_siruta','report_version','report_stage_code','report_type_scope_code',
    'report_type_category_code','report_type_code','created_at','a','a1','a2','a3','a4',
    'b','b1','b2','b3','b4','c','d','e','f'
]

# Identify candidate columns dynamically for each row
def get_candidate_columns(row):
    return [col for col in row.index if col not in standard_columns]

# Function to calculate additional columns
def calculate_columns(row):
    candidate_columns = get_candidate_columns(row)
    candidate_votes = {col: row[col] for col in candidate_columns if not pd.isna(row[col])}
    sorted_candidates = sorted(candidate_votes.items(), key=lambda item: item[1], reverse=True)
    
    # Top 3 candidates
    top_3 = sorted_candidates[:3]
    
    # Remaining candidates
    others = sorted_candidates[3:]
    
    # Results
    result = {
        'candidates_count': len(candidate_columns),
        '1st_place_name': top_3[0][0] if len(top_3) > 0 else '',
        '1st_place_count': top_3[0][1] if len(top_3) > 0 else 0,
        '2nd_place_name': top_3[1][0] if len(top_3) > 1 else '',
        '2nd_place_count': top_3[1][1] if len(top_3) > 1 else 0,
        '3rd_place_name': top_3[2][0] if len(top_3) > 2 else '',
        '3rd_place_count': top_3[2][1] if len(top_3) > 2 else 0,
        'others_names': ';'.join([c[0] for c in others]),
        'others_results': sum([c[1] for c in others]),
        'full_results': json.dumps(sorted_candidates)
    }
    return pd.Series(result)

# Apply the function to each row
df_extra = df.apply(calculate_columns, axis=1)

# Concatenate the original dataframe with the calculated columns
df_final = pd.concat([df, df_extra], axis=1)

# Export to CSV, XLSX, and JSON
csv_output_path = 'data/aggregated_results.csv'
xlsx_output_path = 'data/aggregated_results.xlsx'
json_output_path = 'data/aggregated_results.json'

df_final.to_csv(csv_output_path, index=False)
df_final.to_excel(xlsx_output_path, index=False)
df_final.to_json(json_output_path, orient='records', lines=True)

print(f"CSV output saved to {csv_output_path}")
print(f"XLSX output saved to {xlsx_output_path}")
print(f"JSON output saved to {json_output_path}")
