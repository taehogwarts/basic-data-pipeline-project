import pandas as pd
# import csv
import sqlite3

import os
import time

### 대시보드 툴인 Google Data Studio에서 SQLite를 지원하지 않으므로 csv로 저장해서 활용

DB_FILENAME = 'nhis_treatment_records_2021.db'
DB_FILEPATH = os.path.join(os.getcwd(), 'database/'+DB_FILENAME)

connection = sqlite3.connect(DB_FILEPATH)
cursor = connection.cursor()

cursor.execute(
    f"""
    SELECT tr.GenderCode, 
        tr.AgeCode, a.AgeName, 
        tr.AreaCode, a2.AreaName, 
        tr.ClinicCode, c.ClinicName, 
        tr.DiseaseCode, d.DiseaseName_Kor, d.DiseaseName_Eng, 
        tr.TreatmentPeriod_Days, 
        tr.MedicalExpenses_Won 
    FROM TreatmentRecords tr 
    INNER JOIN Age a 
        ON tr.AgeCode = a.AgeCode 
    INNER JOIN Area a2 
        ON tr.AreaCode = a2.AreaCode 
    INNER JOIN Clinic c 
        ON tr.ClinicCode = c.ClinicCode 
    INNER JOIN Disease d 
        ON tr.DiseaseCode = d.DiseaseCode 
    ;"""
)

data = cursor.fetchall()
columns_list = [
    'GenderCode', 'AgeCode', 'AgeName', 'AreaCode', 'AreaName', 'ClinicCode', 'ClinicName', 
    'DiseaseCode', 'DiseaseName_Kor', 'DiseaseName_Eng', 'TreatmentPeriod_Days', 'MedicalExpenses_won'
]

df = pd.DataFrame(data, columns=columns_list)
print(df.info())

cursor.close()
connection.close()

CSV_FILENAME = 'all_tables_joined.csv'
df.to_csv(CSV_FILENAME)

print("Elapsed Time of STAGE 6-1. Creating CSV for Dashboard:", time.process_time())