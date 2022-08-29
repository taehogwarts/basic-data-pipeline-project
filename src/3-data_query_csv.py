import pandas as pd
# import csv
import sqlite3

import os
import time

### 대시보드 툴인 Google Data Studio에서 SQLite를 지원하지 않으므로 csv로 저장해서 활용

DB_FILENAME = 'nhis_treatment_records_2021.db'
DB_FILEPATH = os.path.join(os.getcwd(), 'database/'+DB_FILENAME)

table_name = 'TreatmentRecords'
columns_list = [
    'GenderCode', 'AgeCode', 'AreaCode', 'ClinicCode', 'DiseaseCode', 
    'TreatmentPeriod_Days', 'MedicalExpenses_Won'
]

connection = sqlite3.connect(DB_FILEPATH)
cursor = connection.cursor()

cursor.execute(
    f"""
    SELECT {columns_list[0]}, 
        {columns_list[1]}, 
        {columns_list[2]}, 
        {columns_list[3]}, 
        {columns_list[4]}, 
        {columns_list[5]}, 
        {columns_list[6]}
    FROM {table_name}
    ;"""
)

data = cursor.fetchall()

df = pd.DataFrame(data, columns=columns_list)
print(df.info())

CSV_FILENAME = 'nhis_treatment_records_2021.csv'

df.to_csv(CSV_FILENAME)

print("Elapsed Time of STAGE 6-1. Creating CSV for Dashboard:", time.process_time())