import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("69768554-e323-4172-a2de-cf273531be36.csv", encoding='cp949')
    df['계약년월'] = pd.to_datetime(df['계약년월'], format='%Y-%m')
    df['거래금액(만원)'] = df['거래금액(만원)'].astype(int)
    df['동'] = df['시군구'].str.split().str[2]
    return df

df = load_data()

st.title("🏘️ 동네별 부동산 가격 변동 분석")

# 동 선택
dong_options = df['동'].value_counts().index.tolist()
selected_dongs = st.multiselect("동네를 선택하세요", dong_options, default=dong_options[:3])

# 필터링
filtered = df[df['동'].isin(selected_dongs)]

# 월별 평균 가격 계산
monthly_avg = filtered.groupby(['계약년월', '동'])['거래금액(만원)'].mean().reset_index()

# Plotly 그래프
fig = px.line(monthly_avg, x='계약년월', y='거래금액(만원)', color='동',
              markers=True, title='동네별 월별 평균 거래금액 추이')
st.plotly_chart(fig)

# 최근 월 기준 평균 거래금액 표시
latest_month = monthly_avg['계약년월'].max()
latest_data = monthly_avg[monthly_avg['계약년월'] == latest_month]
st.subheader(f"📊 {latest_month.strftime('%Y-%m')} 기준 평균 거래금액")
st.dataframe(latest_data.set_index('동')[['거래금액(만원)']].sort_values(by='거래금액(만원)', ascending=False))

# 원본 데이터 확인
with st.expander("📂 원본 데이터 보기"):
    st.dataframe(df)
