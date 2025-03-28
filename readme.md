## streamlit 專案

## 目錄

## 台灣鐵路

1. 以年為單位，以折現圖的方式呈現人數趨勢，
   以十二個點，每點皆為該月平均人數
2. 以月為單位，以折現圖的方式呈現人數趨勢，
   以三十/三一個點，每點皆為當日人數
3. 以周為單位，以折現圖的方式呈現人數趨勢，
   以七個點

## 發現
1. 2022通常比較低一點
2. 進站人數跟出站人數會有高度重疊
3. 進站人數比出站人數微多
4. 每月的漲幅比較(顏色)

## 2024/12/03的內容
1. 各站點位置地圖和基本資料
    - 讓使用者了解每個車站在台灣的分布情況
    - 如有進一步的需求，可以得到這些資訊
    - 如果想了解更深入的資訊，如:車站代碼、進站人數、出站人數、車站地址、經緯度、車站電話、是否設置UBike，可點選地圖的物件得到以上的資訊
2. 顏色區分近五年各站進站與出站人數
    - 檢視"進站"與"出站"的人數
    - 凸顯各個車站的人數多寡
3. 歷年月份進出人數比較，含有折線圖和散布圖
    - 折線圖 : 表示各站進出的人數變化，有藍色(進站人數)與紅色(出站人數)進行比較
    - 散布圖 : 每個點標記出具體的人數，能準確的知道每個月的進出人數

## perplexity的建議
1. 趨勢預測 : 車站流量變化趨勢   目的：分析特定車站的進出人次隨時間的變化。
2. 閱讀圖表不易:
   1. 分組比較 依據地理位置分組
   2. 縮放功能
   3. 使用摘要統計
   4. 地理熱力圖
3. 使用者互動儀表板

## 進出站差異推論
# 出>進
1. 桃園、中壢、樹林，可能原因是去台北工作
2. 新竹，可能因為竹科工作機會多讓許多人在新竹站下車
# 進>出
3. 台北、台中、高雄，可能是因為大城市為人口聚集地，使這些站為出發的起點
4. 2021各站人數銳減可能為疫情之因素
5. 進出站前十名車站的圖形趨近於重合，可能的原因為日常通勤者(通勤族)，多會在同站進出

## 人數多寡程度分配標準
# 求出平均與標準差
# 使用站點的顏色不同，讓使用者能更方便看出各進出人數狀況
現在使用尋找中位數的方法來進行分群，
首先先找出所有車站進出站人數的中位數，分為兩群，
接著在上述的兩群中在各取一個中位數，分群由兩群變成四群
這四群的人數由多到少，將車站的顏色依序標示為:紅色、橘色、藍色、白色

1. 觀察:多數車站每一年都在同一個區間(顏色相同)
2. 原因:人數不會大幅成長，每個區間都是差好幾萬，不至於和前一年有過大的差距
3. 觀察2:新城2019後人數下降
# 問題:因各站人數相差過多，導致標準差>平均數 因而無法求出上面3個比較





#https://www.perplexity.ai/search/yi-ge-pythonzhuan-an-cong-tai-X1gOVJYBTv.xc4mYH7bi3A
#https://python-visualization.github.io/folium/latest/reference.html#folium.map.Icon
#https://seaborn.pydata.org/examples/index.html
#https://seaborn.pydata.org/examples/errorband_lineplots.html
#https://pygwalkerdemo-cxz7f7pt5oc.streamlit.app/
#https://file.data.gov.tw/ext/curation/703/embed.html
#https://data.gov.tw/expos
#https://docs.streamlit.io/develop/api-reference/charts/st.line_chart