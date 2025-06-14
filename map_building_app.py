import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 타이틀
st.title('🏢 광양시 노후 건축물 정보')

# 예시 데이터
data = {
    '건물명': ['광양고등학교', '광양주택1', '광양상가2', '광양읍 빌라', '광양읍 상가1', '광양읍 주택2'],
    '건축년도': [1987, 1975, 1980, 1970, 1985, 1990],
    '주소': ['전라남도 광양시 봉강면 매천로 667', '광양시 YY길 45', '광양시 ZZ로 678', '광양읍 AA길 89', '광양읍 BB로 56', '광양읍 CC로 101'],
    '노후화정도': ['심각', '보통', '양호', '심각', '보통', '양호'],
    '보수필요': ['예', '예', '아니오', '예', '예', '아니오'],
    '위도': [34.9836075015558, 34.9700, 34.9740, 34.9760, 34.9780, 34.9800],
    '경도': [127.572658384177, 127.5800, 127.5830, 127.5845, 127.5850, 127.5860],
}
df = pd.DataFrame(data)

# 지도 생성 (중심 위치도 광양고등학교 근처로 설정)
m = folium.Map(location=[34.9836, 127.5726], zoom_start=15)

# 지도에 건물 표시
for i, row in df.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=f"""
        <b>건물명:</b> {row['건물명']}<br>
        <b>건축년도:</b> {row['건축년도']}<br>
        <b>노후화 정도:</b> {row['노후화정도']}<br>
        <b>보수 필요:</b> {row['보수필요']}
        """,
        tooltip=row['건물명']
    ).add_to(m)

# Streamlit에서 Folium 지도 렌더링
st_map = st_folium(m, width=700, height=500)

# 선택한 건물 정보를 표시 (Popup으로 제공)
if st_map.get("last_object_clicked"):
    clicked_info = st_map["last_object_clicked"]
    clicked_building = df[
        (df["위도"] == clicked_info["lat"]) & (df["경도"] == clicked_info["lng"])
    ].iloc[0]
    
    st.subheader(f"{clicked_building['건물명']} 상세 정보")
    st.write(f"건축년도: {clicked_building['건축년도']}")
    st.write(f"주소: {clicked_building['주소']}")
    st.write(f"노후화 정도: {clicked_building['노후화정도']}")
    st.write(f"보수 필요 여부: {clicked_building['보수필요']}")

    # 노후화 정도에 따라 색깔 표시
    if clicked_building['노후화정도'] == '심각':
        st.error('⚠️ 노후화 상태가 매우 심각합니다.')
    elif clicked_building['노후화정도'] == '보통':
        st.warning('⚠️ 노후화 상태가 보통입니다.')
    else:
        st.success('😊 노후화 상태가 양호합니다.')