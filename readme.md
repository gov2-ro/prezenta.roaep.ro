Downloadează (și agregă) date despre rezultate și prezență la vot publicate pe [prezenta.roaep.ro](https://prezenta.roaep.ro/) 


- Prezență vot: [consolidated-euro.xlsx](https://docs.google.com/spreadsheets/d/1Rynf1Ns5H1-j0RVtdlvD71mYWL09_B4i/edit?usp=sharing&ouid=110866595781073302984&rtpof=true&sd=true), [consolidated-locale.xlsx](https://docs.google.com/spreadsheets/d/1Ryn5gShIYUN3hjcrSUZurkZBfEQJVHyA/edit?usp=drive_link&ouid=110866595781073302984&rtpof=true&sd=true)    
- PVs: [primărie](https://docs.google.com/spreadsheets/d/1SJQjSnJlN1IeoQ38sXAIBM2LBtrj5Wo_/edit?usp=drive_link&ouid=110866595781073302984), [CL](https://docs.google.com/spreadsheets/d/1SJwARd3E-GEqKiwMhnlfMQP3ayxH11dQ/edit?usp=drive_link&ouid=110866595781073302984) 
- **Agregat**: [verificare-locale PVs + prezenta](https://docs.google.com/spreadsheets/d/1S4K92YJPrIUTOYLAEWafUJvKp04XojPg/edit?gid=1765616260)

## Scripts

Prezență vot
- generate-urls-prezenta.py
- dl-jsons-prezenta.py
- consolidate-prezenta.py

Rezultate (procese verbale)
- dl-pvs.py
- merge-pvs-aggregate.py – ignoră rezultatele / voturile individuale
- merge-pvs-rezultate.py

----

$ python dl-pvs.py --functie <functie> --pv-type <pv-type> --uat <uat> --alegeri <alegeri> 

- functie: _p*, cl, cj, pcj, eup_
- pv-type: _temp, part, final*_ 
- uat: _uat, cnty*, cntry_ 
- alegeri: _locale*, europarlamentare_ 

\* default values

### Data
- data
    - analize/Alegeri locale24 - PVs x Prezență.xlsx ([gSheet](https://docs.google.com/spreadsheets/d/1S4K92YJPrIUTOYLAEWafUJvKp04XojPg)) 
    - pvs
        - cl
        - p
    - jsons-locale
    - jsons-euro
    - siruta-cod_jud.csv

![voturi nule](assets/chart-v-nule.png)
![pivot 1](assets/pivot-p1.png)
![detaliu 1](assets/detaliu-xlsx.png)
![dl data](assets/dl-prezenta.aep.ro.gif)