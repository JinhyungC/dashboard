
import streamlit as st
st.set_page_config(layout='wide')

import pandas as pd

import datetime
import plotly.io as io
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.title(" 키워드 등장 빈도 ")

data_df = pd.read_csv("data.csv")

신문사 = [ "강원도민일보",       "경기일보",       "경향신문",       "국민일보",       "국제신문",       "대전일보",       "동아일보",
       "디지털타임스",       "매일경제",       "매일신문",       "머니투데이",       "문화일보",       "부산일보",       "서울경제",
       "서울신문",       "세계일보",       "전자신문",       "조선일보",       "조세일보",       "중앙일보",       "파이낸셜뉴스",
       "한겨레",       "한국경제",       "한국일보",       "헤럴드경제",       "조선비즈"]

방송사 = ["JTBC",       "KBS",       "MBC",
       "MBN",       "SBS",       "TV조선",
       "YTN",       "채널A",       "한국경제TV",       "연합뉴스TV",
       ]

통신사 = ["뉴스1",
       "뉴시스",
       "연합뉴스"
       ]


언론_종류_df = pd.DataFrame( 
    [
         신문사 + 방송사 + 통신사,
         ["신문사"] * len(신문사) + ["방송사"] * len(방송사) + ["통신사"] * len(통신사)
    ],
    index = ["언론사명", "종류"]                            
    ).T

news_data = pd.merge(data_df , 
                   언론_종류_df,
                   how = "left",
                   left_on = ["media1"], 
                   right_on = ["언론사명"])


#%% 시간 -> 일자 생성
news_data["date"] = pd.to_datetime( news_data.time.str[:10], format = "%Y-%m-%d" )
news_data["종류"] = news_data["종류"].fillna("기타")



#%%
negative_word_list = [ '유죄', '불법', '형벌', '리스크', '구속', '시세조종' ]

for text in negative_word_list:
    news_data[text + "_(등장_횟수)"] = news_data["content"].str.count(text)

#news_df["content"].str.contains("유죄") 해당 단어가 존재하는지 여부 0,1
#news_df["content"].str.count("유죄") 해당 단어가 등장하는 횟수

today = datetime.datetime.now()
start_date = datetime.date(2023, 9, 1)

d = st.date_input(
    "조회 범위를 설정하세요.",
    (start_date, today),
    start_date,
    today,
    format="YYYY/MM/DD",
)

option_언론사종류 = st.selectbox(
        "언론사 종류를 선택하세요",
        ['전체', '신문사', '방송사', '통신사', '기타' ],
        index = 0,
    )

try:
    cur_df1 = news_data.loc[news_data["date"].dt.date >= d[0]]
    chart_date_df = cur_df1.loc[cur_df1["date"].dt.date <= d[1]]
    if not option_언론사종류 == "전체":
        chart_date_df = chart_date_df.loc[chart_date_df["종류"] == option_언론사종류]



    chart_df = chart_date_df[[ "media1", '유죄_(등장_횟수)',
        '불법_(등장_횟수)', '형벌_(등장_횟수)', 
        '리스크_(등장_횟수)', '구속_(등장_횟수)',
        '시세조종_(등장_횟수)']].groupby("media1").sum()[['유죄_(등장_횟수)',
        '불법_(등장_횟수)', '형벌_(등장_횟수)', '리스크_(등장_횟수)', '구속_(등장_횟수)',
        '시세조종_(등장_횟수)']]



    main_fig = go.Figure(
        data = [
            go.Bar(
                x = chart_df.index,
                y = chart_df['유죄_(등장_횟수)'],
                name="유죄",
                ),

            go.Bar(
                x = chart_df.index,
                y = chart_df['불법_(등장_횟수)'],
                name="불법",
                ),

            go.Bar(
                x = chart_df.index,
                y = chart_df['형벌_(등장_횟수)'],
                name="형벌",
                ),

            go.Bar(
                x = chart_df.index,
                y = chart_df['리스크_(등장_횟수)'],
                name="리스크",
                ),
            go.Bar(
                x = chart_df.index,
                y = chart_df['구속_(등장_횟수)'],
                name="구속",
                ),
            go.Bar(
                x = chart_df.index,
                y = chart_df['시세조종_(등장_횟수)'],
                name="시세조종",
                ),

            go.Bar(
                x = chart_df.index,
                y = chart_df['시세조종_(등장_횟수)'] + chart_df['구속_(등장_횟수)'] + chart_df['리스크_(등장_횟수)'] + chart_df['형벌_(등장_횟수)'] +  chart_df['불법_(등장_횟수)'] + chart_df['유죄_(등장_횟수)'],
                name="합",
                ),

            ]
    )


    main_fig.update_layout(title='선택 기간 동안의 단어별 등장 횟수', xaxis_title='언론사', yaxis_title='횟수 (건)')
    st.plotly_chart( main_fig, use_container_width=True) 
except:
    st.text("기간 선택 대기중")