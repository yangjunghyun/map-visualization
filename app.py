import streamlit as st
import pandas as pd
import pydeck as pdk

# 데이터 로드
data = pd.read_csv('data.csv')

st.title("상권 분석 지도 시각화")

# 광역별 필터링
selected_region = st.selectbox("광역을 선택하세요", data['광역'].unique())
filtered_data = data[data['광역'] == selected_region]

# 업종별 필터링
selected_category = st.selectbox("업종 대분류를 선택하세요", filtered_data['업종대분류_임시'].unique())
filtered_data = filtered_data[filtered_data['업종대분류_임시'] == selected_category]

st.subheader(f"{selected_region}의 {selected_category} 업종 분석")

# 지도 시각화
if not filtered_data.empty:
    st.map(filtered_data[['좌표_위도', '좌표_경도']])

    # pydeck을 사용하여 마커와 팝업을 포함한 지도 생성
    layer = pdk.Layer(
        "ScatterplotLayer",
        filtered_data,
        get_position='[좌표_경도, 좌표_위도]',
        get_radius=100,
        get_color=[255, 0, 0, 160],
        pickable=True,
    )

    # 초기 뷰 설정
    initial_view = pdk.ViewState(
        latitude=filtered_data['좌표_위도'].mean(),
        longitude=filtered_data['좌표_경도'].mean(),
        zoom=10,
        pitch=50,
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
st.write(filtered_data[['사업체명', '대표자명', '광역', '좌표_위도', '좌표_경도']])
