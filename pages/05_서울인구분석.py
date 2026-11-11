
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import koreanize_matplotlib
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
# 2. CSV 파일 경로 설정
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "population.csv"

# -------------------------------
# 3. CSV 파일 불러오기
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

# -------------------------------
# 4. 행정구역 이름 정리
# -------------------------------
df["행정구역명"] = df["행정구역"].astype(str).str.extract(
    r"^\s*(.*?)\s*\(\d+\)"
)

df["행정구역명"] = df["행정구역명"].fillna(
    df["행정구역"]
)

districts = df["행정구역명"].tolist()

# -------------------------------
# 5. 선택 메뉴
# -------------------------------
st.subheader("🔎 검색 조건 선택")

col1, col2, col3 = st.columns(3)

with col1:
    selected_district = st.selectbox(
        "행정구역 선택",
        districts
    )

with col2:
    selected_year = st.selectbox(
        "연도 선택",
        [2020, 2021, 2022, 2023, 2024, 2025]
    )

with col3:
    selected_gender = st.selectbox(
        "성별 선택",
        ["전체", "남자", "여자"]
    )

# -------------------------------
# 6. 연령대별 데이터 추출
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

selected_row = df[
    df["행정구역명"] == selected_district
].iloc[0]

column_names = [
    f"{selected_year}년_{gender_prefix}_{age}"
    for age in age_groups
]

population = pd.to_numeric(
    selected_row[column_names].astype(str).str.replace(
        ",", "", regex=False
    ),
    errors="coerce"
).fillna(0)

chart_data = pd.DataFrame({
    "나이": age_groups,
    "인구수": population.values
})

# -------------------------------
# 7. 선택 정보 출력
# -------------------------------
st.divider()

st.subheader("📌 선택한 인구 정보")

st.write(
    f"행정구역: {selected_district} | "
    f"연도: {selected_year}년 | "
    f"성별: {selected_gender}"
)

total_population = int(chart_data["인구수"].sum())

metric1, metric2 = st.columns(2)

metric1.metric(
    "총인구수",
    f"{total_population:,}명"
)

metric2.metric(
    "가장 인구가 많은 연령대",
    chart_data.loc[
        chart_data["인구수"].idxmax(), "나이"
    ]
)

# -------------------------------
# 8. 꺾은선 그래프
# -------------------------------
st.subheader("📈 연령대별 인구수 꺾은선 그래프")

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    chart_data["나이"],
    chart_data["인구수"],
    color="green",
    marker="o",
    linewidth=2.5,
    markersize=7
)

ax.set_title(
    f"{selected_district} {selected_year}년 "
    f"{selected_gender} 연령대별 인구수",
    fontsize=16,
    pad=20
)

ax.set_xlabel("나이", fontsize=12)
ax.set_ylabel("인구수 (명)", fontsize=12)

# Y축 1,000명 단위
max_population = chart_data["인구수"].max()

y_max = max(
    1000,
    ((int(max_population) // 1000) + 1) * 1000
)

ax.set_ylim(0, y_max)

ax.yaxis.set_major_locator(
    ticker.MultipleLocator(1000)
)

ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(
        lambda x, pos: f"{int(x):,}"
    )
)

# 가로 구분선
ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.5,
    color="gray"
)

plt.xticks(rotation=30)
plt.tight_layout()

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# -------------------------------
# 9. 상세 데이터
# -------------------------------
with st.expander("연령대별 상세 인구 데이터 보기"):

    display_data = chart_data.copy()

    display_data["인구수"] = display_data["인구수"].map(
        lambda x: f"{int(x):,}명"
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.caption(
    "자료: population.csv | 서울특별시 연령별 인구 데이터"
)
