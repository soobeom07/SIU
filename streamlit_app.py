import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 동네별 부동산 가격 변동 분석")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        # CSV 읽기
        try:
            df = pd.read_csv(uploaded_file, encoding='cp949')
        except:
            df = pd.read_csv(uploaded_file, encoding='utf-8')

        st.subheader("📌 데이터 미리 보기")
        st.dataframe(df.head())

        # 날짜, 지역, 가격 컬럼 선택
        date_col = st.selectbox("날짜 컬럼 선택", df.columns)
        region_col = st.selectbox("지역 컬럼 선택", df.columns)
        price_col = st.selectbox("가격 컬럼 선택", df.columns)

        # 날짜 전처리
        df[date_col] = df[date_col].astype(str).str.strip()  # 공백 제거
        df[date_col] = df[date_col].str.replace(".", "-").str.replace("/", "-")  # . 또는 / → -
        df[date_col] = pd.to_datetime(df[date_col], format="mixed", errors="coerce")

        # 유효하지 않은 날짜 제거
        df = df.dropna(subset=[date_col])

        # 지역 선택
        selected_regions = st.multiselect(
            "비교할 지역 선택", options=df[region_col].unique(), default=df[region_col].unique()[:3]
        )

        # 필터링
        filtered_df = df[df[region_col].isin(selected_regions)]

        # 시각화
        st.subheader("📈 지역별 가격 추이")
        fig = px.line(
            filtered_df,
            x=date_col,
            y=price_col,
            color=region_col,
            markers=True,
            labels={date_col: "날짜", price_col: "가격", region_col: "지역"},
            title="지역별 부동산 가격 변동"
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("왼쪽에서 CSV 파일을 업로드해주세요.")
