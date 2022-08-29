import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sqlite3


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


df.groupby('AgeCode').agg({"TreatmentPeriod_days": np.mean, "MedicalExpenses_won": np.mean})
