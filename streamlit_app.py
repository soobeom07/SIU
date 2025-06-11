import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="인천시 부동산 거래 분석", layout="wide")
st.title("🏙️ 인천시 부동산 거래 분석 대시보드")

# 데이터 불러오기
df = pd.read_csv("인천광역시_부동산 거래 현황_20231231.csv", encoding="cp949")

# 컬럼명 정리
df = df.rename(columns={
    '행정구역': '지역',
    '거래신고(물건수)': '거래건수',
    '거래신고 토지면적(제곱미터)': '토지면적_㎡',
    '거래신고건축물면적(제곱미터)': '건축물면적_㎡',
    '거래신고 금액(백만원)': '거래금액_백만원'
})

# 데이터 타입 정리 (숫자형 변환)
numeric_cols = ['거래건수', '토지면적_㎡', '건축물면적_㎡', '거래금액_백만원']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

# 사이드바 지역 선택
지역_선택 = st.sidebar.selectbox("📍 지역 선택", df['지역'].unique())
filtered = df[df['지역'] == 지역_선택]

# 요약 정보
st.subheader(f"📌 {지역_선택} 거래 요약")
st.write(filtered)

col1, col2, col3 = st.columns(3)
col1.metric("거래 건수", int(filtered['거래건수'].sum()))
col2.metric("토지 면적 (㎡)", f"{filtered['토지면적_㎡'].sum():,.2f}")
col3.metric("건축물 면적 (㎡)", f"{filtered['건축물면적_㎡'].sum():,.2f}")

# 지역별 거래금액 비교
st.subheader("💰 지역별 거래 금액 비교")
df_grouped = df.groupby('지역')[['거래금액_백만원']].sum().reset_index()
fig = px.bar(df_grouped.sort_values('거래금액_백만원', ascending=False),
             x='지역', y='거래금액_백만원',
             labels={'거래금액_백만원': '거래 금액 (백만원)'},
             color='거래금액_백만원')
st.plotly_chart(fig, use_container_width=True)

# 산점도: 면적 대비 거래금액 (회귀선 제거)
st.subheader("📈 면적 대비 거래 금액 분석")
fig2 = px.scatter(df,
                  x='토지면적_㎡', y='거래금액_백만원',
                  size='건축물면적_㎡', hover_name='지역',
                  labels={
                      '토지면적_㎡': '토지 면적 (㎡)',
                      '거래금액_백만원': '거래 금액 (백만원)'
                  })
st.plotly_chart(fig2, use_container_width=True)

# 출처
st.caption("데이터 출처: 인천시 공개 데이터")
