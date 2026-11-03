
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인이 좋아하는 서울 관광지 TOP 10")
st.write("서울의 대표 관광지와 1박 2일 여행 코스를 소개합니다.")

places = [
    {"rank": 1, "name": "명동", "english": "Myeong-dong",
     "lat": 37.5636, "lon": 126.9850, "category": "쇼핑·먹거리",
     "description": "화장품, 패션 매장과 길거리 음식이 모여 있는 대표적인 쇼핑 거리입니다."},

    {"rank": 2, "name": "N서울타워", "english": "N Seoul Tower",
     "lat": 37.5512, "lon": 126.9882, "category": "전망·랜드마크",
     "description": "서울의 대표 랜드마크로 전망대에서 아름다운 서울 풍경을 감상할 수 있습니다."},

    {"rank": 3, "name": "코엑스·별마당도서관", "english": "COEX",
     "lat": 37.5126, "lon": 127.0593, "category": "쇼핑·문화",
     "description": "대형 쇼핑 공간과 독특한 책장이 있는 별마당도서관을 즐길 수 있습니다."},

    {"rank": 4, "name": "강남역", "english": "Gangnam Station",
     "lat": 37.4979, "lon": 127.0276, "category": "쇼핑·도심문화",
     "description": "패션 매장과 카페, 음식점이 밀집한 서울의 대표 번화가입니다."},

    {"rank": 5, "name": "홍대 거리", "english": "Hongdae",
     "lat": 37.5563, "lon": 126.9236, "category": "문화·공연",
     "description": "거리 공연과 인디 음악, 개성 있는 카페와 상점으로 유명합니다."},

    {"rank": 6, "name": "동대문디자인플라자", "english": "DDP",
     "lat": 37.5671, "lon": 127.0095, "category": "건축·전시",
     "description": "독특한 곡선형 건축물이 인상적인 디자인 및 전시 공간입니다."},

    {"rank": 7, "name": "광장시장", "english": "Gwangjang Market",
     "lat": 37.5700, "lon": 126.9997, "category": "전통시장·음식",
     "description": "빈대떡과 김밥 등 다양한 한국 전통시장 음식을 맛볼 수 있습니다."},

    {"rank": 8, "name": "경복궁", "english": "Gyeongbokgung Palace",
     "lat": 37.5796, "lon": 126.9770, "category": "역사·문화",
     "description": "조선 왕조의 대표 궁궐로 한국의 전통 건축과 역사를 경험할 수 있습니다."},

    {"rank": 9, "name": "북촌한옥마을", "english": "Bukchon Hanok Village",
     "lat": 37.5826, "lon": 126.9830, "category": "전통·거리",
     "description": "전통 한옥이 모여 있는 마을로 한국의 옛 거리 풍경을 감상할 수 있습니다."},

    {"rank": 10, "name": "남대문시장", "english": "Namdaemun Market",
     "lat": 37.5592, "lon": 126.9777, "category": "전통시장·쇼핑",
     "description": "의류와 기념품, 생활용품, 다양한 먹거리를 판매하는 전통시장입니다."}
]

# 관광지 지도
st.info("서울의 대표 관광지 10곳을 방문객 관심도와 관광지의 대표성을 참고하여 선정했습니다.")

seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=12,
    tiles="OpenStreetMap"
)

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
        popup=folium.Popup(popup_html, max_width=280),
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

seoul_map.fit_bounds([
    [37.485, 126.88],
    [37.70, 127.12]
])

st.subheader("📍 서울 관광지 지도")
st.write("빨간색 숫자 마커를 클릭하면 관광지 설명을 볼 수 있습니다.")

st_folium(
    seoul_map,
    width=None,
    height=620,
    returned_objects=[],
    use_container_width=True
)

# 관광지 설명
st.divider()
st.header("🏙️ 서울 관광지 TOP 10 소개")

for start in range(0, len(places), 2):
    cols = st.columns(2)

    for col, place in zip(cols, places[start:start + 2]):
        with col:
            st.markdown(f"### {place['rank']}. {place['name']}")
            st.caption(f"{place['english']} | {place['category']}")
            st.write(place["description"])

            st.link_button(
                "📍 위치 확인",
                f"https://www.google.com/maps/search/?api=1&query={place['lat']},{place['lon']}"
            )

# 1박 2일 여행 일정
st.divider()
st.header("🧳 서울 1박 2일 추천 여행 일정")
st.write("서울의 역사, 전통시장, 쇼핑, 문화와 야경을 경험할 수 있는 코스입니다.")

# 일정 데이터
itinerary = [
    {
        "day": "DAY 1",
        "title": "서울의 역사와 전통, 야경 즐기기",
        "items": [
            ("09:00~11:00", "경복궁", "조선 왕조의 궁궐을 둘러보고 한국의 역사와 전통 건축을 경험합니다."),
            ("11:00~12:00", "북촌한옥마을", "전통 한옥과 아름다운 골목길을 구경합니다. 주민 생활 공간이므로 조용히 관람합니다."),
            ("12:00~13:30", "광장시장", "빈대떡, 김밥 등 한국의 대표적인 시장 음식을 맛봅니다."),
            ("14:00~15:30", "동대문디자인플라자", "독특한 건축물을 감상하고 전시 및 디자인 공간을 둘러봅니다."),
            ("16:00~18:00", "명동", "한국 화장품과 패션 상품을 구경하고 길거리 음식을 즐깁니다."),
            ("19:00~20:30", "N서울타워", "서울의 아름다운 야경을 감상하며 첫날 일정을 마무리합니다.")
        ]
    },
    {
        "day": "DAY 2",
        "title": "쇼핑과 현대적인 서울 문화 체험",
        "items": [
            ("09:00~10:30", "남대문시장", "한국 전통시장을 둘러보고 기념품과 다양한 먹거리를 구경합니다."),
            ("11:30~13:00", "강남역", "현대적인 서울의 거리와 다양한 상점, 카페를 구경합니다."),
            ("13:00~15:00", "코엑스·별마당도서관", "대형 쇼핑몰을 구경하고 별마당도서관에서 특별한 사진을 남깁니다."),
            ("16:00~18:30", "홍대 거리", "개성 있는 카페와 상점, 거리 공연을 즐기며 여행을 마무리합니다.")
        ]
    }
]

for day in itinerary:
    st.markdown(f"## 📅 {day['day']} | {day['title']}")

    for time, name, description in day["items"]:
        with st.container(border=True):
            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown(f"**{time}**")

            with col2:
                st.markdown(f"**📍 {name}**")
                st.write(description)

    if day["day"] == "DAY 1":
        st.success("첫째 날 일정 종료 · 서울에서 1박")

st.divider()

st.subheader("✈️ 여행 안내")
st.write("""
- 이동은 지하철과 버스를 중심으로 계획합니다.
- 실제 이동 시간은 교통 상황과 대기 시간에 따라 달라질 수 있습니다.
- 경복궁 휴궁일과 관광지 운영시간을 방문 전에 확인하세요.
- 북촌한옥마을은 주민 거주 지역이므로 방문 가능 시간과 관람 수칙을 확인하세요.
""")

st.caption("지도: OpenStreetMap | 서울 관광지 및 여행 일정 안내")
