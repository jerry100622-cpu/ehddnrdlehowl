
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path

# ----------------------------------
# 1. 페이지 설정
# ----------------------------------
st.set_page_config(
    page_title="월평균기온 예측 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월평균기온 분석 및 미래 기온 예측")
st.write(
    "과거 기온 데이터를 활용하여 원하는 월의 평균기온을 분석하고 "
    "선형회귀 알고리즘으로 미래 기온을 예측합니다."
)

# ----------------------------------
# 2. CSV 파일 불러오기
# ----------------------------------
current_dir = Path(__file__).resolve().parent

file_paths = [
    current_dir / "temperature.csv",
    current_dir.parent / "temperature.csv"
]

csv_path = next(
    (path for path in file_paths if path.exists()),
    None
)

if csv_path is None:
    st.error(
        "temperature.csv 파일을 찾을 수 없습니다. "
        "파이썬 파일과 같은 폴더 또는 상위 폴더에 넣어주세요."
    )
    st.stop()

try:
    try:
        df = pd.read_csv(csv_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

except Exception as e:
    st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# ----------------------------------
# 3. 데이터 전처리
# ----------------------------------
df.columns = df.columns.str.strip()

required_columns = ["일시", "평균기온(℃)"]

if not all(col in df.columns for col in required_columns):
    st.error("CSV 파일에 필요한 열이 없습니다.")
    st.stop()

# 날짜에서 월과 연도 추출
month_map = {
    "Jan": 1, "Feb": 2, "Mar": 3,
    "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9,
    "Oct": 10, "Nov": 11, "Dec": 12
}

date_parts = df["일시"].astype(str).str.strip().str.extract(
    r"^([A-Za-z]{3})-(\d{2,4})$"
)

df["월"] = date_parts[0].map(month_map)

year_text = date_parts[1]

df["연도"] = pd.to_numeric(year_text, errors="coerce")

# 두 자리 연도 처리
two_digit = year_text.str.len() == 2

df.loc[two_digit, "연도"] = df.loc[
    two_digit, "연도"
].apply(
    lambda y: 2000 + y if y <= 68 else 1900 + y
)

df["평균기온(℃)"] = pd.to_numeric(
    df["평균기온(℃)"],
    errors="coerce"
)

df = df.dropna(
    subset=["연도", "월", "평균기온(℃)"]
)

df["연도"] = df["연도"].astype(int)
df["월"] = df["월"].astype(int)

# 동일한 연도와 월에 여러 기록이 있으면 평균 계산
monthly_df = (
    df.groupby(["연도", "월"])["평균기온(℃)"]
    .mean()
    .reset_index()
)

if monthly_df.empty:
    st.error("분석할 수 있는 기온 데이터가 없습니다.")
    st.stop()

month_names = {
    1: "1월", 2: "2월", 3: "3월",
    4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월",
    10: "10월", 11: "11월", 12: "12월"
}

# ----------------------------------
# 4. 사용자 입력
# ----------------------------------
st.subheader("🔎 분석 조건 선택")

col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "분석할 월을 선택하세요.",
        options=list(range(1, 13)),
        format_func=lambda x: month_names[x],
        index=0
    )

with col2:
    max_year = int(monthly_df["연도"].max())

    prediction_year = st.number_input(
        "예측할 연도를 입력하세요.",
        min_value=1900,
        max_value=2100,
        value=min(max_year + 1, 2100),
        step=1
    )

# 선택한 월의 데이터
selected_df = monthly_df[
    monthly_df["월"] == selected_month
].copy()

selected_df = selected_df.sort_values("연도")

if len(selected_df) < 2:
    st.warning("선형회귀 예측을 위해 최소 2개 연도의 데이터가 필요합니다.")
    st.stop()

# ----------------------------------
# 5. 선형회귀 학습
# ----------------------------------
X = selected_df[["연도"]]
y = selected_df["평균기온(℃)"]

model = LinearRegression()
model.fit(X, y)

# 미래 기온 예측
prediction = model.predict(
    pd.DataFrame({"연도": [int(prediction_year)]})
)[0]

# 회귀선 계산
start_year = min(
    int(selected_df["연도"].min()),
    int(prediction_year)
)

end_year = max(
    int(selected_df["연도"].max()),
    int(prediction_year)
)

line_years = np.linspace(
    start_year,
    end_year,
    200
)

line_temps = model.predict(
    pd.DataFrame({"연도": line_years})
)

# ----------------------------------
# 6. 예측 결과 출력
# ----------------------------------
st.divider()

st.subheader(
    f"📊 {month_names[selected_month]} 평균기온 예측 결과"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "예측 연도",
        f"{int(prediction_year)}년"
    )

with col2:
    st.metric(
        "예측 평균기온",
        f"{prediction:.2f} ℃"
    )

with col3:
    st.metric(
        "분석 데이터 개수",
        f"{len(selected_df)}개 연도"
    )

# ----------------------------------
# 7. 그래프 시각화
# ----------------------------------
st.subheader("📈 과거 기온과 선형회귀 예측 그래프")

fig = go.Figure()

# 과거 실제 기온 데이터
fig.add_trace(
    go.Scatter(
        x=selected_df["연도"],
        y=selected_df["평균기온(℃)"],
        mode="markers",
        name="실제 평균기온",
        marker=dict(
            size=9,
            color="#3498db"
        ),
        hovertemplate=
        "%{x}년<br>실제 평균기온: %{y:.2f}℃<extra></extra>"
    )
)

# 회귀선
fig.add_trace(
    go.Scatter(
        x=line_years,
        y=line_temps,
        mode="lines",
        name="선형회귀 예측선",
        line=dict(
            color="#e74c3c",
            width=3
        ),
        hovertemplate=
        "연도: %{x:.1f}<br>회귀선: %{y:.2f}℃<extra></extra>"
    )
)

# 잔차(실제값과 예측값의 차이) 표시
residual_x = []
residual_y = []

for _, row in selected_df.iterrows():

    actual_year = int(row["연도"])
    actual_temp = row["평균기온(℃)"]

    fitted_temp = model.predict(
        pd.DataFrame({"연도": [actual_year]})
    )[0]

    residual_x.extend([actual_year, actual_year, None])
    residual_y.extend([actual_temp, fitted_temp, None])

fig.add_trace(
    go.Scatter(
        x=residual_x,
        y=residual_y,
        mode="lines",
        name="예측 오차(잔차)",
        line=dict(
            color="gray",
            width=1,
            dash="dot"
        ),
        hoverinfo="skip"
    )
)

# 미래 예측 지점
fig.add_trace(
    go.Scatter(
        x=[int(prediction_year)],
        y=[prediction],
        mode="markers+text",
        name="미래 기온 예측",
        marker=dict(
            size=17,
            color="#f39c12",
            symbol="star"
        ),
        text=[f"{prediction:.2f}℃"],
        textposition="top center",
        hovertemplate=
        "예측 연도: %{x}년<br>예측 기온: %{y:.2f}℃<extra></extra>"
    )
)

# 예측 연도 표시선
fig.add_vline(
    x=int(prediction_year),
    line_dash="dash",
    line_color="#f39c12",
    opacity=0.7
)

fig.update_layout(
    title=f"{month_names[selected_month]} 연도별 평균기온 및 미래 예측",
    xaxis_title="연도",
    yaxis_title="평균기온 (℃)",
    hovermode="closest",
    template="plotly_white",
    height=600,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# 8. 선형회귀 알고리즘 설명
# ----------------------------------
st.divider()

st.subheader("📚 선형회귀 알고리즘이란?")

st.write("""
선형회귀는 과거에 수집한 데이터를 이용하여
두 변수 사이의 관계를 직선으로 나타내고,
그 직선을 이용해 새로운 값을 예측하는 알고리즘입니다.
""")

st.markdown("### ① 실제 데이터 수집")

st.write("""
파란색 점은 CSV 파일에 기록된 실제 월평균기온입니다.
각 점은 해당 연도의 평균기온을 나타냅니다.
""")

st.markdown("### ② 가장 적합한 직선 찾기")

st.write("""
빨간색 선은 선형회귀 알고리즘이 찾은 예측선입니다.

실제 데이터 점들과 직선 사이의 거리(오차)를
종합적으로 줄이는 방향으로 직선의 기울기와 위치를 결정합니다.
""")

st.markdown("### ③ 예측 오차 확인")

st.write("""
회색 점선은 실제 기온과 회귀선이 예측한 기온의 차이입니다.
이 차이를 잔차라고 합니다.

잔차가 작을수록 해당 데이터에 대한 예측값이
실제값에 가깝다는 뜻입니다.
""")

st.markdown("### ④ 미래 기온 예측")

st.write(f"""
학습한 직선을 이용하여 {int(prediction_year)}년
{month_names[selected_month]}의 평균기온을 예측합니다.

이번 분석의 예측 결과는 **{prediction:.2f}℃**입니다.
""")

st.markdown("### 선형회귀의 기본 원리")

st.latex(r"y = ax + b")

st.write("""
- x: 연도
- y: 예측 평균기온
- a: 직선의 기울기
- b: y절편

기울기가 양수이면 시간이 지날수록 기온이 상승하는 경향이고,
음수이면 하락하는 경향을 나타냅니다.
""")

# ----------------------------------
# 9. 회귀 분석 정보
# ----------------------------------
st.subheader("📋 선형회귀 분석 정보")

st.write(
    f"**기울기:** {model.coef_[0]:.4f}"
)

st.write(
    f"**절편:** {model.intercept_:.2f}"
)

st.write(
    f"**결정계수(R²):** {model.score(X, y):.4f}"
)

st.caption(
    "※ 결정계수(R²)는 회귀모델이 과거 데이터의 변화를 "
    "얼마나 설명하는지 나타냅니다. 미래 예측의 정확도를 보장하지는 않습니다."
)

# ----------------------------------
# 10. 원본 데이터 확인
# ----------------------------------
with st.expander("📁 분석에 사용된 데이터 확인하기"):
    st.dataframe(
        selected_df.rename(
            columns={
                "연도": "연도",
                "평균기온(℃)": "평균기온(℃)"
            }
        ),
        use_container_width=True
    )

st.info(
    "이 결과는 과거 데이터의 선형적인 추세를 이용한 통계적 예측입니다. "
    "실제 기온은 기후 변화, 자연환경 등 다양한 요인으로 달라질 수 있습니다."
)


import streamlit as st
import pandas as pd
from pathlib import Path

# 현재 파이썬 파일 위치
current_dir = Path(__file__).resolve().parent

# CSV 파일 검색 위치
search_paths = [
    current_dir / "temperature.csv",
    current_dir.parent / "temperature.csv",
    Path.cwd() / "temperature.csv",
    Path.cwd().parent / "temperature.csv"
]

# CSV 파일 찾기
csv_path = next(
    (p for p in search_paths if p.is_file()),
    None
)

if csv_path is None:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")

    st.write("현재 작업 폴더:", Path.cwd())
    st.write("파이썬 파일 위치:", current_dir)

    st.write("검색한 경로:")
    for p in search_paths:
        st.write(str(p), " - ", p.exists())

    st.stop()

# CSV 읽기
try:
    try:
        df = pd.read_csv(csv_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

    st.success("temperature.csv 파일을 정상적으로 불러왔습니다.")

except Exception as e:
    st.error(f"CSV 파일 읽기 오류: {e}")
    st.stop()
