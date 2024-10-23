# 광명시 건축 인허가 데이터 전처리

광명시의 건축 인허가 데이터를 원본 `.xlsx` 파일로부터 하나의 CSV 파일로 추출합니다. 이를 위해, Google Maps API를 사용하여 주소 데이터를 지오코딩하여 위도와 경도 정보를 추가합니다.

## 설치 방법

### 1. Python 환경 설정
**Python 3.11** 버전 설치 후 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. .env 파일 설정
[Google Maps Platform](https://mapsplatform.google.com/)에서 API 키 생성후 .env 파일에 추가 
```
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

## 데이터 수집
1. [세움터](https://https://www.eais.go.kr/) 웹사이트에 접속
2. 상단 메뉴에서 정보 탭을 클릭한 후 인허가 정보로 이동
3. 기간 및 대지 위치를 지정하여 광명시의 건축 인허가 정보를 검색
4. 검색된 데이터를 엑셀(.xlsx) 형식으로 다운로드
   
## 사용법
```
python main.py
```

## streamlit
데이터 테이블을 시각화하고, 동별 및 연도/월별 필터링 기능을 제공
```
streamlit run app.py
```