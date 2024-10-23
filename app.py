import streamlit as st
import pandas as pd

# 첨부한 파일 경로
file_path = './지오코딩_결과.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path)

# '대지위치' 컬럼에서 동 정보가 포함된 행을 찾기 위한 '동' 컬럼 추가
df['동'] = df['대지위치'].apply(lambda x: x.split()[1] if pd.notna(x) and len(x.split()) > 1 else '')

# 사이드바에 select box를 활용하여 동을 선택한 다음 그에 해당하는 행만 추출
st.sidebar.title('광명시 건축 인허가 데이터🏢')

select_multi_species = st.sidebar.multiselect(
    '확인하고자 하는 동을 선택해 주세요. 복수선택가능',
    ['전체', '가학동', '광명동', '노온사동', '소하동', '옥길동', '일직동', '철산동', '하안동'],
    default='전체'
)

# '착공예정일', '실착공일', '사용승인일'에서 NaN 또는 빈 값이 있는 행을 제외
df = df.dropna(subset=['착공예정일', '실착공일', '사용승인일'])

# '착공예정일', '실착공일', '사용승인일'을 str로 변환하여 연도, 월을 추출하기 쉽게 함
df['착공예정일'] = df['착공예정일'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
df['실착공일'] = df['실착공일'].apply(lambda x: str(int(x)) if pd.notna(x) else '')
df['사용승인일'] = df['사용승인일'].apply(lambda x: str(int(x)) if pd.notna(x) else '')

# 각 일자에서 연도 및 월 추출
df['착공_연도'] = df['착공예정일'].apply(lambda x: x[:4] if x else None)
df['착공_월'] = df['착공예정일'].apply(lambda x: x[4:6] if x else None)

df['실착공_연도'] = df['실착공일'].apply(lambda x: x[:4] if x else None)
df['실착공_월'] = df['실착공일'].apply(lambda x: x[4:6] if x else None)

df['사용승인_연도'] = df['사용승인일'].apply(lambda x: x[:4] if x else None)
df['사용승인_월'] = df['사용승인일'].apply(lambda x: x[4:6] if x else None)

# 각 일자별로 연도 및 월 범위 슬라이더 추가 (착공, 실착공, 사용승인)

# 착공예정일 슬라이더
st.sidebar.title("착공예정일 필터링")
min_start_year = int(df['착공_연도'].min())
max_start_year = int(df['착공_연도'].max())
selected_start_year_range = st.sidebar.slider(
    '착공예정 연도 범위 선택',
    min_value=min_start_year, max_value=max_start_year, value=(min_start_year, max_start_year)
)

selected_start_month_range = st.sidebar.slider(
    '착공예정 월 범위 선택',
    min_value=1, max_value=12, value=(1, 12)
)

# 실착공일 슬라이더
st.sidebar.title("실착공일 필터링")
min_actual_start_year = int(df['실착공_연도'].min())
max_actual_start_year = int(df['실착공_연도'].max())
selected_actual_start_year_range = st.sidebar.slider(
    '실착공 연도 범위 선택',
    min_value=min_actual_start_year, max_value=max_actual_start_year, value=(min_actual_start_year, max_actual_start_year)
)

selected_actual_start_month_range = st.sidebar.slider(
    '실착공 월 범위 선택',
    min_value=1, max_value=12, value=(1, 12)
)

# 사용승인일 슬라이더
st.sidebar.title("사용승인일 필터링")
min_approval_year = int(df['사용승인_연도'].min())
max_approval_year = int(df['사용승인_연도'].max())
selected_approval_year_range = st.sidebar.slider(
    '사용승인 연도 범위 선택',
    min_value=min_approval_year, max_value=max_approval_year, value=(min_approval_year, max_approval_year)
)

selected_approval_month_range = st.sidebar.slider(
    '사용승인 월 범위 선택',
    min_value=1, max_value=12, value=(1, 12)
)

# 선택된 범위로 데이터 필터링
start_year, end_year = selected_start_year_range
start_month, end_month = selected_start_month_range

actual_start_year, actual_end_year = selected_actual_start_year_range
actual_start_month, actual_end_month = selected_actual_start_month_range

approval_start_year, approval_end_year = selected_approval_year_range
approval_start_month, approval_end_month = selected_approval_month_range

# 필터링
filtered_df = df[
    (df['착공_연도'].astype(int) >= start_year) & (df['착공_연도'].astype(int) <= end_year) &
    (df['착공_월'].astype(int) >= start_month) & (df['착공_월'].astype(int) <= end_month) &
    (df['실착공_연도'].astype(int) >= actual_start_year) & (df['실착공_연도'].astype(int) <= actual_end_year) &
    (df['실착공_월'].astype(int) >= actual_start_month) & (df['실착공_월'].astype(int) <= actual_end_month) &
    (df['사용승인_연도'].astype(int) >= approval_start_year) & (df['사용승인_연도'].astype(int) <= approval_end_year) &
    (df['사용승인_월'].astype(int) >= approval_start_month) & (df['사용승인_월'].astype(int) <= approval_end_month)
]

# 선택된 동이 포함된 행 필터링
if '전체' not in select_multi_species:
    # 사용자가 선택한 동이 '대지위치' 텍스트에 포함된 경우를 필터링
    filtered_df = filtered_df[filtered_df['대지위치'].apply(lambda x: any(dong in x for dong in select_multi_species))]

# '동' 컬럼 삭제 후 출력
filtered_df = filtered_df.drop(columns=['동'])

# 필터링된 데이터 테이블 출력
st.write(f"선택된 착공예정 연도 범위: {start_year} - {end_year}, 월 범위: {start_month} - {end_month}")
st.write(f"선택된 실착공 연도 범위: {actual_start_year} - {actual_end_year}, 월 범위: {actual_start_month} - {actual_end_month}")
st.write(f"선택된 사용승인 연도 범위: {approval_start_year} - {approval_end_year}, 월 범위: {approval_start_month} - {approval_end_month}")
st.write(filtered_df)
