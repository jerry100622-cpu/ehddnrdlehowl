import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit 설정
st.set_page_config(page_title="월별 기온분석", layout="wide")

st.title("월별 기온분석")
st.write("월을 선택하면 해당 월의 최고기온과 최저기온을 그래프로 보여줍니다.")

# CSV 파일 불러오기
try:
    df = pd.read_csv("../temperature (5).csv", encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv("../temperature (5).csv", encoding="utf-8-sig")
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.stop()

# 월과 연도 분리
month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
}

date_parts = df["일시"].astype(str).str.split("-", expand=True)

df["월"] = date_parts[0].map(month_map)
df["연도"] = pd.to_numeric(date_parts[1], errors="coerce") + 1900

df["최고기온(℃)"] = pd.to_numeric(df["최고기온(℃)"], errors="coerce")
df["최저기온(℃)"] = pd.to_numeric(df["최저기온(℃)"], errors="coerce")

df = df.dropna(subset=["월", "연도"])
df["월"] = df["월"].astype(int)
df["연도"] = df["연도"].astype(int)

# 월 선택
month_names = [
    "1월", "2월", "3월", "4월",
    "5월", "6월", "7월", "8월",
    "9월", "10월", "11월", "12월"
]

selected_month = st.selectbox("월을 선택하세요.", month_names)

month_number = month_names.index(selected_month) + 1

# 선택한 월 데이터 추출
monthly_df = df[df["월"] == month_number].copy()

monthly_df = monthly_df.sort_values("연도")

monthly_df = monthly_df.dropna(
    subset=["최고기온(℃)", "최저기온(℃)"]
)

if monthly_df.empty:
    st.warning("해당 월의 데이터가 없습니다.")
    st.stop()

# 그래프 생성
fig = go.Figure()

# 최고기온 그래프
fig.add_trace(go.Scatter(
    x=monthly_df["연도"],
    y=monthly_df["최고기온(℃)"],
    mode="lines+markers",
    name="최고기온",
    line=dict(color="hotpink", width=3)
))

# 최저기온 그래프
fig.add_trace(go.Scatter(
    x=monthly_df["연도"],
    y=monthly_df["최저기온(℃)"],
    mode="lines+markers",
    name="최저기온",
    line=dict(color="skyblue", width=3)
))

# 그래프 제목과 축 설정
fig.update_layout(
    title="월별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    legend_title="범례",
    template="plotly_white",
    hovermode="x unified",
    height=600
)

fig.update_xaxes(dtick=10)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 표 출력
st.subheader(f"{selected_month} 기온 데이터")

st.dataframe(
    monthly_df[["연도", "최고기온(℃)", "최저기온(℃)"]],
    use_container_width=True,
    hide_index=True
)
import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_PATH = os.path.join(BASE_DIR, "temperature (5).csv")

try:
    df = pd.read_csv(CSV_PATH, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
except FileNotFoundError:
    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    st.stop()
