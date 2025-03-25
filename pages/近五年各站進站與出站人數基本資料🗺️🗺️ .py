import pandas as pd
import streamlit as st
import altair as alt

DATA_URL_PEOPLE = "https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/8ae4cabf6973990e0169947ed32454b9"
DATA_URL_STATION = ('https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/0518b833e8964d53bfea3f7691aea0ee')

st.title('歷年月份進出表')
st.write('使用市政府的資訊，得到一個歷年月份人數的比較')

@st.cache_data
def load_data_people_count():
    csv_files = [
        "每日各站進出站人數2020.csv",
        "每日各站進出站人數2021.csv",
        "每日各站進出站人數2022.csv",
        "每日各站進出站人數2023.csv",
        "每日各站進出站人數20190423-20191231.csv",
    ]

    data_frames = [pd.read_csv(file) for file in csv_files]
    data_latest = pd.read_json(DATA_URL_PEOPLE, orient="record")
    data_frames.append(data_latest)

    data_people_count = pd.concat(data_frames, ignore_index=True)

    data_people_count['trnOpDate'] =pd.to_datetime(
        data_people_count['trnOpDate'],format="%Y%m%d"
    )
    data_people_count["month"] = data_people_count["trnOpDate"].dt.month
    data_people_count["year"] = data_people_count["trnOpDate"].dt.year

    return data_people_count

@st.cache_data
def load_station_data():
    data = pd.read_json(DATA_URL_STATION, orient="record").rename(
        {"stationCode": "staCode"}, axis=1
    )
    return data

@st.cache_data
def group_data_month_and_stacode(data_people_count):
    data_people_count["year"] = data_people_count["trnOpDate"].dt.year

    return (
        data_people_count.drop(columns=['trnOpDate'])
        .groupby(["year","staCode"])
        .sum()
    )

data_people_count=load_data_people_count()
data_stations = load_station_data()


data_people_count_annually=group_data_month_and_stacode(data_people_count)
data_people_count_annually.reset_index(inplace=True)

data_people_count_annually=data_people_count_annually.merge(
    data_stations[["staCode", "stationName"]], on="staCode"
)

years=st.selectbox(
    "請選擇你要的年份",data_people_count_annually["year"].unique()
)

data_people_count_annually_selected_year=data_people_count_annually[
    data_people_count_annually["year"]==years
]

st.write(data_people_count_annually_selected_year)
