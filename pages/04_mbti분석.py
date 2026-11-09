
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="국가별 MBTI 비율 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석")
st.write("국가를 선택하면 해당 국가의 MBTI 16가지 유형별 비율을 확인할 수 있습니다.")

DATA_FILE = Path(__file__).parent / "countriesMBTI_16types.csv"

MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    df["Country"] = df["Country"].astype(str).str.strip()

    for col in MBTI_TYPES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Country"] + MBTI_TYPES)
    df = df.drop_duplicates(subset=["Country"])

    return df


def blue_gradient(n):
    start = (21, 101, 192)
    end = (220, 235, 250)

    colors = []

    for i in range(n):
        ratio = i / max(n - 1, 1)

        rgb = tuple(
            round(start[j] + (end[j] - start[j]) * ratio)
            for j in range(3)
        )

        colors.append("#{:02X}{:02X}{:02X}".format(*rgb))

    return colors


if not DATA_FILE.exists():
    st.error("CSV 파일을 app.py와 같은 폴더에 넣어주세요.")
    st.stop()

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 오류: {e}")
    st.stop()


countries = sorted(df["Country"].unique())

default_index = (
    countries.index("South Korea")
    if "South Korea" in countries
    else 0
)

selected_country = st.selectbox(
    "국가 선택",
    countries,
    index=default_index
)

country_data = df[
    df["Country"] == selected_country
][MBTI_TYPES].iloc[0]

if country_data.max() <= 1.5:
    percentages = country_data * 100
else:
    percentages = country_data.copy()

chart_data = (
    percentages.rename_axis("MBTI")
    .reset_index(name="비율")
    .sort_values("비율", ascending=False)
    .reset_index(drop=True)
)

# 1위 빨간색, 나머지 파란색 그라데이션
colors = ["#E53935"] + blue_gradient(len(chart_data) - 1)

top_mbti = chart_data.iloc[0]["MBTI"]
top_percentage = chart_data.iloc[0]["비율"]

col1, col2, col3 = st.columns(3)

col1.metric("선택 국가", selected_country)
col2.metric("가장 높은 유형", top_mbti)
col3.metric("가장 높은 비율", f"{top_percentage:.2f}%")


fig = go.Figure(
    data=[
        go.Bar(
            x=chart_data["MBTI"],
            y=chart_data["비율"],
            marker_color=colors,
            text=[
                f"{value:.2f}%"
                for value in chart_data["비율"]
            ],
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "비율: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    ]
)

fig.update_layout(
    title=f"{selected_country}의 MBTI 유형별 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율 (%)",
    yaxis=dict(
        rangemode="tozero",
        ticksuffix="%",
        showgrid=True
    ),
    xaxis=dict(
        categoryorder="array",
        categoryarray=chart_data["MBTI"].tolist()
    ),
    showlegend=False,
    height=560,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("MBTI 상세 데이터 보기"):
    display_data = chart_data.copy()

    display_data["비율"] = display_data["비율"].map(
        lambda x: f"{x:.2f}%"
    )

    display_data.index = display_data.index + 1
    display_data.index.name = "순위"

    st.dataframe(
        display_data,
        use_container_width=True
    )

st.caption(
    "참고: 제공된 CSV 원본 데이터를 기준으로 분석합니다."
)
