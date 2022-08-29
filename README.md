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
- 데이터 개수: 약 45,000개
- 출처: https://www.data.go.kr/data/15067467/fileData.do

<br>

## 프로젝트 진행 과정
- 사용 언어: Python 3.8
- 데이터베이스 유형: SQLite
- 사용 컴퓨터: MacBook Air (M1, 2020)

### STAGE 1. Data-Pull
- 소스 코드: 1-data_pull_and_store.py

### STAGE 2. Data-Storing
- 생성 DB 파일 크기: 약 300MB
- 소스 코드: 1-data_pull_and_store.py

### STAGE 3. Data Query & Preprocessing
- 후보 타겟: 요양일수, 심결본인부담금
- EDA 및 Data Wrangling 결과: 요양일수 예측 모델링 어려울 것으로 판단(99%, 1% percentile 이상치로 제거 후 로그변환해도 right-skewed 분포 개선 안 됨)
- 최종 타겟: 심결본인부담금
- 소스 코드: 2-predictive_modeling.py

### STAGE 4. Machine-Learning Modeling
- 특성: 성별, 연령, 진료과목코드
- 타겟: 심결본인부담금
- 머신러닝 모델: 지도학습 회귀 모델
- 모델링 방법: 2-Way Holdout Method (TrainSet 0.75%, TestSet 0.25%)
- 테스트 모델: Random Forest, Gradient Boosting(XGBoost), Linear Regression, Ridge Regression
- 특이사항: 로그변환 - sklearn TransformedTargetRegressor 활용
- 최종 선택 모델: XGBoost (* 최종 모델 학습은 전체 데이터셋 사용)
- 소스 코드(모델별 성능값 포함): 2-predictive_modeling.py
- 모델 인코딩 : model.pkl

### STAGE 5. Web API Building
- API endpoint: /api/user
- Keys: Gender, Age, ClinicCode
- Values: 메인 페이지에서 안내

### STAGE 6. Dashboard Building



### STAGE 7. Web API Deploying


