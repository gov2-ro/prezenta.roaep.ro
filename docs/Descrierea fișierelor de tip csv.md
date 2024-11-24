Descrierea fișierelor de tip .csv (comma separated values) cu toate informațiile din procesele verbale publicate conform [deciziei BEC nr. 161D/17.11.2024](https://prezidentiale2024.bec.ro/wp-content/uploads/2024/11/Decizie_161D_P.pdf): 
1.  Fisierul .csv cu rezultatele actualizate(**ultima versiune**) din procesele verbale întocmite de birourile secțiilor de votare conform anexelor 1A,1B și 1C. Fisierul va respecta urmatorii parametri:
    1.  Denumire: pv_part_cntry_prsd
    2.  Actualizare la 10 minute( se va inlocui fisierul vechi cu altul cu aceeasi denumire)
    3.  Vor include doar ultima versiune a procesului verbal si starea în care se afla acesta [^1]
    4.  Informatia va fi desfasurată pe următoarele coloane:
        -   precinct_county_nce
        -   precinct_county_name
        -   precinct_name
        -   precinct_nr
        -   uat_name
        -   uat_siruta
        -   report_version
        -   report_stage_code(PROV,PART,FINAL)
        -   report_type_scope_code
        -   report_type_category_code
        -   report_type_code
        -   created_at
        -   a
        -   b
        -   b1
        -   b2
        -   b3
        -   c
        -   d
        -   e
        -   f
        -   CANDIDAT 1-voturi
        -   ....
        -   CANDIDAT n -voturi (n la turul 1=14, turul 2 n=2)
1.  2 fisiere.csv cu rezultatele din secțiile de votare(**PRIMA versiune**) din procesele verbale întocmite de birourile secțiilor de votare conform anexelor 1A,1B și 1C. Fisierul va respecta urmatorii parametri:
    1.  Denumire: pv_prov_cntry_prsd_v1(sau v2)
    2.  Publicarea primei versiuni se va face dupa ce a ultima sectie din tara a transmis rezultatele prin intermediul SIMPV, iar versiunea 2 se va publica dupa ce ultima sectie din strainatate a transmis rezultatele.
    3.  Informatia va fi desfasurată pe următoarele coloane:
        -   precinct_county_nce
        -   precinct_county_name
        -   precinct_name
        -   precinct_nr
        -   uat_name
        -   uat_siruta
        -   report_version(v1)
        -   report_stage_code(PROV)
        -   report_type_scope_code
        -   report_type_category_code
        -   report_type_code
        -   created_at
        -   a
        -   b
        -   b1
        -   b2
        -   b3
        -   c
        -   d
        -   e
        -   f
        -   CANDIDAT 1-voturi
        -   ....
        -   CANDIDAT n -voturi (n la turul 1=14, turul 2 n=2)
1.  Fisierul .csv cu rezultatele actualizate(**ultima versiune**) din procesele verbale întocmite de birourile secțiilor de votare **pentru votul prin corespondență** conform anexei 1D. Fisierul va respecta urmatorii parametri:
    1.  Denumire: pv_part_cntry_prsd_c
    2.  Actualizare la 10 minute( se va inlocui fisierul vechi cu altul cu aceeasi denumire)
    3.  Vor include doar ultima versiune a procesului verbal si starea în care se afla acesta [^1]
    4.  Informatia va fi desfasurată pe următoarele coloane:
        -   precinct_county_nce
        -   precinct_county_name
        -   precinct_name
        -   precinct_nr
        -   uat_name
        -   uat_siruta
        -   report_version
        -   report_stage_code
        -   report_type_scope_code
        -   report_type_category_code
        -   report_type_code
        -   created_at
        -   a
        -   b
        -   b1
        -   b2
        -   c
        -   c1
        -   c2
        -   d
        -   d1
        -   d2
        -   CANDIDAT 1-voturi
        -   ....
        -   CANDIDAT n -voturi (n la turul 1=14, turul 2 n=2)
1.  Fisierul .csv cu rezultatele din secțiile de votare(**PRIMA versiune**) din procesele verbale întocmite de birourile secțiilor de votare **pentru votul prin corespondență** conform anexei 1D. Fisierul va respecta urmatorii parametri:
    1.  Denumire: pv_prov_cntry_prsd_c_v1
    2.  Publicarea se va face dupa ce a ultima sectie **pentru votul prin corespondență** a transmis rezultatele prin intermediul SIMPV,
    3.  Informatia va fi desfasurată pe următoarele coloane:
        -   precinct_county_nce
        -   precinct_county_name
        -   precinct_name
        -   precinct_nr
        -   uat_name
        -   uat_siruta
        -   report_version(v1)
        -   report_stage_code(PROV)
        -   report_type_scope_code
        -   report_type_category_code
        -   report_type_code
        -   created_at
        -   a
        -   b
        -   b1
        -   b2
        -   c
        -   c1
        -   c2
        -   d
        -   d1
        -   d2
        -   CANDIDAT 1-voturi
        -   ....
        -   CANDIDAT n -voturi (n la turul 1=14, turul 2 n=2)

[^1]: PROV- datele din PV sunt provizorii(au fost transmise din secții dar nu a fost verificat de biroul electoral superior, PART=datele sunt verificate și validate de biroul electoral superior , FINAL=datele au fost incluse in PV-ul centralizator al biroului electoral superior.
