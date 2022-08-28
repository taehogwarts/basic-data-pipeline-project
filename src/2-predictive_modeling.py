import pandas as pd
import matplotlib.pyplot as plt

import os
import sqlite3
import time


#1. DB에서 데이터 쿼리해서 데이터프레임 객체에 저장

DB_FILENAME = 'nhis_treatment_records_2021.db'
DB_FILEPATH = os.path.join(os.getcwd(), 'database/'+DB_FILENAME)

columns_list = [
    'Gender', 'Age', 'AreaCode', 'ClinicCode', 'TreatmentPeriod_Days', 'MedicalExpenses_Won'
]
table_name = 'TreatmentRecords'

connection = sqlite3.connect(DB_FILEPATH)
cursor = connection.cursor()

cursor.execute(
    f"""
    SELECT {columns_list[0]}, {columns_list[1]}, {columns_list[2]}, {columns_list[3]}, {columns_list[4]}, {columns_list[5]}
    FROM {table_name}
    ;"""
)

data = cursor.fetchall()


### tuple을 DataFrame의 데이터로 바로 받아 오는 게 가능함
### Ref. https://appdividend.com/2022/06/02/how-to-convert-python-tuple-to-dataframe
df = pd.DataFrame(data, columns=columns_list)

print(df.info())


print("Elapsed Time of STAGE 3-1. Data Query:", time.process_time())



#2. 데이터 전처리 및 세트 나누기

#2-1. 2-way holdout -- 훈련/테스트 세트 나누기

from sklearn.model_selection import train_test_split

features = columns_list[0:3]
target_1 = columns_list[4]
target_2 = columns_list[5]

plt.boxplot(x=df[target_1])
plt.show()

plt.boxplot(x=df[target_2])
plt.show()

train, test = train_test_split(df, test_size=0.25)
### 타겟 분포가 매우 skewed되어 있으므로 


print("Elapsed Time of STAGE 3-2. Data Preprocessing & Dataset-Split:", time.process_time())






#3. 머신러닝 모델링

#2-2. 머신러닝 모델링 1) RandomForestClassifier



#2-3. 머신러닝 모델링 2) XGBoostClassifier



#2-4. 전체 데이터셋으로 최종 모델 학습



#2-5. 모델 pickling



#3. 본인부담금 예측 모델링 및 성능평가


