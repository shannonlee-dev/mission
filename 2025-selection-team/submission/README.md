# Codyssey Team 프로젝트

## 프로젝트 설명
이 프로젝트는 Python 3을 기반으로 하며, pandas와 matplotlib 라이브러리를 사용하여 지역 맵 데이터를 분석하고 시각화하는 프로젝트입니다.

## 개발 환경 설정

### 필수 요구사항
- Python 3.8 이상
- pip (Python 패키지 관리자)

### 환경 설정 방법

#### 1. 저장소 클론
```bash
git clone [저장소 URL]
cd codyssey-team
```

#### 2. 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

#### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

#### 4. 환경 확인
```bash
# 설치된 패키지 확인
pip list

# Python 버전 확인
python --version
```

### 주요 라이브러리
- `pandas`: CSV 데이터 읽기 및 조작
- `matplotlib`: 데이터 시각화 및 이미지 생성
- `pytest`: 테스트 프레임워크

### 데이터 파일
프로젝트에서 사용하는 CSV 파일들:
- `data/area_map.csv`: 지역 맵 기본 데이터 (좌표 정보)
- `data/area_struct.csv`: 구조물 위치 및 타입 데이터
- `data/area_category.csv`: 구조물 타입 ID와 이름 매핑 데이터

### 프로젝트 구조
```
codyssey-team/
├── data/                   # 데이터 파일들
├── test/                   # 테스트 파일들
├── mas_map.py             # Stage 1: 데이터 분석
├── map_draw.py            # Stage 2: 맵 시각화
├── map_direct_save.py     # Stage 3: 경로 찾기
├── requirements.txt       # 패키지 의존성
└── README.md             # 이 파일
```

### 실행 방법
```bash
# 가상환경이 활성화된 상태에서:
python mas_map.py          # 데이터 분석
python map_draw.py         # 맵 시각화  
python map_direct_save.py  # 경로 찾기
```

### 테스트 실행
```bash
# 모든 테스트 실행
python -m pytest test/

# 특정 테스트 실행
python -m pytest test/test_mas_map.py
```

### 출력 파일
- `map.png`: 기본 맵 이미지
- `map_final.png`: 최종 맵 이미지
- `home_to_cafe.csv`: 집에서 카페까지의 경로 데이터

## 문제 해결

### 가상환경 관련
- 가상환경이 제대로 활성화되었는지 확인: `which python`
- 가상환경을 재생성해야 하는 경우: `.venv` 폴더 삭제 후 다시 생성

### 패키지 설치 오류
- pip 업데이트: `pip install --upgrade pip`
- 패키지별 설치: `pip install pandas matplotlib pytest`

### 권한 문제 (macOS/Linux)
- sudo 없이 설치: `pip install --user -r requirements.txt`

## 기여 방법
1. 이슈 생성 또는 기존 이슈 확인
2. 새 브랜치 생성
3. 변경사항 커밋
4. Pull Request 생성

## 코딩 스타일
- PEP 8 준수
- 함수와 변수명: snake_case
- 클래스명: PascalCase
- 주석과 문서화: 한국어 사용
