#  TODO: check if well formated csv
# auto detect columns to keep?
# -voturi
# -mandate-faza-*

tip_alegeri='locale'
# tip_alegeri='europarlamentare'

# diaspora="abroad"

functie_alesi='p'
# functie_alesi='cl'
functie_alesi='cj'
functie_alesi='pcj'
# functie_alesi='eup'

# pv_type='temp'
# pv_type='part'
pv_type='final'

# uat_type='uat'
uat_type='judet'
# uat_type='tara'

data_scrutin='09062024'      # euro + locale

data_root = "data/" + data_scrutin + '-' + tip_alegeri + '/pvs/'

uatx={
    # 'sectie': 'sv',
    'judet': 'cnty',
    'tara': 'cntry',
}

csv_folder = data_root + functie_alesi + '/' + uatx[uat_type] + '/' + pv_type + '/'
output_csv = data_root + 'merged-' + functie_alesi + '-' + uatx[uat_type] + '-' + pv_type + '.csv'
output_xlsx = data_root + 'merged-' + functie_alesi + '-' + uatx[uat_type] + '-' + pv_type + '.xlsx'


# csv_folder = data_root + 'pvs/cl/'
# output_csv = data_root + 'pvs-cl.csv'
# output_xlsx = data_root + 'pvs-cl.xlsx'

# columns_to_keep = ["precinct_county_nce", "precinct_county_name", "precinct_name", "precinct_nr", "uat_name", "uat_siruta", "report_version", "report_stage_code", "report_type_scope_code", "report_type_category_code", "report_type_code", "created_at", "a", "a1", "a2", "a3", "a4", "b", "b1", "b2", "b3", "b4", "c", "d", "e", "f", "candidates_count", "1st_place_name", "1st_place_count", "2nd_place_name", "2nd_place_count", "3rd_place_name", "3rd_place_count", "others_names", "others_results", "full_results_json"]
columns_to_keep = ["uat_name", "uat_siruta", "report_version", "report_stage_code", "report_type_scope_code", "report_type_category_code", "report_type_code", "created_at", "a", "a1", "a2", "a3", "a4", "b", "b1", "b2", "b3", "b4", "c", "d", "e", "f", "candidates_count", "1st_place_name", "1st_place_count", "2nd_place_name", "2nd_place_count", "3rd_place_name", "3rd_place_count", "others_names", "others_results", "full_results_json"]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -   

import pandas as pd
import glob
import json
from tqdm import tqdm

def process_csv(file_path):
    df = pd.read_csv(file_path)
    result = []

    for _, row in df.iterrows():
        row_data = row[:35].to_dict()
        
        candidate_cols = [col for col in row.index if '-voturi' in col]
        
        candidates = {}
        for col in candidate_cols:
            name = col.replace("-voturi", "")
            votes = row[col]
            candidates[name] = votes
        
        sorted_candidates = sorted(candidates.items(), key=lambda item: item[1], reverse=True)
        top_3 = sorted_candidates[:3]
        others = sorted_candidates[3:]

        row_data["candidates_count"] = len(candidate_cols)
        row_data["1st_place_name"] = top_3[0][0] if len(top_3) > 0 else None
        row_data["1st_place_count"] = top_3[0][1] if len(top_3) > 0 else None
        row_data["2nd_place_name"] = top_3[1][0] if len(top_3) > 1 else None
        row_data["2nd_place_count"] = top_3[1][1] if len(top_3) > 1 else None
        row_data["3rd_place_name"] = top_3[2][0] if len(top_3) > 2 else None
        row_data["3rd_place_count"] = top_3[2][1] if len(top_3) > 2 else None
        row_data["others_names"] = ";".join([name for name, _ in others])
        row_data["others_results"] = sum([votes for _, votes in others])
        row_data["full_results_json"] = json.dumps(sorted_candidates)

        result.append(row_data)
    
    return pd.DataFrame(result, columns=columns_to_keep)

processed_dfs = []

try:
    csv_files = glob.glob(csv_folder + '*.csv')

    for file in tqdm(csv_files, desc="Processing CSV files"):
        #  TODO: check if well formated csv
        try:
            processed_dfs.append(process_csv(file))
        except Exception as e:
            tqdm.write(f"Error processing {file}: {e}")
            continue
    tqdm.write("Start concatenating results...")
    final_df = pd.concat(processed_dfs, ignore_index=True)
    tqdm.write("Concatenating results... done")
    tqdm.write("Exporting results...")

    # final_df.to_csv(output_csv, index=False)
    final_df.to_excel(output_xlsx, index=False)

    tqdm.write(f"Done: {output_xlsx} saved")
except Exception as e:
    print(f"Error: {e}")