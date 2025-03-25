import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

st.title('臺鐵每日各站點進出站人數')

dict={
    "緯度":None,
    "經度":None
}

DATA_URL_STATION = ('https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/0518b833e8964d53bfea3f7691aea0ee')

DATA_URL_PEOPLE = ("https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/8ae4cabf6973990e0169947ed32454b9")


markdown='''
## 使用站點的顏色不同，讓使用者能更方便看出各進出人數狀況
現在使用尋找中位數的方法來進行分群，
首先先找出所有車站進出站人數的中位數，分為兩群，
接著在上述的兩群中在各取一個中位數，分群由兩群變成四群
這四群的人數由多到少，將車站的顏色依序標示為 : 紅色、橘色、藍色、白色

### 觀察:
1.多數車站每一年都在同一個區間(顏色相同)
### 原因:
1.人數不會大幅成長，每個區間都是差好幾萬，不至於和前一年有過大的差距 '''
st.markdown(markdown)



@st.cache_data
def load_data_people_count():
    csv_files = [
        "每日各站進出站人數2020.csv",
        "每日各站進出站人數2021.csv",
        "每日各站進出站人數2022.csv",
        "每日各站進出站人數2023.csv",
        "每日各站進出站人數20190423-20191231.csv",
        "每日各站進出站人數2024.csv",
    ]

    data_frames = [pd.read_csv(file) for file in csv_files]
    data_latest = pd.read_json(DATA_URL_PEOPLE, orient="record")
    data_frames.append(data_latest)

    data_people_count = pd.concat(data_frames, ignore_index=True)

    data_people_count['trnOpDate'] = pd.to_datetime(
        data_people_count['trnOpDate'], format="%Y%m%d"
    )
    # data_people_count["month"] = data_people_count["trnOpDate"].dt.month
    # data_people_count["year"] = data_people_count["trnOpDate"].dt.year

    return data_people_count


@st.cache_data
def load_station_data():
    data = pd.read_json(DATA_URL_STATION, orient="record").rename(
        {"stationCode": "staCode"}, axis=1
    )
    return data

@st.cache_data
def group_data_by_year_and_stacode(data_people_count):
    data_people_count["year"] = data_people_count["trnOpDate"].dt.year

    return (
        data_people_count.drop(columns=['trnOpDate'])
        .groupby(["year","staCode"])
        .mean()
    )

data_people_count=load_data_people_count()
data_stations = load_station_data()

data_people_count_annually=group_data_by_year_and_stacode(data_people_count)
data_people_count_annually.reset_index(inplace=True)

data_people_count_annually=data_people_count_annually.merge(
    data_stations[["staCode","stationName","gps"]],on="staCode"
)


years=data_people_count_annually["year"].unique()

year_numbers={}
colors=["red","orange","blue","white"]


for year in years :
    _data= data_people_count_annually[data_people_count_annually['year']==year]

    median=_data['gateInComingCnt'].median()
    upper_median=_data[_data['gateInComingCnt']>median]['gateInComingCnt'].median()

    lower_median = _data[_data['gateInComingCnt'] < median]['gateInComingCnt'].median()

    year_numbers[year]={
        "median": median,
        "upper_median": upper_median,
        "lower_median" : lower_median,
    }

year=st.selectbox("選擇年分:",years)
selected_data=data_people_count_annually[data_people_count_annually["year"]==year]


m = folium.Map(location=[23.483697, 120.6777852], zoom_start=7.5)

for index, row in selected_data.iterrows():
    dict = {
        "lat": float(row["gps"].split(" ")[0]),
        "lng": float(row["gps"].split(" ")[1])
    }

    if row['gateInComingCnt'] > year_numbers[row["year"]]["upper_median"] :
        color=colors[0]
    elif row['gateInComingCnt'] > year_numbers[row["year"]]["median"] :
        color=colors[1]
    elif row['gateInComingCnt'] > year_numbers[row["year"]]["lower_median"] :
        color=colors[2]
    else :
        color=colors[3]

    popup_html = f"<h2>{row['stationName']}</h2><br/>每日平均進站人數:{round(row['gateInComingCnt'], 2)}<br/>"
    popup = folium.Popup(popup_html, max_width=400)

    folium.Marker(
        [dict["lat"],dict["lng"]], popup=popup, tooltip=row["stationName"],icon=folium.Icon(color=color),
    ).add_to(m)


st_data = st_folium(m, width=725)

