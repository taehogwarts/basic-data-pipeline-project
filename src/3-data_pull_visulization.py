import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl
mpl.rc("font", family='AppleGothic')

import os
import sqlite3
import time


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
    'DiseaseCode', 'DiseaseName_Kor', 'DiseaseName_Eng', 'TreatmentPeriod_Days', 'MedicalExpenses_Won'
]

df = pd.DataFrame(data, columns=columns_list)
print(df.info())

cursor.close()
connection.close()

print("Elapsed Time of STAGE 6-2. Data Query:", time.process_time())



group_1 = df.groupby('AgeName').agg({"MedicalExpenses_Won": np.mean})
group_1.plot(kind='bar')
plt.show()

group_1 = df.groupby('AgeName').agg({"TreatmentPeriod_Days": np.mean})
group_1.plot(kind='bar')
plt.show()

group_2 = df.groupby('AreaName').agg({"MedicalExpenses_Won": np.mean})
group_2.plot(kind='bar')
plt.show()

group_2 = df.groupby('AreaName').agg({"TreatmentPeriod_Days": np.mean})
group_2.plot(kind='bar')
plt.show()

group_3 = df.groupby('ClinicName').agg({"MedicalExpenses_Won": np.mean})
group_3.plot(kind='bar')
plt.show()

group_3 = df.groupby('ClinicName').agg({"TreatmentPeriod_Days": np.mean})
group_3.plot(kind='bar')
plt.show()

print("Elapsed Time of STAGE 6-3. Data Visualization:", time.process_time())
