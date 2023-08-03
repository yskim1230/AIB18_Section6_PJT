'''
pip install streamlit
pip install mysql-connector-python
pip install streamlit-aggrid #데이터프레임안에 체크박스 넣는 기능
'''

import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import mysql.connector
from datetime import time, datetime, date
from st_aggrid import AgGrid, GridUpdateMode #데이터프레임안에 체크박스 넣는 메소드
from st_aggrid.grid_options_builder import GridOptionsBuilder #데이터프레임안에 체크박스 넣는 메소드

##############################
#########탭 생성###########
##############################
tab_titles = ['서비스', '결과', '예측']
tabs = st.tabs(tab_titles)

##############################
#########서비스탭시작###########
##############################


#####전역변수 설정#####
global_selected_rows = None         # 서비스탭에서 왕복항공권을 결과탭으로 보내주기 위한 전역변수
global_selected_rows_hotel = None   # 서비스탭에서 왕복항공권을 결과탭으로 보내주기 위한 전역변수
#recommendation1 = None              # 호텔추천 전역변수
#recommendation2 = None              # 호텔추천 전역변수


with tabs[0]: #서비스탭#
    st.header('플래닝이 싫은 P들을 위해, 쉽게 여행가DA')
    st.write(' ')

    # 출발지/도착지 탭 생성

    departure = st.selectbox(
        '출발지 DEPARTURE',
        ('인천국제공항(ICN)',))
    st.write(' ')

    arrival = st.selectbox(
        '도착지 ARRIVAL',
        ('간사이국제공항(KIX)',))
    st.write(' ')


    ##############################
    #########제목끝###########
    ##############################

    ##############################
    #########필터입력단시작###########
    ##############################

    # 출국날짜/귀국날짜 탭 생성

    #min_date = date.today()
    min_date = date(2023, 8, 1)
    max_date = date(2023, 8, 31)

    # 출발 날짜의 기본값을 8월 1일로 설정
    default_departure_date = datetime(datetime.now().year, 8, 1).date()

    # 도착 날짜의 기본값을 8월 3일로 설정
    default_return_date = datetime(datetime.now().year, 8, 3).date()

    date1 = st.date_input('출발하는 날짜 DEPARTURE DATE', min_value=min_date, max_value=max_date, value=default_departure_date)
    st.write(' ')

    date2 = st.date_input('돌아오는 날짜 RETURN DATE', min_value=min_date, max_value=max_date, value=default_return_date)
    st.write(' ')


    # 예산 슬라이더 생성
    budget = st.slider(
        '예산(원) BUDGET',
        0, 3000000, (500000, 1000000), step=10000)
    st.write(' ')

    # 벨런스 슬라이더 생성(기본값 50, 5단위 조정)
    balance = st.slider('여행 밸런스 (항공권 가격 비중)', 
                        min_value=0, max_value=100, value=50, step=5)
    st.write(' ')

    # 항공권 벨런스별 최소/최대금액
    balance_air = balance*0.01
    min_price_air = budget[0]*balance_air
    max_price_air = budget[1]*balance_air

    #숙박비 벨런스별 최대/최대금액
    balance_hotel = (100-balance)*0.01
    min_price_hotel = budget[0]*balance_hotel
    max_price_hotel = budget[1]*balance_hotel

    # 현지 교통패스 및 관광 옵션 탭 생성
    # 교통 데이터프레임 생성
    df_trans = pd.DataFrame(
        {
        "교통패스" : ["라피트 특급열차(편도)", "라피트 특급열차(왕복)"],
        "금액" : [9400,18000]
        }
    )
    # 관광지 데이터 프레임 생성
    df_site = pd.DataFrame(
        {
        "관광패스" : ['오사카 주유패스 1일', '오사카 주유패스 2일', '유니버설 스튜디오 재팬 1일', '유니버설 스튜디오 재팬 2일', '간사이 쓰루패스 2일', '간사이 쓰루패스 3일'],
        "금액" : [25500,33000,85500,162800,38700,47700]
        }
    )    
    # 교통패스 필터
    Trans_pass = df_trans['교통패스'].unique().tolist()
    option_trans = st.multiselect('교통패스', Trans_pass)
    
    Site_pass = df_site['관광패스'].unique().tolist()
    option_site = st.multiselect('관광패스', Site_pass)


    ##############################
    #########필터입력단 끝###########
    ##############################
    
    
    ##############################
    #########사이드바입력시작###########
    ##############################
    # 사이드 바 컨텐츠 생성
    st.sidebar.title("여행 꿀팁")
    st.sidebar.write(' ')
    st.sidebar.selectbox('궁금한 도시', ['오사카 OSAKA'])
    st.sidebar.write(' ')
    op = st.sidebar.checkbox('오사카 주유패스')
    usj = st.sidebar.checkbox('유니버설 스튜디오 재팬')
    kt = st.sidebar.checkbox('간사이 쓰루패스')

    if op:
        st.sidebar.write(' ')
        st.sidebar.subheader('오사카 주유패스')
        st.sidebar.write(' ')
        st.sidebar.write("""오사카 주유패스(Osaka Amazing Pass)는 일본 오사카(Osaka) 지역의 여행자들을 대상으로 제공되는 할인 혜택과 무료 입장을 포함하는 특별 패스입니다. 이 패스를 소지하면 오사카 지역 내의 주요 관광 명소와 교통 수단을 편리하게 이용할 수 있습니다.""")

    if usj: 
        st.sidebar.write(' ')
        st.sidebar.subheader('유니버설 스튜디오 재팬')
        st.sidebar.write(' ')
        st.sidebar.write("""유니버설 스튜디오 재팬(Universal Studios Japan, USJ)은 일본 오사카(Osaka)에 위치한 테마파크로, 유니버설 스튜디오를 기반으로 한 테마 기반의 어트랙션과 엔터테인먼트를 즐길 수 있는 인기 있는 관광 명소입니다. 유니버설 스튜디오 재팬은 세계적으로 유명한 영화와 TV 프로그램들을 기반으로 한 어트랙션과 라이드를 제공하며, 다양한 쇼와 퍼레이드, 먹거리 등이 있는 컴플리트한 테마파크입니다.""")

    if kt:
        st.sidebar.write(' ')
        st.sidebar.subheader('간사이 쓰루패스')
        st.sidebar.write(' ')
        st.sidebar.write("""간사이 쓰루패스(Kansai Thru Pass)는 일본의 간사이 지역(Kansai region)을 여행하는 관광객들을 대상으로 제공되는 교통 패스입니다. 이 패스를 소지하면 간사이 지역 내의 주요 교통 수단을 자유롭게 이용할 수 있습니다. 간사이 지역은 일본의 주요 관광 도시들이 모여 있는 지역으로, 오사카, 교토, 고베, 나라 등이 포함됩니다.""")

    ##############################
    #########사이드바입력끝###########
    ##############################

    ##############################
    #######데이터 호출 시작###########
    ##############################

    # MySQL 데이터베이스 연결
    def connect_to_database():
        try:
            conn = mysql.connector.connect(
                host='aibsection6pjt.cbodywvxd8v5.ap-northeast-2.rds.amazonaws.com',
                port=3306,
                user='admin',
                password='aibsection6pjt',
                database='aibsection6pjt'
            )
            return conn
        except Exception as e:
            st.error("데이터베이스에 연결하는 데 문제가 발생했습니다.")
            st.write(e)
            return None
    # MySQL 데이터베이스 연결 끝



    ####################    
    ######왕복항공권 SP호출#######
    ####################
    def call_gettrip(date1, date2, min_price_air, max_price_air):
        conn = connect_to_database()
        date1_str = date1.strftime('%Y%m%d')
        date2_str = date2.strftime('%Y%m%d')
        if conn:
            cursor = conn.cursor()
            try:
                # SP호출
                cursor.callproc("Gettrip", [date1_str, date2_str, min_price_air, max_price_air])
                # 데이터프레임으로 출력, 실패하면 오류 메세지
                for result in cursor.stored_results():
                    if result.with_rows:
                        # 호출된 데이터를 데이터 프레임형태로 출력
                        columns = {
                            'date_osa': '출국일자',
                            'airline_name_osa': '항공사(출국)',
                            'departure_time_osa': '출발시간(출국)',
                            'departure_location_osa': '출발지(출국)',
                            'arrival_time_osa': '도착시간(출국)',
                            'arrival_location_osa': '도착지(출국)',
                            'additional_info_osa': '비행시간(출국)',
                            'ticket_price_osa': '가격(출국)',
                            'seat_info_osa': '좌석정보(출국)',
                            'date_icn': '입국일자',
                            'airline_name_icn': '항공사(입국)',
                            'departure_time_icn': '출발시간(입국)',
                            'departure_location_icn': '출발지(입국)',
                            'arrival_time_icn': '도착시간(입국)',
                            'arrival_location_icn': '도착지(입국)',
                            'additional_info_icn': '비행시간(입국)',
                            'ticket_price_icn': '가격(입국)',
                            'seat_info_icn': '좌석정보(입국)',
                            'ticket_total': '가격(왕복)'
                        }
                        df = pd.DataFrame(result.fetchall(), columns=columns.keys())
                        df = df.rename(columns=columns)
                        
                        st.subheader("왕복항공권 추천")
                        st.write(f"항공권 예산 범위: {round(min_price_air)}원 ~ {round(max_price_air)}원")
                        
                        #항공사 출국/입국편 필터 추가
                        airlinedpt = df['항공사(출국)'].unique().tolist()
                        option_airdpt = st.multiselect('항공사(출국)', airlinedpt)

                        airlinearv = df['항공사(입국)'].unique().tolist()
                        option_airarv = st.multiselect('항공사(입국)', airlinearv)

                        # 항공사(출국)
                        if option_airdpt and not option_airarv:
                            df_date = df[df['항공사(출국)'].isin(option_airdpt)]
                        # 항공사(출국),항공사(입국)
                        elif option_airdpt and option_airarv:
                            df_date = df[df['항공사(출국)'].isin(option_airdpt) & df['항공사(입국)'].isin(option_airarv)]
                        # 항공사(입국)
                        elif not option_airdpt and option_airarv:
                            df_date = df[df['항공사(입국)'].isin(option_airarv)]
                        # 둘다 아님
                        else:
                            df_date = df
                        

                       
                        gd = GridOptionsBuilder.from_dataframe(df_date)
                        gd.configure_selection(selection_mode='multiple', use_checkbox=True)
                        gridoptions = gd.build()
                        grid_table = AgGrid(df_date, height=250, gridOptions=gridoptions,
                                            update_mode=GridUpdateMode.SELECTION_CHANGED)
                        st.markdown('<span style="color: red;"> 옆으로 넘기셔야 데이터가 다 보입니다.</span>', unsafe_allow_html=True)

                        st.write('선택하신 항공권')
                        # 함수 내에서 global_selected_rows 변수를 업데이트합니다.
                        global global_selected_rows
                        global_selected_rows = None 
                        global_selected_rows = grid_table["selected_rows"]

                        # "_selectedRowNodeInfo" 항목을 제거한 선택된 행을 표시합니다.
                        if global_selected_rows is not None:
                            selected_rows_without_info = []
                            for row in global_selected_rows:
                                row_without_info = {key: value for key, value in row.items() if key != '_selectedRowNodeInfo'}
                                selected_rows_without_info.append(row_without_info)
                            
                            st.dataframe(selected_rows_without_info)

                    else:
                        # 데이터가 없을 경우
                        messages = result.fetchall()
                        if messages:
                            st.error("Messages from Gettrip:")
                            st.write(messages)
                        else:
                            st.warning("출력할 데이터가 없습니다.")
            except Exception as e:
                conn.rollback()  
                st.error("에러발생")
                st.write(e)
            finally:
                # Close connection
                conn.close()


    ####################    
    ######왕복항공권 SP호출끝#######
    ####################


    ####################    
    ######오사카/인천/호텔DB#######
    ####################
    # 오사카행 정보 가져오기
    def get_osa():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TFESchedule_osa")
            users = cursor.fetchall()
            conn.close()
            return users
        else:
            return None

    # 인천행 항공권 정보 가져오기
    def get_icn():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TFEschedule_icn")
            users = cursor.fetchall()
            conn.close()
            return users
        else:
            return None
    # 호텔정보가져오기
    def get_hotel():
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TDAHotel")
            users = cursor.fetchall()
            conn.close()
            return users
        else:
            return None
    ####################    
    ######오사카/인천/호텔DB끝#######
    ####################

    ##############################
    #######데이터 호출 끝###########
    ##############################

    ##################################    
    ######오사카/인천/호텔 화면디자인시작#######
    ##################################
    # 오사카행 호출
    def osa():
        # 데이터베이스에서 사용자 정보 가져오기
        users = get_osa()
        # 사용자 정보 표시
        if users:
            with st.expander('더 많은 오사카행 항공권 정보를 원하시나요?'):
                st.write(' ')
                df = pd.DataFrame(users, columns=['날짜', '항공사', '출발시간', '출발지', '도착시간', '도착지', '비행시간', '가격', '좌석정보'])
                date1_str = date1.strftime('%Y%m%d')
                df_date = df[df['날짜'] == date1_str]
                airline = df['항공사'].unique().tolist()
                option_air = st.multiselect('항공사 AIRLINE', airline)
                if option_air:
                    df_date = df_date[df_date['항공사'].isin(option_air)]
                st.write('출국일자 : ',date1_str)
                st.dataframe(df_date,hide_index=True)
                
        else:
            st.warning("데이터베이스 연결에 실패했습니다.")

    # 인천행 호출
    def icn():
        # 데이터베이스에서 사용자 정보 가져오기
        users = get_icn()
        # 사용자 정보 표시
        if users:
            with st.expander('더 많은 인천행 항공권 정보를 원하시나요?'):
                st.write(' ')
                df = pd.DataFrame(users, columns=['날짜', '항공사', '출발시간', '출발지', '도착시간', '도착지', '비행시간', '가격', '좌석정보'])
                date2_str = date2.strftime('%Y%m%d')
                df_date = df[df['날짜'] == date2_str]
                airline = df['항공사'].unique().tolist()
                option_air = st.multiselect('항공사 AIRLINE', airline)
                if option_air:
                    df_date = df_date[df_date['항공사'].isin(option_air)]
                st.write('귀국일자 : ',date2_str)
                st.dataframe(df_date,hide_index=True)
        else:
            st.warning("데이터베이스 연결에 실패했습니다.")

    def hotel(min_price_hotel, max_price_hotel):
        # 데이터베이스에서 사용자 정보 가져오기
        global recommendation1, recommendation2  # 변수를 전역 변수로 선언
        users = get_hotel()
        # 사용자 정보 표시
        if users:
            st.subheader("숙박 정보")
            st.write(f"호텔 예산 범위: {round(min_price_hotel)}원 ~ {round(max_price_hotel)}원")
            df = pd.DataFrame(users, columns=['체크인 날짜', '체크아웃 날짜', '호텔명', '위치', '평점', '호텔 등급', '가격', '링크'])
            balance_hotel = (100-balance)*0.01
            date1_int = int(date1.strftime('%Y%m%d'))
            date2_int = int(date2.strftime('%Y%m%d'))
            df['체크인 날짜'] = df['체크인 날짜'].astype(int)
            df = df[(df['체크인 날짜'] >= date1_int) & (df['체크인 날짜'] <= date2_int)]
            df['체크인 날짜'] = df['체크인 날짜'].astype(str)
            df['체크인 날짜'] = pd.to_datetime(df['체크인 날짜'], format='%Y%m%d')
            available_hotels = df.groupby('호텔명').filter(lambda x: x['체크인 날짜'].nunique() == date2_int - date1_int)['호텔명'].unique()
            available_hotels = df[df['호텔명'].isin(available_hotels)].groupby(['호텔명', '호텔 등급', '평점', '링크'])['가격'].sum().reset_index()
            available_hotels = available_hotels[(available_hotels['가격'] >= min_price_hotel)
                                                & (available_hotels['가격'] <= max_price_hotel)].sort_values(by='평점', ascending=False).reset_index()
            available_hotels = available_hotels.iloc[:, 1:]

            # 조건에 맞는 호텔이 없을 때 메시지 출력
            if len(available_hotels) == 0:
                st.warning("조건에 맞는 호텔이 없습니다.")
            else:
                        gd = GridOptionsBuilder.from_dataframe(available_hotels)
                        gd.configure_selection(selection_mode='multiple', use_checkbox=True)
                        gridoptions = gd.build()
                        grid_table = AgGrid(available_hotels, height=250, gridOptions=gridoptions,
                                            update_mode=GridUpdateMode.SELECTION_CHANGED)
                        st.markdown('<span style="color: red;"> 옆으로 넘기셔야 데이터가 다 보입니다.</span>', unsafe_allow_html=True)

                        st.write('선택하신 호텔')
                        # 함수 내에서 global_selected_rows_hotel 변수를 업데이트합니다.
                        global global_selected_rows_hotel
                        global_selected_rows_hotel = None 
                        global_selected_rows_hotel = grid_table["selected_rows"]
                        
                        # "_selectedRowNodeInfo" 항목을 제거한 선택된 호텔 행을 표시합니다.
                        if global_selected_rows_hotel is not None:
                            selected_hotel_without_info = []
                            for row in global_selected_rows_hotel:
                                row_without_info = {key: value for key, value in row.items() if key not in ['index', '_selectedRowNodeInfo', '링크']}
                                selected_hotel_without_info.append(row_without_info)
                            
                            st.dataframe(selected_hotel_without_info, hide_index=True)
        else:
            st.warning("데이터베이스 연결에 실패했습니다.")



   
    ##################################    
    ######오사카/인천/호텔 화면디자인끝#######
    ##################################

    ####################    
    ######출력부분 시작#######
    ####################


    # 특정 세션 상태를 유지하기 위해 st.session_state를 초기화합니다.
    if "search_clicked" not in st.session_state:
        st.session_state["search_clicked"] = False

    # 2차 화면 생성
    search_clicked = True

    # 2차 화면 생성
    if st.session_state.search_clicked:
        min_price_air = budget[0]*balance_air
        max_price_air = budget[1]*balance_air
        min_price_air = budget[0]*balance_air
        max_price_air = budget[1]*balance_air
        st.write('')
        st.write('')
        st.write('')
        call_gettrip(date1, date2, min_price_air, max_price_air)   # 왕복항공권
        st.write('')
        osa()                                                      # 오사카행 정보
        st.write('')
        icn()                                                      # 인천행 정보
        st.write('')
        st.write('')
        hotel(min_price_hotel, max_price_hotel)                    # 호텔정보

    # 출력 버튼 생성
    searchbutton = st.button('검색')

    if searchbutton:
        st.session_state.search_clicked = True  

    st.write('<span style="color: red;"> \n 검색 버튼 클릭 후 결과 확인을 위하여 결과 탭으로 이동해주세요.</span>', unsafe_allow_html=True) 

##############################
#########서비스탭끝###########
##############################




##############################
#########결과탭시작###########
##############################
with tabs[1]: #서비스탭#
    # 왕복항공권 선택
    if global_selected_rows:
        # DataFrame으로 변환하여 원하는 컬럼만 선택하여 테이블 형태로 출력합니다.
        df_selected_rows = pd.DataFrame(global_selected_rows)
        selected_columns = ['항공사(출국)','출국일자', '출발시간(출국)', '도착시간(출국)', '가격(출국)','항공사(입국)','입국일자', '출발시간(입국)','도착시간(입국)', '가격(입국)','가격(왕복)']
        df_selected_columns = df_selected_rows[selected_columns]
        global RoundTripPrice
        RoundTripPrice = df_selected_columns['가격(왕복)']
        st.dataframe(df_selected_columns)
    else:
        st.warning("아직 선택된 항공권이 없습니다.")
        RoundTripPrice = None
    # 호텔 선택
    if global_selected_rows_hotel:
        # DataFrame으로 변환하여 원하는 컬럼만 선택하여 테이블 형태로 출력합니다.
        df_selected_rows_hotel = pd.DataFrame(global_selected_rows_hotel)
        selected_columns_hotel = ['호텔명','호텔 등급','평점','가격','링크']
        df_selected_columns_hotel = df_selected_rows_hotel[selected_columns_hotel]
        global HotelPrice
        HotelPrice = df_selected_columns_hotel['가격']
        st.dataframe(df_selected_columns_hotel)
        for index, row in df_selected_columns_hotel.iterrows():
            st.image(row['링크'], use_column_width=True)
    else:
        st.warning("아직 선택된 호텔이 없습니다.")
        HotelPrice = None
    # 교통패스 선택
    if option_trans:
        # 사용자가 선택한 교통패스에 대한 이름과 금액 표시
        selected_trans_passes = df_trans[df_trans['교통패스'].isin(option_trans)]
        global TransPrice
        TransPrice = selected_trans_passes['금액']
        st.subheader("선택한 교통패스:")
        st.table(selected_trans_passes)
    else:
       TransPrice = None

    # 관광지 선택
    if option_site:
        # 사용자가 선택한 관광패스에 대한 이름과 금액 표시
        selected_site_passes = df_site[df_site['관광패스'].isin(option_site)]
        global SitePrice
        SitePrice = selected_site_passes['금액']
        st.subheader("선택한 관광패스:")
        st.table(selected_site_passes)
    else:
        SitePrice = None
    
    # 사용자가 선택한 항목에 대한 금액 합계 추가
    if RoundTripPrice is not None and HotelPrice is not None and TransPrice is not None and SitePrice is not None:
        total_price = RoundTripPrice.sum() + HotelPrice.sum() + TransPrice.sum() + SitePrice.sum()
        st.subheader("선택한 옵션들의 금액 합계:")
        st.table(pd.DataFrame({"항목": ["왕복항공권", "호텔", "교통패스", "관광패스", "총 합계"], "금액": [RoundTripPrice.sum(), HotelPrice.sum(), TransPrice.sum(), SitePrice.sum(), total_price]}))
        st.metric(label="선택하신 옵션들의 비용은", value=f"{total_price}원")
        # CSV 파일로 다운로드하는 버튼 추가
        df_summary = pd.DataFrame({"항목": ["왕복항공권", "호텔", "교통패스", "관광패스", "총 합계"], "금액": total_price})
        csv_data = df_summary.to_csv(index=False).encode('utf-8')
        st.download_button("옵션별_금액_합계_다운로드.csv", csv_data, mime='text/csv')
##############################
#########결과탭끝###########
##############################


##############################
#########예측탭시작###########
##############################
with tabs[2]: #예측탭#
    import pickle
    import requests
    import streamlit as st
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor

    def load_model_from_github(raw_url):
        try:
            response = requests.get(raw_url)
            response.raise_for_status()  # 요청이 성공적으로 완료되었는지 확인

            # 파일을 바이너리 모드로 열기
            loaded_model = pickle.loads(response.content, encoding='latin1')
            return loaded_model

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            st.write(f'HTTP error occurred: {http_err}')
            return None
        except requests.exceptions.RequestException as req_err:
            print(f'Request error occurred: {req_err}')
            st.write(f'Request error occurred: {req_err}')
            return None
        except pickle.UnpicklingError as pick_err:
            print(f'Unpickling error occurred: {pick_err}')
            st.write(f'Unpickling error occurred: {pick_err}')
            return None
        except Exception as err:
            print(f'Error occurred: {err}')
            st.write(f'Error occurred: {err}')
            return None


    github_raw_url = 'https://github.com/yskim1230/AIB18Section6PJT_MODEL/raw/main/incheon_osaka_Premium_standard.pkl'

    model = load_model_from_github(github_raw_url)

    st.write("""
    # 항공권 가격 예측 서비스
    Enter the details of the airline ticket you want to purchase and get an estimated price!
    """)

    ordered_columns = ['date', 'departure_time', 'arrival_time', 'airline_name_ANA',
        'airline_name_대한항공', 'airline_name_아시아나항공', 'airline_name_일본항공',
        'airline_name_제주항공', 'airline_name_티웨이항공', 'airline_name_한에어',
        'weekday', 'holiday']

    def preprocess(input_data):
        # 'weekday' 컬럼 추가 (변환 전 'date' 컬럼에서 직접 추출)
        input_data['weekday'] = pd.to_datetime(input_data['date'], format='%Y%m%d').dt.dayofweek
        
        # 'date'를 datetime 형태로 변환하고, 'day of year'로 변환
        input_data['date'] = pd.to_datetime(input_data['date'], format='%Y%m%d').dt.dayofyear
        
        # 'departure_time'과 'arrival_time'을 시간 단위로 변환
        input_data['departure_time'] = pd.to_numeric(input_data['departure_time'])
        input_data['arrival_time'] = pd.to_numeric(input_data['arrival_time'])
        
        # 'airline_name' 항목을 one-hot encoding으로 변환
        airline_options = ['ANA', '대한항공', '아시아나항공', '일본항공', '제주항공', '티웨이항공', '한에어']
        airline_encoded = pd.DataFrame(columns=[f'airline_name_{option}' for option in airline_options], data=[[0]*len(airline_options)])
        airline_encoded.loc[0, f'airline_name_{input_data["airline"].iloc[0]}'] = 1
        input_data.drop('airline', axis=1, inplace=True)
        
        # 'holiday' 컬럼 추가 (기본값: 0)
        input_data['holiday'] = [0] * len(input_data)  
        
        input_data = pd.concat([input_data, airline_encoded], axis=1)  # Fix concatenation

        # 컬럼 순서 재배열
        ordered_columns = ['date', 'departure_time', 'arrival_time', 'airline_name_ANA',
        'airline_name_대한항공', 'airline_name_아시아나항공', 'airline_name_일본항공',
        'airline_name_제주항공', 'airline_name_티웨이항공', 'airline_name_한에어',
        'weekday', 'holiday']
        input_data = input_data.reindex(columns=ordered_columns)

        return input_data


    #예측 익스팬더
    
    with st.expander('어떻게 떠나실 건가요?'):
        departure_time = st.slider('Departure Time', 0, 24, 12)
        arrival_time = st.slider('Arrival Time', 0, 24, 12)
        airline = st.selectbox('Airline', ['ANA', '대한항공', '아시아나항공', '일본항공', '제주항공', '티웨이항공', '한에어'])

        date = st.date_input('Date')

    st.write('')
    ok = st.button("가격 예측")
    if ok:
        input_data = pd.DataFrame({
            'departure_time': [departure_time],
            'arrival_time': [arrival_time],
            'airline': [airline],
            'date': [date]
        })

        processed_data = preprocess(input_data)
        predicted_price = model.predict(processed_data)
        st.write(f"예측가격은  {int(predicted_price[0])}원 입니다.")
##############################
#########예측탭끝###########
##############################
