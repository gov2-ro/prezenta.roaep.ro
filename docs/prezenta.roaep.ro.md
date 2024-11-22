# Informatii generale

Pentru exemplificare se poate acesa site-ul de prezenta ale ultimelor alegeri prezidentiale si parlamentare:
```
https://prezenta.bec.ro/prezidentiale10112019
https://prezenta.roaep.ro/parlamentare06122020
```


## 1. Nomenclatoare
Nomenclatoare SIMPV (date despre voturi) ce pot fi descarcate 1 singura data:
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/simpv/lists/counties.json - "sr" pentru "Strainatate"
https://prezenta.roaep.ro/prezidentiale24112024/data/json/simpv/lists/uats_ab.json - uats_sr.json - lista de tari
https://prezenta.roaep.ro/prezidentiale24112024/data/json/simpv/lists/localities_ab.json
https://prezenta.roaep.ro/prezidentiale24112024/data/json/simpv/lists/precincts_ab.json
```

Nomenclatoare SICPV (date despre procese verbale) ce pot fi descarcate 1 singura data:
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/sicpv/lists/counties.json
https://prezenta.roaep.ro/prezidentiale24112024/data/json/sicpv/lists/localities_ab.json
https://prezenta.roaep.ro/prezidentiale24112024/data/json/sicpv/lists/precincts_ab.json
```

Pentru fiecare judet exista cate un fisier `uats_XX.json`, `localities_XX.json`, `precincts_XX.json`


## 2. Voturi

Informatiile despre voturi se actualizeaza la fiecare minut:
2.1. Informatii despre prezenta la nivel de judete:
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/simpv/presence/presence_now.json
```

2.2. Informatii despre prezenta la nivel de sectii de votare. Cate un fisier pentru fiecare judet. 
Ex. pentru Prahova se poate inlocui `_ab_` cu `_ph_`:

```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/simpv/presence/presence_ab_now.json
```

Suplimentar exista si date istorice din ora in ora:
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/simpv/presence/presence_2024-11-24_21-00.json
```
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/simpv/presence/presence_ab_2024-11-24_21-00.json
```



## 3. Procese verbale

Informatiile despre procese verbale se genereaza la 5 minute.

3.1. Informatii despre pv-uri la nivel de tara si judet:
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/sicpv/pv/pv.json
```

3.2. Informatii despre pv-uri la nivel de sectie de vot si UAT:
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/sicpv/pv/pv_ab.json
```

JSON-ul contine urmatoarea structura:
```
1. scopes.${scopeCode}.categories.${categoryCode}.files.${teritoryId}          -> fisiere PV-uri
2. scopes.${scopeCode}.categories.${categoryCode}.table.${teritoryId}.fields`  -> campuri din PV-uri (a, a1, a2, a3, a4, b, b1, b2, b3, b4, c, d, e,f )
3. scopes.${scopeCode}.categories.${categoryCode}.table.${teritoryId}.candidates`   -> voturi candidati din PV-uri
```

Valori posibile pentrun campurile cod:

1.scopeCode
```
- PRCNCT
- UAT
- CNTY
- CNTRY
```

2.categoryCode
```
- PRSD (Prezidentiale)
- PRSD_C (Prezidentiale corespondenta)

- S (Senat)
- S_C (Senat corespondenta)
- CD (Camera deputatilor)
- CD_C (Camera deputatilor corespondenta)

- REFL1 (Referendum - intrebarea 1)
- REFL2 (Referendum - intrebarea 2)
- REFL3 (Referendum - intrebarea 3)

```

3. teritoryId
```
if  (scopeCode = PRCNCT) -> precinct_id
if  (scopeCode = UAT)    -> uat_id
if  (scopeCode = CNTY)   -> county_id 
if  (scopeCode = CNTRY)  -> RO 
```


## 4. Procese verbale agregate din sectii

Informatiil contin numarul total de voturi pentru fiecare candidat, la nivel de UAT, judet si tara. Se calculeaza folosind procesele verbale de sectie. Se genereaza la intervale de 5 minute.

3.1. Informatii despre pv-uri la nivel de tara si judet:
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/sicpv/pv/pv_aggregated.json
```

3.2. Informatii despre pv-uri la nivel de UAT:
```
https://prezenta.roaep.ro/prezidentiale24112024/data/json/sicpv/pv/pv_aggregated_ab.json
```

JSON-ul contine urmatoarea structura:
```
scopes.${scopeCode}.categories.${categoryCode}.table.${teritoryId}.candidates`   -> voturi candidati din PV-uri
scopes.${scopeCode}.categories.${categoryCode}.table.${teritoryId}.info. -> numar de sectii de votare centralizate (precincts_with_data / precincts)
```

## URL-urile viitoarelor alegeri:
```
https://prezenta.roaep.ro/prezidentiale24112024
https://prezenta.roaep.ro/referendum24112024
https://prezenta.roaep.ro/parlamentare01122024
```

