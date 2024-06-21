# auto detect columns to keep?
# -voturi
# -mandate-faza-*

tip_alegeri   = 'locale'
# diaspora="abroad"
functie_alesi = 'p'
pv_type       = 'final'
uat_type      = 'judet'
data_scrutin  = '09062024'

uatx          = {'sectie': 'sv', 'judet': 'cnty', 'tara': 'cntry'}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -   

import glob, json, argparse
from tqdm import tqdm
import pandas as pd

def process_csv(file_path):
    df = pd.read_csv(file_path)
    columns_to_exclude = ['-voturi', '-mandate']
    columns_to_keep = [col for col in df.columns if not any(col.endswith(exclude) for exclude in columns_to_exclude)]
    
    result = []

    for _, row in df.iterrows():
        row_data = row[columns_to_keep].to_dict()
        
        candidate_cols = [col for col in row.index if '-voturi' in col]
        
        candidates = {}
        for col in candidate_cols:
            name = col.replace("-voturi", "")
            votes = row[col]
            candidates[name] = votes
        
        sorted_candidates = sorted(candidates.items(), key=lambda item: item[1], reverse=True)
        top_3 = sorted_candidates[:3]
        
        if top_3:
            row_data["1st_place_name"] = top_3[0][0]
            row_data["1st_place_count"] = top_3[0][1]
            if len(top_3) > 1:
                row_data["2nd_place_name"] = top_3[1][0]
                row_data["2nd_place_count"] = top_3[1][1]
            if len(top_3) > 2:
                row_data["3rd_place_name"] = top_3[2][0]
                row_data["3rd_place_count"] = top_3[2][1]
        
        row_data["others_names"] = ', '.join([candidate[0] for candidate in sorted_candidates[3:]])
        row_data["others_results"] = ', '.join([str(candidate[1]) for candidate in sorted_candidates[3:]])
        row_data["full_results_json"] = json.dumps(sorted_candidates)

        result.append(row_data)
    
    return pd.DataFrame(result)

processed_dfs = []

parser = argparse.ArgumentParser(description='Merge PVs')
parser.add_argument('--functie', type=str, help='Function type (e.g., pcj)', default='p')
parser.add_argument('--pv-type', type=str, help='PV type (e.g., part)', default='final')
parser.add_argument('--uat', type=str, help='UAT type (e.g., cnty)', default='judet')
parser.add_argument('--data', type=str, help='Dată alegeri (ddmmyyy)', default='09062024')
parser.add_argument('--alegeri', type=str, help='Tip alegeri (e.g., locale, europarlamentare)', default='locale')
args = parser.parse_args()

functie_alesi = args.functie
pv_type = args.pv_type
data_scrutin = args.data

uatx = {'sectie': 'sv', 'judet': 'cnty', 'tara': 'cntry'}
uat_type = uatx[args.uat] if args.uat in uatx else uatx['judet']

data_root = "data/" + data_scrutin + '-' + args.alegeri + '/pvs/'
csv_folder = data_root + functie_alesi + '/' + uat_type + '/' + pv_type + '/'
output_csv = data_root + 'merged-' + functie_alesi + '-' + uat_type + '-' + pv_type + '.csv'
output_xlsx = data_root + 'merged-' + functie_alesi + '-' + uat_type + '-' + pv_type + '.xlsx'

try:
    csv_files = glob.glob(csv_folder + '*.csv')

    for file in tqdm(csv_files, desc="Processing CSV files"):
        try:
            processed_dfs.append(process_csv(file))
        except Exception as e:
            tqdm.write(f"Error processing {file}: {e}")
            continue
    tqdm.write("Start concatenating results...")
    final_df = pd.concat(processed_dfs, ignore_index=True)
    tqdm.write("Concatenating results... done")
    tqdm.write("Exporting results...")

    final_df.to_excel(output_xlsx, index=False, sheet_name='PVs-' + functie_alesi.upper(), freeze_panes=(1,0))

    tqdm.write(f"Done: {output_xlsx} saved")
except Exception as e:
    print(f"Error: {e}")
