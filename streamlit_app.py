import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 동네별 부동산 가격 변동 분석")

# 1. 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        # 2. 파일 읽기 (인코딩 문제 있을 수 있어 cp949 → utf-8 시도)
        try:
            df = pd.read_csv(uploaded_file, encoding="cp949")
        except:
            df = pd.read_csv(uploaded_file, encoding="utf-8")

        # 3. 컬럼명 미리 보기
        st.subheader("📌 데이터 미리 보기")
        st.dataframe(df.head())

        # 4. 날짜 컬럼 변환
        # 예시: '년월' 또는 '기준연월' 등의 컬럼이 있을 경우
        date_col = st.selectbox("날짜 컬럼을 선택하세요", df.columns)

        try:
            df[date_col] = pd.to_datetime(df[date_col], format="%Y-%m")
        except:
            try:
                df[date_col] = pd.to_datetime(df[date_col], format="mixed")
            except:
                st.error("날짜 형식이 맞지 않아 변환할 수 없습니다.")
                st.stop()

        # 5. 지역 컬럼 선택
        region_col = st.selectbox("지역(구/동) 컬럼을 선택하세요", df.columns)

        # 6. 가격 컬럼 선택
        price_col = st.selectbox("가격 컬럼을 선택하세요", df.columns)

        # 7. 특정 지역 선택
        selected_regions = st.multiselect(
            "비교할 지역을 선택하세요", options=df[region_col].unique(), default=df[region_col].unique()[:3]
        )

        # 8. 필터링
        filtered_df = df[df[region_col].isin(selected_regions)]

        # 9. 시각화
        st.subheader("📈 지역별 부동산 가격 추이")
        fig = px.line(
            filtered_df,
            x=date_col,
            y=price_col,
            color=region_col,
            markers=True,
            labels={date_col: "날짜", price_col: "가격", region_col: "지역"},
            title="지역별 가격 변동 추이"
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("왼쪽 사이드바에서 CSV 파일을 먼저 업로드해주세요.")
