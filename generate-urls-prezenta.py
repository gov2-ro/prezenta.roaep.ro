
hour_end = 22
tip_alegeri= "locale"
tip_alegeri= "europarlamentare"

csv_file = "data/presence_urls-" + str(hour_end) + "-" + tip_alegeri + ".csv"
judete = ["ab", "ar", "ag", "bc", "bh", "bn", "bt", "br", "bv", "b", "bz", "cl", "cs", "cj", "ct", "cv", "db", "dj", "gl", "gr", "gj", "hr", "hd", "il", "is", "if", "mm", "mh", "ms", "nt", "ot", "ph", "sj", "sm", "sb", "sv", "tr", "tm", "tl", "vl", "vs", "vn"]


import pandas as pd

# Definirea parametrilor
ore = [f"{hour:02d}" for hour in range(7, hour_end + 1)]
# Crearea URL-urilor
# url_template = "https://prezenta.roaep.ro/locale09062024/data/json/simpv/presence/presence_{judet}_2024-06-09_{ora}-00.json"
url_template = "https://prezenta.roaep.ro/" + tip_alegeri +"09062024/data/json/simpv/presence/presence_{judet}_2024-06-09_{ora}-00.json"
data = []

for judet in judete:
    for ora in ore:
        url = url_template.format(judet=judet, ora=ora)
        data.append({"judet": judet, "ora": ora, "url": url})

# Crearea DataFrame-ului
df = pd.DataFrame(data)


df.to_csv(csv_file, index=False)

print(f"Fișierul CSV a fost salvat ca {csv_file}")
