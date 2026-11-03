
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인이 좋아하는 서울 관광지 TOP 10")
st.write("서울의 대표 관광지 10곳을 지도에서 확인해 보세요.")

places = [
    {
        "rank": 1,
        "name": "명동",
        "english": "Myeong-dong",
        "lat": 37.5636,
        "lon": 126.9850,
        "category": "쇼핑·먹거리",
        "description": "화장품, 패션 매장과 길거리 음식이 모여 있는 대표적인 쇼핑 거리입니다."
    },
    {
        "rank": 2,
        "name": "N서울타워",
        "english": "N Seoul Tower",
        "lat": 37.5512,
        "lon": 126.9882,
        "category": "전망·랜드마크",
        "description": "서울의 대표 랜드마크로 전망대에서 아름다운 서울 풍경을 감상할 수 있습니다."
    },
    {
        "rank": 3,
        "name": "코엑스·별마당도서관",
        "english": "COEX & Starfield Library",
        "lat": 37.5126,
        "lon": 127.0593,
        "category": "쇼핑·문화",
        "description": "대형 쇼핑 공간과 독특한 책장이 있는 별마당도서관을 즐길 수 있습니다."
    },
    {
        "rank": 4,
        "name": "강남역",
        "english": "Gangnam Station",
        "lat": 37.4979,
        "lon": 127.0276,
        "category": "쇼핑·도심문화",
        "description": "패션 매장과 카페, 음식점이 밀집한 서울의 대표 번화가입니다."
    },
    {
        "rank": 5,
        "name": "홍대 거리",
        "english": "Hongdae",
        "lat": 37.5563,
        "lon": 126.9236,
        "category": "문화·공연",
        "description": "거리 공연과 인디 음악, 개성 있는 카페와 상점으로 유명합니다."
    },
    {
        "rank": 6,
        "name": "동대문디자인플라자",
        "english": "DDP",
        "lat": 37.5671,
        "lon": 127.0095,
        "category": "건축·전시",
        "description": "독특한 곡선형 건축물이 인상적인 디자인 및 전시 공간입니다."
    },
    {
        "rank": 7,
        "name": "광장시장",
        "english": "Gwangjang Market",
        "lat": 37.5700,
        "lon": 126.9997,
        "category": "전통시장·음식",
        "description": "빈대떡과 김밥 등 다양한 한국 전통시장 음식을 맛볼 수 있습니다."
    },
    {
        "rank": 8,
        "name": "경복궁",
        "english": "Gyeongbokgung Palace",
        "lat": 37.5796,
        "lon": 126.9770,
        "category": "역사·문화",
        "description": "조선 왕조의 대표 궁궐로 한국의 전통 건축과 역사를 경험할 수 있습니다."
    },
    {
        "rank": 9,
        "name": "북촌한옥마을",
        "english": "Bukchon Hanok Village",
        "lat": 37.5826,
        "lon": 126.9830,
        "category": "전통·거리",
        "description": "전통 한옥이 모여 있는 마을로 한국의 옛 거리 풍경을 감상할 수 있습니다."
    },
    {
        "rank": 10,
        "name": "남대문시장",
        "english": "Namdaemun Market",
        "lat": 37.5592,
        "lon": 126.9777,
        "category": "전통시장·쇼핑",
        "description": "의류와 기념품, 생활용품, 다양한 먹거리를 판매하는 전통시장입니다."
    }
]

st.info(
    "관광지 선정은 방문객 규모와 외국인 관광객 관심도, "
    "서울의 대표성을 참고한 안내용 목록이며 공식 통합 순위는 아닙니다."
)

# 서울 지도 생성
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

# 관광지 마커 표시
for place in places:

    popup_html = f"""
    <div style="width:220px">
        <h4>{place['rank']}. {place['name']}</h4>
        <b>{place['english']}</b>
        <p>{place['category']}</p>
        <p>{place['description']}</p>
    </div>
    """

    folium.Marker(
        location=[place["lat"], place["lon"]],
        tooltip=f"{place['rank']}. {place['name']}",
        popup=folium.Popup(
            popup_html,
            max_width=280
        ),
        icon=folium.DivIcon(
            html=f"""
            <div style="
                background:#d62828;
                color:white;
                border:2px solid white;
                border-radius:50%;
                width:29px;
                height:29px;
                text-align:center;
                line-height:25px;
                font-weight:bold;
                font-size:13px;
                box-shadow:0 1px 5px #777;">
                {place['rank']}
            </div>
            """,
            icon_size=(29, 29),
            icon_anchor=(14, 14)
        )
    ).add_to(seoul_map)

# 지도 표시 범위
seoul_map.fit_bounds([
    [37.485, 126.88],
    [37.70, 127.12]
])

st.subheader("📍 서울 관광지 지도")
st.write("지도에 표시된 빨간색 숫자를 클릭하면 관광지 설명을 확인할 수 있습니다.")

st_folium(
    seoul_map,
    width=None,
    height=620,
    returned_objects=[],
    use_container_width=True
)

st.divider()

# 관광지 설명
st.subheader("🏙️ 관광지 TOP 10 소개")

for start in range(0, len(places), 2):

    cols = st.columns(2)

    for col, place in zip(
        cols,
        places[start:start + 2]
    ):

        with col:

            st.markdown(
                f"### {place['rank']}. {place['name']}"
            )

            st.caption(
                f"{place['english']} | {place['category']}"
            )

            st.write(place["description"])

            st.link_button(
                "📍 지도에서 위치 보기",
                f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lon']}"
            )

st.divider()

st.caption(
    "지도 데이터: OpenStreetMap | "
    "관광지 위치 및 소개를 제공하는 서울 관광 안내 앱"
)
