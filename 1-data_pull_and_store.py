import pandas as pd
# import csv

import os
import sqlite3


#1. CSV 파일 읽어온 후 전처리


#1-1. 진료내역 정보 CSV 파일 읽어오기

CSV_FILEPATH_1 = os.path.join(os.getcwd(), 'dataset/HP_T20_2020_1.csv') 
CSV_FILEPATH_2 = os.path.join(os.getcwd(), 'dataset/HP_T20_2020_2.csv') 
CSV_FILEPATH_3 = os.path.join(os.getcwd(), 'dataset/HP_T20_2020_3.csv') 


### Pandas 사용 시

public_health_columns_list = ['성별코드', '연령대코드', '시도코드', '진료과목코드', '주상병코드', '요양일수', '심결본인부담금']

df1 = pd.read_csv(CSV_FILEPATH_1, encoding='cp949')
# print(df1.head())
df1 = df1[public_health_columns_list]
# print(df1.head())

df2 = pd.read_csv(CSV_FILEPATH_2, encoding='cp949')
df2 = df2[public_health_columns_list]

df3 = pd.read_csv(CSV_FILEPATH_3, encoding='cp949')
df3 = df3[public_health_columns_list]

public_health_df = pd.concat([df1, df2, df3])
# public_health_df.to_csv('df.csv') ## --> csv 파일 용량이 대략 350mb 정도 나옴

# print(public_health_df.info())
# print(public_health_df.head())



# -------------------------------------------

### CSV 사용 시 (Pandas보다 느림)
# with open(CSV_FILEPATH_1, newline='', encoding='cp949') as csvfile:
#     dataset = list(csv.reader(csvfile))

#     columns = dataset[0]

#     ### 이유를 모르겠으나 아래 인덱스 불러오는 것에서 오류 남..
#     index_1 = columns.index('셩별코드')
#     index_2 = columns.index('연령대코드')
#     index_3 = columns.index('시도코드')
#     index_4 = columns.index('진료과목코드')
#     index_5 = columns.index('주상병코드')
#     index_6 = columns.index('요양일수')
#     index_7 = columns.index('심결본인부담금')

#     dataset = dataset[1:]
#     processed_dataset = []

#     for row in dataset:
#         selected_data = [
#             row[index_1], row[index_2], row[index_3], row[index_4], row[index_5], row[index_6], row[index_7]
#         ]
#         processed_dataset.append(selected_data)

# print(processed_dataset[0])
# print(len(processed_dataset))
# print(columns)

# -----------------------------------------



#1-2. 주상병코드 정보 CSV 파일 읽어오기


CSV_FILEPATH_4 = os.path.join(os.getcwd(), 'dataset/disease_code_20210101.csv')

disease_columns_list = ['상병기호', '한글명', '영문명']

df = pd.read_csv(CSV_FILEPATH_4, encoding='cp949')
disease_df = df[disease_columns_list]

# print(disease_df.info())
# print(disease_df.head())





#1-3. 시도코드 정보 dataframe 저장

area_columns_list = ['코드명', '시도명']

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






#1-4. 진료과목코드 정보 dataframe 저장

clinic_columns_list = ['코드명', '진료과목명']

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




#2. RDB 파일로 저장

# DB_FILENAME = 'public_health_info.db'
# DB_FILEPATH = os.path.join(os.getcwd(), 'database/'+DB_FILENAME)

# connection = sqlite3.connect(DB_FILEPATH)
# cursor = connection.cursor()

# table_name_1 = 'PublicHealthRecords'

# cursor.execute(
#     f"""CREATE TABLE {table_name_1} (
#         RecordId INTEGER NOT NULL PRIMARY KEY,
#         {public_health_columns_list[0]} INTEGER, 
#         {public_health_columns_list[1]} INTEGER, 
#         {public_health_columns_list[2]} INTEGER, 
#         {public_health_columns_list[3]} INTEGER, 
#         {public_health_columns_list[4]} NVARCHAR,
#         {public_health_columns_list[5]} INTEGER, 
#         {public_health_columns_list[6]} INTEGER, 



#     )
#     """)
### NVARCHAR은 일단 데이터 크기 지정 안 하고 만듦.



# table_name_2 = 'Disease'



# table_name_3 = 'Area'



# table_name_4 = 'Clinic'