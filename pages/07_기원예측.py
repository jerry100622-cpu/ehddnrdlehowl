
# ----------------------------------
# CSV 파일 불러오기
# ----------------------------------
from pathlib import Path

current_dir = Path(__file__).resolve().parent

# pages 폴더의 상위 폴더에서 CSV 찾기
csv_path = current_dir.parent / "temperature.csv"

if not csv_path.exists():
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.write("현재 파이썬 파일 위치:", str(current_dir))
    st.write("찾으려는 CSV 위치:", str(csv_path))
    st.stop()

try:
    try:
        df = pd.read_csv(csv_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")

except Exception as e:
    st.error(f"CSV 파일 읽기 오류: {e}")
    st.stop()

