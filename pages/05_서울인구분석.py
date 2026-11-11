
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# -------------------------------
# 1. 페이지 설정
# -------------------------------
st.set_page_config(
    page_title="서울 인구 분석",
    page_icon="📊",
    layout="wide"
)

st.title("📊 서울특별시 인구 분석")
st.write("행정구역, 연도, 성별에 따른 연령대별 인구를 확인할 수 있습니다.")

# -------------------------------
# 2. CSV 파일 경로
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "population.csv"

# -------------------------------
# 3. CSV 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(FILE_PATH, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(FILE_PATH, encoding="utf-8-sig")

    return df

try:
    df = load_data()

except FileNotFoundError:
    st.error("population.csv 파일을 찾을 수 없습니다.")
    st.stop()

except Exception as e:
    st.error(f"CSV 파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# -------------------------------
# 4. 행정구역 정리
# -------------------------------
df["행정구역명"] = (
    df["행정구역"]
    .astype(str)
    .str.extract(r"^\s*(.*?)\s*\(\d+\)")[0]
    .str.strip()
)

# 서울특별시 전체 및 자치구 이름 정리
df["선택지역"] = df["행정구역명"].apply(
    lambda x: x.replace("서울특별시 ", "", 1)
    if x.startswith("서울특별시 ")
    else x
)

districts = df["선택지역"].dropna().tolist()

# -------------------------------
# 5. 검색 조건 선택
# -------------------------------
st.subheader("🔎 검색 조건 선택")

col1, col2, col3 = st.columns(3)

with col1:
    selected_district = st.selectbox(
        "행정구역",
        districts
    )

with col2:
    selected_year = st.selectbox(
        "연도",
        [2020, 2021, 2022, 2023, 2024, 2025],
        index=5
    )

with col3:
    selected_gender = st.selectbox(
        "성별",
        ["전체", "남자", "여자"]
    )

# -------------------------------
# 6. 연령대 설정
# -------------------------------
age_groups = [
    "0~9세",
    "10~19세",
    "20~29세",
    "30~39세",
    "40~49세",
    "50~59세",
    "60~69세",
    "70~79세",
    "80~89세",
    "90~99세",
    "100세 이상"
]

gender_columns = {
    "전체": "거주자",
    "남자": "남_거주자",
    "여자": "여_거주자"
}

gender_prefix = gender_columns[selected_gender]

# -------------------------------
# 7. 선택한 데이터 추출
# -------------------------------
selected_row = df[
    df["선택지역"] == selected_district
].iloc[0]

column_names = [
    f"{selected_year}년_{gender_prefix}_{age}"
    for age in age_groups
]

# CSV 열 존재 여부 확인
missing_columns = [
    col for col in column_names
    if col not in df.columns
]

if missing_columns:
    st.error(
        "CSV 파일에서 필요한 인구 데이터 열을 찾지 못했습니다: "
        + ", ".join(missing_columns)
    )
    st.stop()

# 숫자형 변환
population = pd.to_numeric(
    selected_row[column_names]
    .astype(str)
    .str.replace(",", "", regex=False),
    errors="coerce"
).fillna(0)

chart_data = pd.DataFrame({
    "나이": age_groups,
    "인구수": population.values
})

# -------------------------------
# 8. 인구 정보 출력
# -------------------------------
st.divider()

st.subheader("📌 선택한 인구 정보")

st.write(
    f"**행정구역:** {selected_district} | "
    f"**연도:** {selected_year}년 | "
    f"**성별:** {selected_gender}"
)

total_population = int(chart_data["인구수"].sum())

metric1, metric2 = st.columns(2)

metric1.metric(
    "총인구수",
    f"{total_population:,}명"
)

if total_population > 0:
    max_age = chart_data.loc[
        chart_data["인구수"].idxmax(), "나이"
    ]
else:
    max_age = "데이터 없음"

metric2.metric(
    "인구가 가장 많은 연령대",
    max_age
)

# -------------------------------
# 9. 꺾은선 그래프
# -------------------------------
st.divider()

st.subheader("📈 연령대별 인구수")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=chart_data["나이"],
        y=chart_data["인구수"],
        mode="lines+markers",
        name="인구수",
        line=dict(
            color="green",
            width=3
        ),
        marker=dict(
            color="green",
            size=8
        ),
        hovertemplate=
        "나이: %{x}<br>"
        "인구수: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig.update_layout(
    title=dict(
        text=f"{selected_district} {selected_year}년 "
             f"{selected_gender} 연령대별 인구수",
        x=0.5
    ),
    xaxis=dict(
        title="나이",
        tickangle=0,
        type="category"
    ),
    yaxis=dict(
        title="인구수 (명)",
        tickmode="linear",
        tick0=0,
        dtick=1000,
        tickformat=",d",
        rangemode="tozero",
        showgrid=True,
        gridcolor="lightgray",
        griddash="dash"
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    hovermode="x unified",
    height=550,
    margin=dict(
        l=70,
        r=30,
        t=80,
        b=70
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------
# 10. 상세 데이터
# -------------------------------
with st.expander("📋 연령대별 상세 인구 데이터"):

    display_data = chart_data.copy()

    display_data["인구수"] = display_data[
        "인구수"
    ].apply(lambda x: f"{int(x):,}명")

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

# -------------------------------
# 11. 마무리
# -------------------------------
st.divider()

st.caption(
    "자료: population.csv | 서울특별시 연령별 인구 분석"
)
