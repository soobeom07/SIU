import streamlit as st
import pandas as pd
import plotly.express as px

# 기본 설정
st.set_page_config(page_title="인천 아파트 거래 분석", layout="wide")
st.title("🏙️ 인천 아파트 거래 분석 대시보드")

# 데이터 불러오기
df = pd.read_csv("66083188-77a1-44b2-8105-b7f3f25d937c.csv", encoding="cp949")

# 날짜 칼럼 만들기
df['계약일자'] = pd.to_datetime(df['계약년월'].astype(str) + df['계약일'].astype(str).str.zfill(2), format='%Y-%m%d', errors='coerce')

# 숫자형 변환
df['거래금액(만원)'] = pd.to_numeric(df['거래금액(만원)'], errors='coerce')
df['전용면적(제곱미터)'] = pd.to_numeric(df['전용면적(제곱미터)'], errors='coerce')

# 지역 목록
df['지역'] = df['시군구'].str.split().str[2]
selected_area = st.sidebar.selectbox("📍 지역 선택", df['지역'].unique())

df_filtered = df[df['지역'] == selected_area]

# 요약 정보
st.subheader(f"📊 {selected_area} 지역 아파트 거래 요약")
col1, col2, col3 = st.columns(3)
col1.metric("총 거래 건수", len(df_filtered))
col2.metric("평균 거래 금액 (만원)", f"{df_filtered['거래금액(만원)'].mean():,.0f}")
col3.metric("평균 전용면적 (㎡)", f"{df_filtered['전용면적(제곱미터)'].mean():,.1f}")

# 📈 월별 거래 금액 추이
st.subheader("📉 월별 거래 금액 추이")
df_filtered['계약연월'] = df_filtered['계약일자'].dt.to_period('M').astype(str)
monthly_trend = df_filtered.groupby('계약연월')['거래금액(만원)'].mean().reset_index()

fig1 = px.line(monthly_trend,
               x='계약연월', y='거래금액(만원)',
               title=f"{selected_area} 월별 평균 거래 금액",
               markers=True)
st.plotly_chart(fig1, use_container_width=True)

# 🏠 단지별 누적 거래 금액
st.subheader("🏘️ 단지별 누적 거래 금액")
top_danjis = df_filtered.groupby('단지명')['거래금액(만원)'].sum().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(top_danjis,
              x='단지명', y='거래금액(만원)',
              title=f"{selected_area} 단지별 누적 거래 금액 Top 10",
              labels={'거래금액(만원)': '누적 거래금액(만원)'},
              color='거래금액(만원)')
st.plotly_chart(fig2, use_container_width=True)

# 🔎 데이터 테이블
with st.expander("🔍 원본 데이터 확인"):
    st.dataframe(df_filtered)
