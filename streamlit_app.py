import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="부동산 가격 변동 분석", layout="wide")
st.title("🏠 동네별 부동산 가격 변동 분석")

# CSV 업로드
uploaded_file = st.file_uploader("📁 부동산 거래 CSV 파일을 업로드하세요 (인코딩: CP949)", type="csv")

if uploaded_file:
    try:
        # CSV 읽기
        df = pd.read_csv(uploaded_file, encoding='cp949')

        # 전처리
        df['계약년월'] = pd.to_datetime(df['계약년월'], format='%Y%m')  # 예: 202401 → 2024-01-01
        df['거래금액(만원)'] = df['거래금액(만원)'].astype(str).str.replace(',', '').astype(int)
        df['동'] = df['시군구'].str.split().str[2]

        # 동 선택
        dong_list = sorted(df['동'].unique())
        selected_dong = st.multiselect("📌 분석할 동을 선택하세요", dong_list, default=dong_list[:3])

        filtered = df[df['동'].isin(selected_dong)]

        if filtered.empty:
            st.warning("선택한 동에 대한 데이터가 없습니다.")
        else:
            # 월별 평균 거래금액 계산
            monthly_avg = (
                filtered.groupby(['계약년월', '동'])['거래금액(만원)']
                .mean().reset_index()
            )

            # 라인 차트
            fig = px.line(
                monthly_avg, x='계약년월', y='거래금액(만원)', color='동',
                markers=True, title='📈 동네별 월별 평균 거래금액 추이'
            )
            st.plotly_chart(fig, use_container_width=True)

            # 최신 시점 요약
            latest_month = monthly_avg['계약년월'].max()
            latest_data = monthly_avg[monthly_avg['계약년월'] == latest_month]

            st.subheader(f"📊 {latest_month.strftime('%Y-%m')} 기준 평균 거래금액")
            st.dataframe(latest_data.sort_values(by='거래금액(만원)', ascending=False), use_container_width=True)

            # 원본 데이터 표시
            with st.expander("🔎 전체 원본 데이터 보기"):
                st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("왼쪽 사이드바 또는 위 버튼을 통해 CSV 파일을 먼저 업로드하세요.")

