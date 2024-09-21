import streamlit as st
import pandas as pd
import pydeck as pdk

# Streamlit 설정: 여백 없는 모드, 사이드바 상태 설정
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 데이터 로드
data = pd.read_csv('data.csv')

# 지도에 필요한 열만 남기기
del data['latitude']
del data['longitude']

st.title("상권 분석 지도 시각화")

# 광역별 필터링
selected_region = st.selectbox("광역을 선택하세요", data['광역'].unique())
filtered_data = data[data['광역'] == selected_region]

# 업종별 필터링
selected_category = st.selectbox("업종 대분류를 선택하세요", filtered_data['산업분류_표준산업분류중분류'].unique())
filtered_data = filtered_data[filtered_data['산업분류_표준산업분류중분류'] == selected_category]

# 열 이름을 Streamlit이 인식할 수 있는 이름으로 변경
filtered_data = filtered_data.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})

st.subheader(f"{selected_region}의 {selected_category} 업종 분석")

# 지도 시각화 (pydeck을 사용한 지도만 표시)
if not filtered_data.empty:
    # pydeck을 사용하여 마커와 팝업을 포함한 지도 생성
    layer = pdk.Layer(
        "ScatterplotLayer",
        filtered_data,
        get_position='[longitude, latitude]',
        get_radius=100,
        get_color=[255, 0, 0, 160],
        pickable=True,
    )

    # 초기 뷰 설정
    initial_view = pdk.ViewState(
        latitude=filtered_data['latitude'].mean(),
        longitude=filtered_data['longitude'].mean(),
        zoom=10,
    )

    # pydeck 차트 렌더링
    tooltip = {
        "html": "<b>사업체명:</b> {사업체명}<br/><b>대표자명:</b> {대표자명}",
        "style": {"color": "white"}
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=initial_view,
        tooltip=tooltip
    )

    st.pydeck_chart(deck)
else:
    st.write("선택한 필터에 해당하는 데이터가 없습니다.")

# 상세 정보 테이블로 출력
st.write(filtered_data[['사업체명', '대표자명', '광역', '제품_주생산품']])
