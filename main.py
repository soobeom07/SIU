import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
df1 = pd.read_csv("동단위_데이터.csv")  # 동 단위 데이터 파일명에 맞게 수정
df2 = pd.read_csv("구단위_데이터.csv", encoding="cp949")  # 구 단위 데이터

# 컬럼명 정리
df1 = df1.rename(columns={
    '행정구역': '지역',
    '물건수': '거래건수',
    '토지면적': '토지면적_㎡',
    '건축물면적': '건축물면적_㎡',
    '금액': '거래금액_백만원'
})

df2 = df2.rename(columns={
    '행정구역': '지역',
    '거래신고(물건수)': '거래건수',
    '거래신고 토지면적(제곱미터)': '토지면적_㎡',
    '거래신고건축물면적(제곱미터)': '건축물면적_㎡',
    '거래신고 금액(백만원)': '거래금액_백만원'
})

# Streamlit UI 설정
st.set_page_config(page_title="부동산 가격 분석 대시보드", layout="wide")
st.title("🏙️ 지역별 부동산 거래 분석")

# 데이터 선택
data_option = st.sidebar.radio("분석할 데이터 선택", ("동 단위", "구 단위"))
if data_option == "동 단위":
    df = df1.copy()
else:
    df = df2.copy()

지역_선택 = st.sidebar.selectbox("지역 선택", df['지역'].unique())
filtered = df[df['지역'] == 지역_선택]

# 요약 정보 출력
st.subheader(f"📌 {지역_선택} 거래 요약")
st.write(filtered)

col1, col2, col3 = st.columns(3)
col1.metric("거래 건수", int(filtered['거래건수'].values[0]))
col2.metric("토지 면적 (㎡)", f"{filtered['토지면적_㎡'].values[0]:,.2f}")
col3.metric("건축물 면적 (㎡)", f"{filtered['건축물면적_㎡'].values[0]:,.2f}")

# 시각화
st.subheader("📊 지역별 거래 금액 비교")
fig = px.bar(df.sort_values('거래금액_백만원', ascending=False), x='지역', y='거래금액_백만원',
             labels={'거래금액_백만원': '거래 금액 (백만원)'}, color='거래금액_백만원')
st.plotly_chart(fig, use_container_width=True)

# 산점도: 면적 대비 금액
st.subheader("💡 면적 대비 거래 금액")
fig2 = px.scatter(df, x='토지면적_㎡', y='거래금액_백만원', size='건축물면적_㎡',
                  hover_name='지역', trendline='ols',
                  labels={'토지면적_㎡': '토지 면적 (㎡)', '거래금액_백만원': '거래 금액 (백만원)'})
st.plotly_chart(fig2, use_container_width=True)

# 푸터
st.caption("데이터 출처: 공공데이터포털 / 서울열린데이터광장 등 공개 데이터")
