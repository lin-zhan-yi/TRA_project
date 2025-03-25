import pandas as pd
import streamlit as st
import altair as alt

DATA_URL_PEOPLE = "https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/8ae4cabf6973990e0169947ed32454b9"
DATA_URL_STATION = ('https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/0518b833e8964d53bfea3f7691aea0ee')

st.title('台鐵歷年進出人數前十名的車站')
st.write('使用台鐵提供的資訊，取得進出站最多的前十名，並做幾項推論')


markdown='''
### 進出站差異推論

#### 出>進

1. 桃園、中壢、樹林，可能原因是去台北工作
2. 新竹，可能因為竹科工作機會多讓許多人在新竹站下車

#### 進>出

3. 台北、台中、高雄，可能是因為大城市為人口聚集地，使這些站為出發的起點
4. 2021各站人數銳減可能為疫情之因素

#### 其他

5. 進出站前十名車站的圖形趨近於重合，可能的原因為日常通勤者(通勤族)，多會在同站進出'''
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
def group_data_by_year_and_stacode(data_people_count):
    data_people_count["year"] = data_people_count["trnOpDate"].dt.year

    return (
        data_people_count.drop(columns=['trnOpDate'])
        .groupby(["year","staCode"])
        .sum()
    )

data_people_count=load_data_people_count()
data_stations = load_station_data()


data_people_count_annually=group_data_by_year_and_stacode(data_people_count)
data_people_count_annually.reset_index(inplace=True)

data_people_count_annually=data_people_count_annually.merge(
    data_stations[["staCode", "stationName"]], on="staCode"
)




total_people_count_per_station=(
    data_people_count_annually.groupby(["staCode", "stationName"])["gateInComingCnt"].sum().reset_index()
)

top_10_stations=total_people_count_per_station.sort_values(
    by="gateInComingCnt",ascending=False
).head(10)


data_top_10_stations=data_people_count_annually[
    data_people_count_annually["staCode"].isin(top_10_stations["staCode"])
]

data_top_10_stations_pivot =data_top_10_stations.pivot_table(
    index=["stationName"],columns="year",values="gateInComingCnt",aggfunc="sum"
).reset_index()

st.write("十大進站人數最多的車站(按年分佈):")
st.write(data_top_10_stations_pivot)

chart_incoming = (
    alt.Chart(data_top_10_stations)
    .mark_line()
    .encode(x="year:O", y="gateOutGoingCnt:Q", color="stationName:N")
    .properties(title=f"十大出站人數最多的車站（按年分佈）")
)

chart = alt.layer(chart_incoming).resolve_scale(y="independent")
st.altair_chart(chart, use_container_width=True)






total_people_count_per_station=(
    data_people_count_annually.groupby(["staCode", "stationName"])["gateOutGoingCnt"].sum().reset_index()
)

top_10_stations=total_people_count_per_station.sort_values(
    by="gateOutGoingCnt",ascending=False
).head(10)


data_top_10_stations=data_people_count_annually[
    data_people_count_annually["staCode"].isin(top_10_stations["staCode"])
]

data_top_10_stations_pivot =data_top_10_stations.pivot_table(
    index=["stationName"],columns="year",values="gateOutGoingCnt",aggfunc="sum"
).reset_index()


chart_incoming = (
    alt.Chart(data_top_10_stations)
    .mark_line()
    .encode(x="year:O", y="gateOutGoingCnt:Q", color="stationName:N")
    .properties(title=f"十大出站人數最多的車站（按年分佈）")
)

chart = alt.layer(chart_incoming).resolve_scale(y="independent")
st.altair_chart(chart, use_container_width=True)


st.write("十大出站人數最多的車站(按年分佈):")
st.write(data_top_10_stations_pivot)



# c=(
#     alt.Chart(data_people_count_specific_month)
#     .mark_circle()
#     .encode(x="year:O",y="gateInComingCnt:Q",size="gateInComingCnt",color="gateInComingCnt",tooltip=["stationName","year","month","gateInComingCnt","gateOutGoingCnt"])
# )
# st.altair_chart(c, use_container_width=True)



#https://buttaiwan.github.io/trtcvol/
#https://plotly.streamlit.app/~/+/Heatmaps
#https://plotly.streamlit.app/~/+/Candlestick_Charts
#https://docs.streamlit.io/develop/api-reference/charts/st.altair_chart
#https://plotly.com/python/dot-plots/

