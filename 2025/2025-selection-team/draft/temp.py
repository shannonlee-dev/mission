import pandas as pd

def filter_area_one(csv_path: str) -> pd.DataFrame:
    '''
    area_struct.csv 파일에서 area 값이 1인 행만 추출하여 반환하는 함수

    Args:
        csv_path (str): area_struct.csv 파일 경로

    Returns:
        pd.DataFrame: area가 1인 데이터만 포함된 DataFrame
    '''
    # CSV 파일을 읽어서 DataFrame으로 변환
    df = pd.read_csv(csv_path, dtype={'x': int, 'y': int, 'category': int, 'area': int})
    # 컬럼명에 불필요한 공백이 있으면 제거
    df.columns = df.columns.str.strip()
    # area 값이 1인 행만 필터링
    filtered_df = df[df['area'] == 1].reset_index(drop=True)
    return filtered_df

def main() -> None:

    # area_struct.csv 파일 경로 지정
    csv_file = '/home/shannon.lee.dev/codyssey-team/data/area_struct.csv'

    # area가 1인 데이터만 필터링
    result_df = filter_area_one(csv_file)


    # 결과 출력
    print(result_df)

    # 결과 행 개수 출력
    print(f'area가 1인 데이터 행 개수: {len(result_df)}')  # 결과 행 개수 출력

    # category별 개수 출력
    print('\narea가 1인 데이터의 category별 개수:')
    print(result_df['category'].value_counts().sort_index())



if __name__ == '__main__':
    main()