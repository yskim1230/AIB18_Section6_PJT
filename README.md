# AIB18_Section6_PJT
# AIB18기 DA 5팀 - 여행하DA


---------
### 프로젝트 기간 : 2023.07.19 ~ 2023.08.01
### 프로젝트 도구 : Selenium, Mysql, DBeaver, Pandas, Tableau, StreamLit
### 사용언어 : Python, SQL
---------


## 조원 및 전담 파트
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
# 프로젝트 배경
* 항공권, 숙박비, 관광지 비용 등 따로 흩어져 있는 데이터 정보를 검색하기 어려워하는 사람들을 위해 최대한 간편하게 검색할 수 있는 서비스를 제작

# 프로젝트 개요
* 사용자들이 여행하고자 하는 목적지에 대한 항공권, 숙박비용 정보를 최대한 간단한 작업으로 대략적인 정보를 제공해주는게 목적
* 8월 왕복 항공권 정보, 방문지역 숙박 정보, 관광지 비용 등을 웹 스크래핑을 통해 데이터 수집
* 수집된 데이터를 토대로 가설 설정 및 Tableau 이용한 시각화
* Streamlit을 통한 웹 서비스 구현
* 8월 항공권 가격을 토대로 가격예측 모델 제시

# 프로젝트 기술스택
* Web Scraping
  - Selenium, Python, Pandas
    
* DataBase
  - Mysql
    
* Tools
  - Git
  - StreamLit
  - Tableau
------------------


# 프로젝트 진행과정
* 네이버 항공권 예약, 네이버 호텔 예약에서 데이터 스크래핑(셀레니움) 진행
* 8월 오사카 지역 항공권 금액, 출발일자, 출발시간, 도착일자, 도착시간등을 수집, 숙박정보도 호텔 이름, 가격, 평점, 성급 등을 수집
* 수집한 데이터들을 Pandas를 통해 정제
* 정제된 데이터를 CSV형태로 변환 후 AWS에 구축된 Mysql에 데이터를 적재
* StreamLit을 통핸 Front 구현 및 DB 연결을 통한 데이터 조회 기능 구현
* 가격 예측 모델(RandomForest) 구현 후 StreamLit에 삽입
* 도출된 데이터를 기반으로 Tableau 사용하여 이용자에게 설득력 있는 시각화 자료 제공

# 프로젝트 흐름도
<img width="906" alt="흐름도" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/ef231632-6cba-4393-8710-d1b4db0e49b6">


# 프로젝트 구현내용
## 1.데이터 크롤링 
### (1) 항공권
<img width="986" alt="항공권 크롤링1" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/985611b3-07a6-49d1-8892-ff8a9dd234c8">
<img width="1045" alt="항공권크롤링2" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/9280d7cf-a0cb-4663-96dc-49e39946fa09">

### (2) 호텔정보
<img width="999" alt="호텔크롤링" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/7fc71170-870c-4bf6-9d1c-22d24ca19853">

## 2. Pandas를 이용하여 데이터 정제 및 csv 파일로 변환
<img width="835" alt="EDA완료" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/c70f31d6-328d-4419-a8af-f8f7810c68ed">


## 3. 데이터 적재
### (1) AWS에 Mysql 구축
<img width="1457" alt="aws" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/ebe6f657-36d1-4bd4-81c2-8aa39dd93521">

### (2) Mysql에 데이터 업로드
<img width="940" alt="DB적재" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/d21262bc-cf9b-4eae-97f8-cfededc05bf5">

## 4. StreamLit 을 이용한 서비스 구현

### (1) 왕복항공권 추천, 호텔 추천 서비스
<img width="728" alt="서비스구현1" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/1a31e188-f300-48a5-989b-dd06bdd4d9fa">

<img width="732" alt="서비스구현2" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/655aede9-66f4-4af5-bbf5-1ce2819d9cc5">

<img width="736" alt="서비스구현3" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/3fa5bcc2-9e07-4d25-b0b1-631e104ff22f">

### (2) 결과 조회 서비스
<img width="725" alt="서비스구현4" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/82a76579-27ba-4194-834e-9ffdb55e002d">

<img width="703" alt="서비스구현5" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/af61567a-8a35-4b77-8fff-c5d6a7980aea">

### (3) 8월 항공권 가격예측 서비스
<img width="723" alt="서비스구현6" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/612f59b1-4061-4970-9277-572fc019dc21">

## 5. Tableau 를 이용한 시각화
* URL : https://public.tableau.com/app/profile/.77693538/viz/_16904254566560/1
<img width="969" alt="tableau구현" src="https://github.com/yskim1230/AIB18_Section6_PJT/assets/124799967/c70f8897-0ecd-4a58-b44e-8d3a180ff7eb">


------------------------------

# 프로젝트 한계 및 개선방안
## 한계점
* 현재는 지역 한군데만 지원하기에 서비스 기능에 한계가 있다
* 데이터 양이 많지 않아 인사이트를 도출하는데 있어 한계가 있다.
* 기능 구현에 초점이 맞춰져 진행하다 보니 시각화, 분석, 예측 파트의 구현이 상대적으로 약했다

## 개선방안
* 서비스 지역을 늘려 다양한 지역에 대한 정보를 제공할 수 있게 한다.
* 렌터카 정보, 날씨, 호텔 유형 등 다양한 데이터를 수집을 진행한다.
* 사용자 입장에서 보기 편한 시각화 구성과 다양한 관점에서 데이터 분석을 진행하여 예측 모델링 제작을 위한 추가적인 특성 엔지니어링 작업을 진행한다.
  
