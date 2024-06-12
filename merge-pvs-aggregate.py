import pandas as pd
import os
import glob


input_dir = "data/pvs/cl"  
output_file = "data/merged_pvs-cl.csv"  
input_dir = "data/pvs/p"  
output_file = "data/merged_pvs-p.csv"  

common_columns = [
    "precinct_county_nce", "precinct_county_name", "precinct_name", "precinct_nr",
    "uat_name", "uat_siruta", "report_version", "report_stage_code",
    "report_type_scope_code", "report_type_category_code", "report_type_code",
    "created_at", "a", "a1", "a2", "a3", "a4", "b", "b1", "b2", "b3", "b4", 
    "c", "d", "e", "f"
]


csv_files = glob.glob(os.path.join(input_dir, "*.csv"))


merged_df = pd.DataFrame()


for file_path in csv_files:
    
    df = pd.read_csv(file_path)
    
    
    county_code = file_path.split('_')[-2]
    
    
    df['county_code'] = county_code
    
    
    df = df[common_columns + ['county_code']]
    
    
    merged_df = pd.concat([merged_df, df], ignore_index=True)


merged_df.to_csv(output_file, index=False)

print(f"Merged CSV saved to {output_file}")
