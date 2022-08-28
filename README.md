# Basic Data Pipeline Project

## 프로젝트 개요
- 목적: 데이터 파이프라인 구축
- 세부 내용: 기본적인 데이터 가져오기, 데이터 적재, 머신러닝 예측 모델링, 웹 API 및 대시보드 구현

<br>

## 사용 데이터셋
### 테이블1(데이터셋): 2021년 건강보험 진료내역 정보
- 사용 CSV 파일 크기: 약 1GB
- 데이터 개수: 약 12,000,000개
- 사용 특성: 성별, 연령, 시도코드, 진료과목코드, 주상병코드, 요양일수, 심결본인부담금 (이상 7개)
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
- 소요 시간: 약 19초
- 소스 코드: 1-data_pull_and_store.py

### STAGE 2. Data-Storing
- 소요 시간: 약 11분
- 생성 DB 파일 크기: 약 300MB
- 소스 코드: 1-data_pull_and_store.py

### STAGE 3. Data Query & Preprocessing



### STAGE 4. Machine-Learning Modeling



### STAGE 5. Web API Building



### STAGE 6. Dashboard Building



### STAGE 7. Web API Deploying


