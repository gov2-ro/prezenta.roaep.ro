import pandas as pd
import glob
import json

def process_csv(file_path):
    df = pd.read_csv(file_path)
    result = []

    for _, row in df.iterrows():
        row_data = row[:35].to_dict()
        candidate_cols = row.index[35:]
        
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
        row_data["remaining_votes"] = sum([votes for _, votes in others])
        row_data["full_results_json"] = json.dumps(sorted_candidates)

        result.append(row_data)
    
    return pd.DataFrame(result)

# Load all CSV files
csv_files = glob.glob('data/pvs/p-sample/*.csv')

# Process and concatenate all CSV files
processed_dfs = [process_csv(file) for file in csv_files]
final_df = pd.concat(processed_dfs, ignore_index=True)

# Save the results to CSV and Excel
final_df.to_csv('data/concatenated_results.csv', index=False)
final_df.to_excel('data/concatenated_results.xlsx', index=False)
