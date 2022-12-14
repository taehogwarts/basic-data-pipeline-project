from random import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sqlite3
import time
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import TransformedTargetRegressor
from sklearn.metrics import r2_score



#1. DB에서 데이터 쿼리해서 데이터프레임 객체에 저장

DB_FILENAME = 'nhis_treatment_records_2021.db'
DB_FILEPATH = os.path.join(os.getcwd(), 'database/'+DB_FILENAME)


table_name = 'TreatmentRecords'

connection = sqlite3.connect(DB_FILEPATH)
cursor = connection.cursor()

columns_list = [
    'GenderCode', 'AgeCode', 'AreaCode', 'ClinicCode', 'MedicalExpenses_Won'
]
cursor.execute(
    f"""
    SELECT {columns_list[0]}, {columns_list[1]}, {columns_list[2]}, {columns_list[3]}, {columns_list[4]}
    FROM {table_name}
    ;"""
)

data = cursor.fetchall()


### tuple을 DataFrame의 데이터로 바로 받아 오는 게 가능함
### Ref. https://appdividend.com/2022/06/02/how-to-convert-python-tuple-to-dataframe

df = pd.DataFrame(data, columns=columns_list)

print(df.info())

### 결측치, 중복치 개수 확인 --> 공신력 있는 데이터셋이므로 불필요



print("Elapsed Time of STAGE 3-1. Data Query:", time.process_time())




#2. 데이터 전처리 및 세트 나누기

#2-1. 데이터 전처리

target_1 = 'TreatmentPeriod_Days'
target_2 = 'MedicalExpenses_Won'

## 각 타겟값의 상위, 하위 1%를 이상치로 간주하여 제거
# target_1_top1perc_index_set = set(df[df[target_1] > np.percentile(df[target_1], 99)].index)
# target_1_bot1perc_index_set = set(df[df[target_1] < np.percentile(df[target_1], 1)].index)
# # target_2_top1perc_index_set = set(df[df[target_2] > np.percentile(df[target_2], 99)].index)
# # target_2_bot1perc_index_set = set(df[df[target_2] < np.percentile(df[target_2], 1)].index)
### 타겟2는 제거 후 아래서 로그변환하면 오히려 살짝 left-skewed 분포로 바뀌므로 제거하지 않기로 결정!

# outliers_index_set = target_1_top1perc_index_set.union(target_1_bot1perc_index_set)
# df_clean = df.drop(index = outliers_index_set)
# print(df.info())


### 분포 확인
# # plt.boxplot(x=df[target_1])
# plt.hist(df[target_1])
# plt.show()

# # plt.boxplot(x=df[target_2])
# plt.hist(df[target_2])
# plt.show()

# sns.displot(df[target_1])
# sns.displot(df[target_2])
## 이유는 모르겠으나 터미널에서 seaborn plot이 잘 안 뜸..



## 이상치 제거 후에도 타겟 분포가 매우 right-skewed이므로 로그변환
# target_1_transformed_ser = np.log1p(df[target_1])
# target_2_transformed_ser = np.log1p(df[target_2])

# plt.hist(target_1_transformed_ser)
# plt.show()
# plt.hist(target_2_transformed_ser)
# plt.show()

### 타겟1(요양일수)은 right-skewed가 심각하여 로그변환 해도 분포가 거의 개선이 안 됨
### 반면 타겟2(본인부담금)는 이상치 제거를 하지 않고도 로그변환 후 분포가 거의 정규분포 형태를 띠게 됨



### 결론: 예측 모델링 대상은 타겟2만, 타겟1은 모델링 없이 대시보드에만 활용

# df = df.drop(columns=target_1)
# print(df.info())




#2-2. 2-way holdout -- 훈련/테스트 세트 나누기

features = columns_list[:-1]
target = target_2

train, test = train_test_split(df, test_size=0.25)

### 세트별 분포(skewness) 확인
# plt.hist(np.log1p(train[target]))
# plt.show()
# plt.hist(np.log1p(test[target]))
# plt.show()

X_train = train[features]
y_train = train[target]
X_test = test[features]
y_test = test[target]

print("Elapsed Time of STAGE 3-2. Data Preprocessing & Dataset-Split:", time.process_time())






#3. 머신러닝 모델링

### 특성 인코딩 불필요 (모두 범주형 변수인데 - 데이터셋에서 모두 이미 순서형 인코딩 된 상태)

### 데이터 비선형 상태이므로 선형회귀 모델 사용은 적절하지 않음
### 트리모델이면서 앙상블 방법인 랜덤포레스트(배깅) 또는 부스팅 모델 사용이 적절

#3-0. 기준모델: 평균모델

predict = y_train.mean()
y_pred = [predict] * len(y_test)
baseline_score = r2_score(y_test, y_pred)
print(f'R2 Score of the Baseline(Mean) Model: {baseline_score}')

print("Elapsed Time of STAGE 4-0. Model Training & Test 0 - Baseline(Mean):", time.process_time())
### 결과 - R2 Score of the Baseline(Mean) Model: -2.9956906466566124e-07



#3-1. 머신러닝 모델링 1) RandomForestRegressor

from sklearn.ensemble import RandomForestRegressor

model_1 = RandomForestRegressor(
    n_estimators=300, 
    max_depth=10,  
    n_jobs=-1
)

ttr_1 = TransformedTargetRegressor(
    regressor=model_1,
    func=np.log1p, 
    inverse_func=np.expm1
)

ttr_1.fit(X_train, y_train)
y_pred = ttr_1.predict(X_test)
randomforest_score = r2_score(y_test, y_pred)
print(f'R2 Score of the Random Forest Model: {randomforest_score}')

print("Elapsed Time of STAGE 4-1. Model Training & Test 1 - RandomForestRegressor:", time.process_time())
### 결과 - R2 Score of the Random Forest Model: -0.016489235623298848



#3-2. 머신러닝 모델링 2) XGBoostRegressor
### 데이터셋 크기가 매우 크므로 하이퍼파라미터 튜닝까지 하기엔 시간이 부족
### XGBoost는 하이퍼파라미터 세팅에 민감하므로 안 하는 게 나을 수도 있음

## 위의 랜덤포레스트 모델링 결과 - 과적합(R2값 음수) 상태이므로 부스팅 불필요 판단했지만... 그래도 해봄

from xgboost import XGBRegressor

model_2 = XGBRegressor(
    n_estimators=200, 
    learning_rate=0.2, 
    n_jobs=-1
)

ttr_2 = TransformedTargetRegressor(
    regressor=model_2, 
    func=np.log1p, 
    inverse_func=np.expm1
)

ttr_2.fit(X_train, y_train)
y_pred = ttr_2.predict(X_test)
xgboost_score = r2_score(y_test, y_pred)
print(f'R2 Score of the Gradient Boosting Model(XGBoost): {xgboost_score}')

print("Elapsed Time of STAGE 4-2. Model Training & Test 2 - XGBRegressor:", time.process_time())
### 결과 - R2 Score of the Gradient Boosting Model(XGBoost): -0.015027890476425387




#3-3. 모델 선택 및 전체 데이터셋으로 최종 모델 학습
### 시간관계상 SearchCV 메소드를 이용한 하이퍼파라미터 튜닝은 생략

X_whole = df[features]
y_whole = df[target]

if randomforest_score >= xgboost_score:
    best_model = model_1
    print("Best Model: Random Forest")
else:
    best_model = model_2
    print("Best Model: Gradient Boosting(XGBoost)")

ttr_final = TransformedTargetRegressor(
    regressor=best_model, 
    func=np.log1p, 
    inverse_func=np.expm1
)
ttr_final.fit(X_whole, y_whole)

print("Elapsed Time of STAGE 4-3. Final Model Training:", time.process_time())




#3-4. 모델 pickling

with open('model.pkl','wb') as pickle_file:
    pickle.dump(ttr_final, pickle_file)

print("Elapsed Time of STAGE 4-4. Model Encoding:", time.process_time())