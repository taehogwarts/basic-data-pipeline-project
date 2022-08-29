# Basic Data Pipeline Project

## 프로젝트 개요
- 목적: 데이터 파이프라인 구축
- 세부 내용: 기본적인 데이터 가져오기, 데이터 적재, 머신러닝 예측 모델링, 웹 API 및 대시보드 구현

<br>

## 사용 데이터셋
### 테이블1(데이터셋): 2021년 건강보험 진료내역 정보
- 사용 CSV 파일 크기: 약 1GB
- 데이터 개수: 약 12,000,000개
- 추출 컬럼: 성별, 연령, 시도코드, 진료과목코드, 주상병코드, 요양일수, 심결본인부담금 (이상 7개)
- 출처: https://www.data.go.kr/data/15007115/fileData.do

### 테이블2: 질병코드 정보
- 원 데이터 개수: 약 45,000개
- 한 질병코드가 여러 개의 병명을 가진 경우 최초 데이터만 사용 -> 사용 데이터 개수: 약 21,000개
- 출처: https://www.data.go.kr/data/15067467/fileData.do

<br>

## 프로젝트 진행 과정 및 결과
- 사용 언어: `Python 3.8`
- 사용 컴퓨터: `MacBook Air (M1, 2020)`

### STAGE 1. Data-Pull
- 소스 코드: `1-data_pull_and_store.py`

### STAGE 2. Data-Storing
- 사용 DB: RDB - `SQLite`
- 생성 DB 파일 크기: 약 300MB
- 소스 코드: `1-data_pull_and_store.py`

### STAGE 3. Data Query & Preprocessing
- 후보 타겟: 요양일수, 심결본인부담금
- EDA 및 Data Wrangling 결과: 요양일수 -> 예측 모델링 어려울 것으로 판단 <br>(99%, 1% percentile 이상치로 제거 후 로그변환해도 right-skewed 분포 개선 안 됨)
- 최종 타겟: 심결본인부담금
- 소스 코드: `2-predictive_modeling.py`

### STAGE 4. Machine-Learning Modeling
- 특성: 성별, 연령, 시도코드(지역코드), 진료과목코드
- 타겟: 심결본인부담금
- 머신러닝 모델: 지도학습 회귀 모델
- 모델링 방법: 2-Way Holdout Method (TrainSet 0.75%, TestSet 0.25%)
- 테스트 모델: Random Forest, Gradient Boosting(`XGBoost`)
- 특이사항: 로그변환 - `sklearn TransformedTargetRegressor` 활용
- 최종 선택 모델: `XGBoost` (* 최종 모델 학습은 전체 데이터셋 사용)
- 소스 코드(모델별 성능값 포함): `2-predictive_modeling.py`
- 모델 인코딩 파일: `model.pkl`

### STAGE 5. Web API Building
- 사용 라이브러리: `flask`
- API endpoint: `/api/user`
- Keys: GenderCode, AgeCode, AreaCode, ClinicCode
- Values: 메인 페이지에서 안내
- 소스 코드: `flask_web_api`

### STAGE 6. Dashboard Building
- 사용하고자 했던 툴: Google Data Studio (*M1 Mac - Metabase 사용 불가)
- 특이사항 1: `SQLite` DB 미지원 -> DB의 모든 테이블을 `INNER JOIN` 후 CSV 파일로 출력하여 사용 -> 구글드라이브 업로드했으나 구글시트에서 읽지 못해서 실패 <br>(*소스 코드: `3-data_query_csv.py`)
- 특이사항 2: Amazon RDS, ElephantSQL(유료) 등에 `PostgreSQL`로 적재하여 사용하려 했으나 적재 시간이 너무 길어져서 실패 <br>(*소스 코드: `3-data_store_postgresql.py`)
- 동적으로 작동하는 대시보드 구현은 실패 -> 부족한 대로 `Pandas`, `Matplotlib`, `Seaborn` 등 파이썬 라이브러리로 시각화 <br>(#소스 코드: `3-data_pull_visualization.py`)

### STAGE 7. Web API Deploying
- 배포 플랫폼: Heroku
- 주소: https://basic-datapipeline.herokuapp.com
