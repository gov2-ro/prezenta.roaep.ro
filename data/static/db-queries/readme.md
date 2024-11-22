https://prezenta.roaep.ro/locale09062024/data/csv/sicpv/pv_part_cnty_pcj_b.csv

count votes from json

        WITH parsed AS (
        SELECT 
            json_extract(value, '$[0]') AS name,
            CAST(json_extract(value, '$[1]') AS INTEGER) AS votes
        FROM [PVs-CJ],
            json_each([PVs-CJ].full_results_json)
        )
        SELECT name, SUM(votes) AS total_votes
        FROM parsed
        GROUP BY name
        ORDER BY total_votes DESC;