# AIB18_Section6_PJT
# AIB18기 DA 5팀 - 여행하DA


---------
### 프로젝트 기간 : 2023.07.19 ~ 2023.08.01
### 프로젝트 도구 : Selenium, Mysql, DBeaver, Pandas, Tableau, StreamLit
### 사용언어 : Python, SQL
---------


## 전담 파트
### 김영석 : 프로젝트 플래닝, 데이터 수집 및 적재 
### 김영준 : 시각화, 발표 자료 작성
### 김호인 : 웹 서비스 기능 구현
### 조영재 : 예측 모델링 작성


# 프로젝트명 : 플래닝이 싫은 P들을 위해, 쉽게가DA
## 서비스URL 
### https://aib18section6pjt-nt9inr96bi2mqlttsb2vaw.streamlit.app/

## 대시보드
### https://public.tableau.com/app/profile/.77693538/viz/_16904254566560/1?publish=yes

## 발표영상 다운링크
### https://drive.google.com/file/d/1K8VmY_8QAUu8N09pc7146G3k7y9OemZV/view?usp=drive_link

-------------------
## 프로젝트 배경
* 항공권, 숙박비, 관광지 비용 등 따로 흩어져 있는 데이터 정보를 검색하기 어려워하는 사람들을 위해 최대한 간편하게 검색할 수 있는 서비스를 제작

## 프로젝트 개요
* 사용자들이 여행하고자 하는 목적지에 대한 항공권, 숙박비용 정보를 최대한 간단한 작업으로 대략적인 정보를 제공해주는게 목적
* 8월 왕복 항공권 정보, 방문지역 숙박 정보, 관광지 비용 등을 웹 스크래핑을 통해 데이터 수집
* 수집된 데이터를 토대로 가설 설정 및 시각화
* 8월 항공권 가격을 토대로 가격예측 모델 제시

## 프로젝트 기술스택
* Web Scraping
  - Selenium, Python, Pandas
    
* DataBase
  - Mysql
    
* Tools
  - Git
  - StreamLit
  - Tableau


## 프로젝트 진행과정
* 네이버 항공권 예약, 네이버 호텔 예약에서 데이터 스크래핑(셀레니움) 진행
* 8월 오사카 지역 항공권 금액, 출발일자, 출발시간, 도착일자, 도착시간등을 수집, 숙박정보도 호텔 이름, 가격, 평점, 성급 등을 수집
* 수집한 데이터들을 Pandas를 통해 정제
* 정제된 데이터를 CSV형태로 변환 후 AWS에 구축된 Mysql에 데이터를 적재
* StreamLit을 통핸 Front 구현 및 DB 연결을 통한 데이터 조회 기능 구현
* 가격 예측 모델(RandomForest) 구현 후 StreamLit에 삽입
* 도출된 데이터를 기반으로 Tableau 사용하여 이용자에게 설득력 있는 시각화 자료 제공

## 프로젝트 흐름도
<img width="906" alt="흐름도" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/ef231632-6cba-4393-8710-d1b4db0e49b6">


## 프로젝트 구현내용

## 프로젝트 한계 및 개선방안

