# Basic Data Pipeline Project

## 프로젝트 개요
- 목적: 데이터 파이프라인 구축
- 수준: 기본적인 데이터 가져오기, 데이터 적재, 머신러닝 예측 모델링, 웹 API 및 대시보드 구현

<br>

## 사용 데이터셋
### 테이블1(데이터셋): 2021년 건강보험 진료내역 정보
- 데이터 갯수: 약 1천만개
- 사용 CSV 파일 크기: 약 1GB
- 사용 특성: 성별, 연령, 시도코드, 진료과목코드, 주상병코드, 요양일수, 심결본인부담금 (이상 7개)
- 출처: https://www.data.go.kr/data/15007115/fileData.do

### 테이블2: 질병코드 정보
- 출처: https://www.data.go.kr/data/15067467/fileData.do

<br>

## Python 코드
- 소요 시간 기준 컴퓨터: MacBook Air (M1, 2020)

### STAGE 1. Data-Pull & Preprocessing
- 소요 시간: 약 19초
- 코드 파일: 1-data_pull_and_store.py

### STAGE 2. Data-Storing
- 소요 시간: 약 12분
- 생성 DB 파일 크기: 약 300MB
- 코드 파일: 1-data_pull_and_store.py