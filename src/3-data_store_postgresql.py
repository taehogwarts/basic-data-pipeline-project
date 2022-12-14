import pandas as pd
# import csv

import os
import psycopg2
import time


#0. Amazon RDS 서버 연결

host = os.getenv('host')
database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')


connection = psycopg2.connect(
    host=host,
    database=database, 
    user=user, 
    password=password
)

print("Elapsed Time of STAGE 0. Database-Connection:", time.process_time())



#1. CSV 파일 읽어온 후 전처리


#1-1. 진료내역 정보 CSV 파일 읽어오기

CSV_FILEPATH_1 = os.path.join(os.getcwd(), 'dataset/HP_T20_2020_1.csv') 
CSV_FILEPATH_2 = os.path.join(os.getcwd(), 'dataset/HP_T20_2020_2.csv') 
CSV_FILEPATH_3 = os.path.join(os.getcwd(), 'dataset/HP_T20_2020_3.csv') 


### Pandas 사용 시

treatment_records_columns_list = ['성별코드', '연령대코드', '시도코드', '진료과목코드', '주상병코드', '요양일수', '심결본인부담금']

df1 = pd.read_csv(CSV_FILEPATH_1, encoding='cp949')
# print(df1.head())
df1 = df1[treatment_records_columns_list]
# print(df1.head())

df2 = pd.read_csv(CSV_FILEPATH_2, encoding='cp949')
df2 = df2[treatment_records_columns_list]

df3 = pd.read_csv(CSV_FILEPATH_3, encoding='cp949')
df3 = df3[treatment_records_columns_list]

treatment_records_df = pd.concat([df1, df2, df3])
treatment_records_df.columns = ['GenderCode', 'AgeCode', 'AreaCode', 'ClinicCode', 'DiseaseCode', 
                'TreatmentPeriod_Days', 'MedicalExpenses_Won']





#1-2. 상병코드 정보 CSV 파일 읽어오기


CSV_FILEPATH_4 = os.path.join(os.getcwd(), 'dataset/disease_code_20210101.csv')

disease_columns_list = ['상병기호', '한글명', '영문명']

df = pd.read_csv(CSV_FILEPATH_4, encoding='cp949')
disease_df = df[disease_columns_list]
disease_df.columns = ['DiseaseCode', 'DiseaseName_Kor', 'DiseaseName_Eng']

### 작은따옴표 때문에 아래 적재 과정에서 syntax error 나서 replace
### str 빼고 하면 오류 안 나도 replace 자체가 안 되는 듯...
### caveats: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
disease_df.loc[:, ('DiseaseName_Eng')] = disease_df.loc[:, ('DiseaseName_Eng')].str.replace("'", "`")

# print(disease_df.info())
# print(disease_df.head())





#1-3. 시도코드 정보 dataframe 생성

area_columns_list = ['AreaCode', 'AreaName']

area_data_matrix = [
    [11, '서울특별시'], 
    [26, '부산광역시'], [27, '대구광역시'], [28, '인천광역시'], [29, '광주광역시'], [30, '대전광역시'], [31, '울산광역시'], 
    [36, '세종특별자치시'], 
    [41, '경기도'], [42, '강원도'], [43, '충청북도'], [44, '충청남도'], [45, '전라북도'], [46, '전라남도'], [47, '경상북도'], [48, '경상남도'], 
    [49, '제주특별자치도']
]

area_df = pd.DataFrame(data=area_data_matrix, columns=area_columns_list)

# print(area_df.info())
# print(area_df.head())






#1-4. 진료과목코드 정보 dataframe 생성

clinic_columns_list = ['ClinicCode', 'ClinicName']

clinic_data_matrix = [
    [0, '일반의'], [1, '내과'], [2, '신경과'], [3, '정신건강의학과'], [4, '외과'], [5, '정형외과'], [6, '신경외과'], [7, '흉부외과'], 
    [8, '성형외과'], [9, '마취통증의학과'], [10, '산부인과'], [11, '소아청소년과'], [12, '안과'], [13, '이비인후과'], [14, '피부과'], 
    [15, '비뇨기과'], [16, '영상의학과'], [17, '방사선종양학과'], [18, '병리과'], [19, '진단검사의학과'], [20, '결핵과'], [21, '재활의학과'], 
    [22, '핵의학과'], [23, '가정의학과'], [24, '응급의학과'], [25, '산업의학과'], [26, '예방의학과'], 
    [50, '구강악안면외과'], [51, '치과보철과'], [52, '치과교정과'], [53, '소아치과'], [54, '치주과'], [55, '치과보존과'], [56, '구강내과'], 
    [57, '구강악안면방사선과'], [58, '구강병리과'], [59, '예방치과'], 
    [80, '한방내과'], [81, '한방부인과'], [82, '한방소아과'], [83, '한방안과, 한방이비인후과'], [84, '한방신경정신과'], [85, '침구과'], 
    [86, '한방재활의학과'], [87, '사상체질과'], [88, '한방응급의학과']
]

clinic_df = pd.DataFrame(data=clinic_data_matrix, columns=clinic_columns_list)

# print(clinic_df.info())
# print(clinic_df.head())





#1-5. 연령대코드 정보 dataframe 생성

age_columns_list = ['AgeCode', 'AgeName']
age_data_matrix = [
    [1, '0~4세'], [2, '5~9세'], [3, '10~14세'], [4, '15~19세'], [5, '20~24세'], [6, '25~29세'], [7, '30~34세'],
    [8, '35~39세'], [9, '40~44세'], [10, '45~49세'], [11, '50~54세'], [12, '55~59세'], [13, '60~64세'], [14, '65~69세'], 
    [15, '70~74세'], [16, '75~79세'], [17, '80~84세'], [18, '85세+']
]

age_df = pd.DataFrame(data=age_data_matrix, columns=age_columns_list)

# print(age_df.info())
# print(age_df.head())


print("Elapsed Time of STAGE 1. Data-Pull:", time.process_time())






#2. RDB 파일에 적재


#2-1. 테이블 생성

cursor = connection.cursor()

table_name_1 = 'TreatmentRecords'
table_name_2 = 'Disease'
table_name_3 = 'Area'
table_name_4 = 'Clinic'
table_name_5 = 'Age'

cursor.execute(
    f"""DROP TABLE IF EXISTS {
        table_name_1
        }
    ;"""
)
cursor.execute(
    f"""DROP TABLE IF EXISTS {
        table_name_2
        }
    ;"""
)
cursor.execute(
    f"""DROP TABLE IF EXISTS {
        table_name_3
        }
    ;"""
)
cursor.execute(
    f"""DROP TABLE IF EXISTS {
        table_name_4
        }
    ;"""
)
cursor.execute(
    f"""DROP TABLE IF EXISTS {
        table_name_5
        }
    ;"""
)

cursor.execute(
    f"""CREATE TABLE {
        table_name_1
        } (
            RecordID SERIAL PRIMARY KEY,
            {treatment_records_df.columns[0]} INTEGER, 
            {treatment_records_df.columns[1]} INTEGER, 
            {treatment_records_df.columns[2]} INTEGER, 
            {treatment_records_df.columns[3]} INTEGER, 
            {treatment_records_df.columns[4]} VARCHAR,
            {treatment_records_df.columns[5]} INTEGER, 
            {treatment_records_df.columns[6]} INTEGER
        )
    ;"""
)
# FOREIGN KEY - sqlite와 많이 달라서 일단 설정 안 하고 나중에 join할 때만 쓰기로

cursor.execute(
    f"""CREATE TABLE {
        table_name_2
        } (
            {disease_df.columns[0]} VARCHAR PRIMARY KEY, 
            {disease_df.columns[1]} VARCHAR, 
            {disease_df.columns[2]} VARCHAR
        )
    ;"""
)

cursor.execute(
    f"""CREATE TABLE {
        table_name_3
        } (
            {area_df.columns[0]} INTEGER PRIMARY KEY, 
            {area_df.columns[1]} VARCHAR
        )
    ;"""
)

cursor.execute(
    f"""CREATE TABLE {
        table_name_4
        } (
            {clinic_df.columns[0]} INTEGER PRIMARY KEY, 
            {clinic_df.columns[1]} VARCHAR
        )
    ;"""
)

cursor.execute(
    f"""CREATE TABLE {
        table_name_5
        } (
            {age_df.columns[0]} INTEGER PRIMARY KEY, 
            {age_df.columns[1]} VARCHAR
        )
    ;"""
)

connection.commit()




#2-2. 데이터셋 테이블에 저장

treatment_records_columns_list = treatment_records_df.columns
for i in range(len(treatment_records_df)):
    row_list = list(
        treatment_records_df.iloc[i]
    )
    cursor.execute(
        f"""INSERT INTO {
            table_name_1
        } (
            {treatment_records_columns_list[0]}, 
            {treatment_records_columns_list[1]}, 
            {treatment_records_columns_list[2]}, 
            {treatment_records_columns_list[3]}, 
            {treatment_records_columns_list[4]}, 
            {treatment_records_columns_list[5]}, 
            {treatment_records_columns_list[6]}
        ) VALUES (
            '{row_list[0]}', 
            '{row_list[1]}', 
            '{row_list[2]}', 
            '{row_list[3]}', 
            '{row_list[4]}', 
            '{row_list[5]}', 
            '{row_list[6]}'
        )
        ;"""
    )
connection.commit()

disease_columns_list = disease_df.columns
for i in range(len(disease_df)):
    row_list = list(
        disease_df.iloc[i]
    )
    cursor.execute(
        f"""INSERT INTO {
            table_name_2
        } (
            {disease_columns_list[0]}, 
            {disease_columns_list[1]}, 
            {disease_columns_list[2]}
        ) VALUES (
            '{row_list[0]}', 
            '{row_list[1]}', 
            '{row_list[2]}'
        )
        ON CONFLICT ON CONSTRAINT {disease_columns_list[0]}
        DO NOTHING
        ;"""
    )
connection.commit()

for i in range(len(area_df)):
    row_list = list(
        area_df.iloc[i]
    )
    cursor.execute(
        f"""INSERT INTO {
            table_name_3
        } (
            {area_columns_list[0]}, 
            {area_columns_list[1]}
        ) VALUES (
            '{row_list[0]}', 
            '{row_list[1]}'
        )
        ;"""
    )
connection.commit()

for i in range(len(clinic_df)):
    row_list = list(
        clinic_df.iloc[i]
    )
    cursor.execute(
        f"""INSERT INTO {
            table_name_4
        } (
            {clinic_columns_list[0]}, 
            {clinic_columns_list[1]}
        ) VALUES (
            '{row_list[0]}', 
            '{row_list[1]}'
        )
        ;"""
    )
connection.commit()

for i in range(len(age_df)):
    row_list = list(
        age_df.iloc[i]
    )
    cursor.execute(
        f"""INSERT INTO {
            table_name_5
        } (
            {age_columns_list[0]}, 
            {age_columns_list[1]}
        ) VALUES (
            '{row_list[0]}', 
            '{row_list[1]}'
        )
        ;"""
    )
connection.commit()

cursor.close()
connection.close()

print("Elapsed Time of STAGE 2. Data-Storing:", time.process_time())