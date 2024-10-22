import os
import pandas as pd
import googlemaps
import time
from dotenv import load_dotenv
from tkinter import Tk
from tkinter.filedialog import askdirectory

# .env 파일에서 환경변수 로드
load_dotenv()

# 구글맵 API 키를 환경변수에서 가져오기
my_key = os.getenv('GOOGLE_MAPS_API_KEY')
maps = googlemaps.Client(key=my_key)  # 구글맵 API 클라이언트 설정

# 폴더 선택창 열기
def choose_directory():
    Tk().withdraw()  # Tkinter 창을 숨기기
    folder_path = askdirectory()  # 폴더 선택창 열기
    return folder_path

# 선택한 폴더의 모든 .xlsx 파일을 찾는 함수 (하위 폴더 포함)
def find_xlsx_files(folder_path):
    xlsx_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".xlsx"):
                xlsx_files.append(os.path.join(root, file))
    return xlsx_files

# 선택한 폴더로부터 .xlsx 파일 로드
folder_path = choose_directory()
xlsx_files = find_xlsx_files(folder_path)

# 지오코딩 결과를 저장할 DataFrame
all_data = pd.DataFrame()

# 지오코딩 처리 및 CSV 파일로 저장
for file_path in xlsx_files:
    print(f"처리 중: {file_path}")
    # 엑셀 파일 로드
    df = pd.read_excel(file_path, sheet_name='허가_기본', skiprows=1)

    # '대지위치' 열에서 NaN 값을 제거한 후 인덱스 초기화
    df_cleaned = df.dropna(subset=['대지위치']).reset_index(drop=True)

    # '대지위치', '착공예정일', '실착공일', '사용승인일' 컬럼만 추출
    df_locations = df_cleaned[['대지위치', '착공예정일', '실착공일', '사용승인일']]

    # 지오코딩 결과 저장을 위한 리스트
    lat = []  # 위도
    lng = []  # 경도

    t1 = time.time()  # 지오코딩 시작 시각

    # 지오코딩 처리
    for i, address in enumerate(df_locations['대지위치']):
        try:
            # 구글맵 지오코딩 API 호출
            geo_location = maps.geocode(address)

            if geo_location:
                location = geo_location[0].get('geometry', {}).get('location', {})
                lat.append(location.get('lat', ''))
                lng.append(location.get('lng', ''))
            else:
                lat.append('')
                lng.append('')
                print(f"{i + 1}번 인덱스: 주소 '{address}'에 대한 지오코딩 결과가 없습니다.")

            # Google Maps API 사용 제한을 피하기 위한 대기 시간 설정 (기본적으로 1초)
            time.sleep(1)

        except Exception as e:
            lat.append('')
            lng.append('')
            print(f"{i + 1}번 인덱스 에러: {str(e)}")

    # 지오코딩 총 실행 시간 출력
    print(f"총 소요 시간: {time.time() - t1} 초")

    # 위도, 경도 데이터를 데이터프레임에 추가
    df_locations['위도'] = lat
    df_locations['경도'] = lng

    # 처리한 데이터를 all_data에 추가
    all_data = pd.concat([all_data, df_locations])

# 모든 데이터를 하나의 CSV 파일로 저장
all_data.to_csv("지오코딩_결과.csv", index=False, encoding='utf-8-sig')

