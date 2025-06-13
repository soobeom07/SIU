import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="지역별 부동산 가격 변동", layout="wide")
st.title("📊 지역별 부동산 가격 변동 분석")

# 데이터 불러오기
df = pd.read_csv("66083188-77a1-44b2-8105-b7f3f25d937c.csv", encoding="cp949")

# 컬럼명 확인 및 정리
st.write("✅ 현재 데이터프레임 컬럼 목록:", df.columns.tolist())

# 날짜 컬럼이 '계약일'로 가정
df = df.rename(columns={
    '계약일': '날짜',
    '지역명': '지역',
    '거래금액(만원)': '거래금액_만원'
})

# 날짜 타입으로 변환
df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
df = df.dropna(subset=['날짜'])  # 날짜 없는 행 제거
df = df.sort_values('날짜')

# 숫자형 정리
df['거래금액_만원'] = pd.to_numeric(df['거래금액_만원'], errors='coerce').fillna(0)

# 사이드바: 지역 선택
지역_목록 = df['지역'].unique()
선택_지역 = st.sidebar.multiselect("📍 분석할 지역 선택", options=지역_목록, default=지역_목록[:3])

# 필터링
filtered = df[df['지역'].isin(선택_지역)]

# 시계열 라인 그래프: 지역별 가격 변동
st.subheader("📈 지역별 거래 금액 변동 추이 (만원 기준)")
fig = px.line(filtered, x='날짜', y='거래금액_만원', color='지역',
              labels={'거래금액_만원': '거래 금액 (만원)', '날짜': '계약일'},
              title="지역별 부동산 거래 금액 시계열 추이")
st.plotly_chart(fig, use_container_width=True)

# 출처
st.caption("데이터 출처: 사용자 업로드 파일")
