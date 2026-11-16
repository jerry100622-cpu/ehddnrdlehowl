import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Streamlit 기본 설정
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("월별 기온분석")
st.write("원하는 월을 선택하면 연도별 최고기온과 최저기온을 비교할 수 있습니다.")

# CSV 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "temperature (5).csv")

# CSV 파일 불러오기
try:
    df = pd.read_csv(CSV_PATH, encoding="cp949")
except UnicodeDecodeError:
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding="euc-kr")
except FileNotFoundError:
    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    st.stop()

# 월 영어 이름을 숫자로 변경
month_map = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

# 날짜 분리
date_parts = df["일시"].astype(str).str.strip().str.split("-", expand=True)

df["월"] = date_parts[0].map(month_map)
df["연도"] = pd.to_numeric(date_parts[1], errors="coerce") + 1900

# 기온 데이터 숫자로 변환
df["최고기온(℃)"] = pd.to_numeric(
    df["최고기온(℃)"], errors="coerce"
)

df["최저기온(℃)"] = pd.to_numeric(
    df["최저기온(℃)"], errors="coerce"
)

# 결측치 제거
df = df.dropna(subset=["월", "연도"])

df["월"] = df["월"].astype(int)
df["연도"] = df["연도"].astype(int)

# 월 선택
month_names = [
    "1월", "2월", "3월", "4월",
    "5월", "6월", "7월", "8월",
    "9월", "10월", "11월", "12월"
]

selected_month = st.selectbox(
    "분석할 월을 선택하세요.",
    month_names
)

# 선택한 월 숫자로 변환
month_number = month_names.index(selected_month) + 1

# 선택한 월 데이터 추출
monthly_df = df[df["월"] == month_number].copy()

monthly_df = monthly_df.sort_values("연도")

monthly_df = monthly_df.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"]
)

# 데이터 확인
if monthly_df.empty:
    st.warning(f"{selected_month} 데이터가 없습니다.")
    st.stop()

# 그래프 생성
fig = go.Figure()

# 최고기온 그래프
fig.add_trace(
    go.Scatter(
        x=monthly_df["연도"],
        y=monthly_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="hotpink",
            width=3
        )
    )
)

# 최저기온 그래프
fig.add_trace(
    go.Scatter(
        x=monthly_df["연도"],
        y=monthly_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="skyblue",
            width=3
        )
    )
)

# 그래프 제목 및 축 설정
fig.update_layout(
    title="월별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    legend_title="범례",
    hovermode="x unified",
    template="plotly_white",
    height=600
)

# 가로축 연도 표시
fig.update_xaxes(dtick=10)

# 세로축 격자 표시
fig.update_yaxes(showgrid=True)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

# 데이터 표 출력
st.subheader(f"{selected_month} 기온 데이터")

st.dataframe(
    monthly_df[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ],
    use_container_width=True,
    hide_index=True
)

# 데이터 분석 결과
st.subheader("기온 분석 결과")

st.write(
    f"선택한 {selected_month}의 최고기온 평균은 "
    f"{monthly_df['최고기온(℃)'].mean():.2f}℃입니다."
)

st.write(
    f"선택한 {selected_month}의 최저기온 평균은 "
    f"{monthly_df['최저기온(℃)'].mean():.2f}℃입니다."
)
