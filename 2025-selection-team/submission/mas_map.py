"""
Stage 1: 데이터 수집 및 분석

이 모듈은 area_map.csv, area_struct.csv, area_category.csv 파일의 내용을 로드하고 분석합니다.
area_category.csv를 기반으로 구조물 ID를 이름으로 변환하고, 데이터셋을 병합하며,
구역 1 데이터만을 필터링합니다.
"""

import pandas as pd
import os
import sys


def load_data_files():
    """오류 처리와 함께 세 개의 CSV 파일을 로드하고 DataFrame으로 반환합니다."""
    required_files = {
        'area_map': 'data/area_map.csv',
        'area_struct': 'data/area_struct.csv', 
        'area_category': 'data/area_category.csv'
    }
    
    # 모든 필수 파일이 존재하는지 확인
    missing_files = []
    for name, path in required_files.items():
        if not os.path.exists(path):
            missing_files.append(path)
    
    if missing_files:
        print(f'❌ 오류: 다음 필수 파일들이 존재하지 않습니다:')
        for file in missing_files:
            print(f'   - {file}')
        sys.exit(1)
    
    dataframes = {}
    
    try:
        # area_map.csv 로드 (좌표 정보 및 공사장 데이터 포함)
        print('area_map.csv 로딩 중...')
        area_map_df = pd.read_csv('data/area_map.csv')
        
        # area_map.csv 구조 검증
        required_columns_map = ['x', 'y', 'ConstructionSite']
        missing_cols = [col for col in required_columns_map if col not in area_map_df.columns]
        if missing_cols:
            raise ValueError(f'area_map.csv에서 필수 컬럼이 누락되었습니다: {missing_cols}')
        
        # 빈 데이터 확인
        if area_map_df.empty:
            raise ValueError('area_map.csv가 비어있습니다.')
            
        # 중요한 컬럼에서 누락된 값 확인
        null_counts_map = area_map_df[required_columns_map].isnull().sum()
        if null_counts_map.any():
            print(f'⚠️ 경고: area_map.csv에 누락된 값이 있습니다:')
            for col, count in null_counts_map.items():
                if count > 0:
                    print(f'   - {col}: {count}개 누락')
        
        dataframes['area_map'] = area_map_df
        
        # area_struct.csv 로드 (구조물 위치 및 타입 데이터 포함)
        print('area_struct.csv 로딩 중...')
        area_struct_df = pd.read_csv('data/area_struct.csv')
        
        # area_struct.csv 구조 검증
        required_columns_struct = ['x', 'y', 'category', 'area']
        missing_cols = [col for col in required_columns_struct if col not in area_struct_df.columns]
        if missing_cols:
            raise ValueError(f'area_struct.csv에서 필수 컬럼이 누락되었습니다: {missing_cols}')
            
        # 빈 데이터 확인
        if area_struct_df.empty:
            raise ValueError('area_struct.csv가 비어있습니다.')
            
        # 중요한 컬럼에서 누락된 값 확인
        null_counts_struct = area_struct_df[required_columns_struct].isnull().sum()
        if null_counts_struct.any():
            print(f'⚠️ 경고: area_struct.csv에 누락된 값이 있습니다:')
            for col, count in null_counts_struct.items():
                if count > 0:
                    print(f'   - {col}: {count}개 누락')
        
        dataframes['area_struct'] = area_struct_df
        
        # area_category.csv 로드 (카테고리 ID에서 구조물 이름으로의 매핑 포함)
        print('area_category.csv 로딩 중...')
        area_category_df = pd.read_csv('data/area_category.csv')
        
        # area_category.csv 구조 검증
        required_columns_category = ['category', 'struct']
        # 잠재적인 컬럼명 변형 처리
        actual_columns = [col.strip() for col in area_category_df.columns]
        area_category_df.columns = actual_columns
        
        missing_cols = [col for col in required_columns_category if col not in actual_columns]
        if missing_cols:
            raise ValueError(f'area_category.csv에서 필수 컬럼이 누락되었습니다: {missing_cols}')
            
        # 빈 데이터 확인
        if area_category_df.empty:
            raise ValueError('area_category.csv가 비어있습니다.')
            
        # 중요한 컬럼에서 누락된 값 확인
        null_counts_category = area_category_df[required_columns_category].isnull().sum()
        if null_counts_category.any():
            print(f'⚠️ 경고: area_category.csv에 누락된 값이 있습니다:')
            for col, count in null_counts_category.items():
                if count > 0:
                    print(f'   - {col}: {count}개 누락')
                    
        dataframes['area_category'] = area_category_df
        
        # area_map과 area_struct 간의 좌표 일관성 확인
        map_coords = set(zip(area_map_df['x'], area_map_df['y']))
        struct_coords = set(zip(area_struct_df['x'], area_struct_df['y']))
        
        if map_coords != struct_coords:
            missing_in_struct = map_coords - struct_coords
            missing_in_map = struct_coords - map_coords
            
            if missing_in_struct:
                print(f'⚠️ 경고: area_struct.csv에서 누락된 좌표 {len(missing_in_struct)}개')
            if missing_in_map:
                print(f'⚠️ 경고: area_map.csv에서 누락된 좌표 {len(missing_in_map)}개')
        
        print('✅ 모든 데이터 파일이 성공적으로 로딩되었습니다.')
        return area_map_df, area_struct_df, area_category_df
        
    except FileNotFoundError as e:
        print(f'❌ 파일을 찾을 수 없습니다: {e}')
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f'❌ 파일이 비어있거나 잘못된 형식입니다.')
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f'❌ CSV 파일 파싱 오류: {e}')
        sys.exit(1)
    except ValueError as e:
        print(f'❌ 데이터 검증 오류: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'❌ 예상치 못한 오류가 발생했습니다: {e}')
        sys.exit(1)


def clean_category_data(area_category_df):
    """여분의 공백을 제거하고 누락된 값을 처리하여 카테고리 데이터를 정리합니다."""
    try:
        # 컬럼명과 값에서 여분의 공백 제거
        area_category_df.columns = area_category_df.columns.str.strip()
        
        # struct 컬럼이 존재하는지 확인하고 정리
        if 'struct' in area_category_df.columns:
            area_category_df['struct'] = area_category_df['struct'].str.strip()
            
            # 누락된 구조물 이름 처리
            missing_struct = area_category_df['struct'].isnull().sum()
            if missing_struct > 0:
                print(f'⚠️ 경고: {missing_struct}개의 구조물 이름이 누락되어 기본값으로 대체합니다.')
                area_category_df['struct'] = area_category_df['struct'].fillna('Unknown')
        else:
            raise ValueError('area_category.csv에 struct 컬럼이 없습니다.')
            
        # 중복된 카테고리 확인
        if area_category_df['category'].duplicated().any():
            print('⚠️ 경고: 중복된 카테고리 번호가 발견되었습니다. 첫 번째 항목을 사용합니다.')
            area_category_df = area_category_df.drop_duplicates(subset=['category'], keep='first')
            
        return area_category_df
        
    except Exception as e:
        print(f'❌ 카테고리 데이터 정리 중 오류 발생: {e}')
        raise


def convert_struct_ids_to_names(area_struct_df, area_category_df):
    """오류 처리와 함께 area_category 매핑을 사용하여 구조물 카테고리 ID를 이름으로 변환합니다."""
    try:
        # 먼저 카테고리 데이터를 정리
        area_category_df = clean_category_data(area_category_df)
        
        # area_struct_df에서 누락된 카테고리 값 확인
        missing_categories = area_struct_df['category'].isnull().sum()
        if missing_categories > 0:
            print(f'⚠️ 경고: {missing_categories}개의 카테고리 값이 누락되어 0으로 대체합니다.')
            area_struct_df['category'] = area_struct_df['category'].fillna(0)
        
        # area_struct를 area_category와 병합하여 구조물 이름 가져오기
        merged_df = pd.merge(
            area_struct_df, 
            area_category_df, 
            on='category', 
            how='left'
        )
        
        # 카테고리 0 (구조물 없음) 또는 매칭되지 않는 카테고리의 경우 구조물 이름을 'Empty'로 설정
        unmatched_count = merged_df['struct'].isnull().sum()
        if unmatched_count > 0:
            unmatched_categories = merged_df[merged_df['struct'].isnull()]['category'].unique()
            print(f'⚠️ 경고: {unmatched_count}개의 매칭되지 않은 카테고리({unmatched_categories})를 Empty로 설정합니다.')
            
        merged_df['struct'] = merged_df['struct'].fillna('Empty')
        
        # 병합 결과 검증
        if len(merged_df) != len(area_struct_df):
            print(f'⚠️ 경고: 병합 후 레코드 수가 변경되었습니다. (원본: {len(area_struct_df)}, 병합 후: {len(merged_df)})')
        
        return merged_df
        
    except Exception as e:
        print(f'❌ 구조물 ID를 이름으로 변환하는 중 오류 발생: {e}')
        raise


def merge_all_datasets(area_map_df, area_struct_with_names_df):
    """오류 처리와 함께 모든 데이터셋을 단일 DataFrame으로 병합합니다."""
    try:
        # 병합 전 좌표 불일치 확인
        map_coords = set(zip(area_map_df['x'], area_map_df['y']))
        struct_coords = set(zip(area_struct_with_names_df['x'], area_struct_with_names_df['y']))
        
        common_coords = map_coords & struct_coords
        map_only = map_coords - struct_coords  
        struct_only = struct_coords - map_coords
        
        if map_only:
            print(f'⚠️ 경고: area_map.csv에만 있는 좌표 {len(map_only)}개가 병합에서 제외됩니다.')
        if struct_only:
            print(f'⚠️ 경고: area_struct.csv에만 있는 좌표 {len(struct_only)}개가 병합에서 제외됩니다.')
        
        # area_map을 area_struct (구조물 이름 포함)와 병합
        complete_df = pd.merge(
            area_map_df,
            area_struct_with_names_df,
            on=['x', 'y'],
            how='inner'
        )
        
        # 병합 결과 검증
        if complete_df.empty:
            raise ValueError('병합 결과가 비어있습니다. 공통 좌표가 없는지 확인하세요.')
            
        print(f'✅ 데이터 병합 완료: {len(complete_df)}개 레코드 생성 (공통 좌표: {len(common_coords)}개)')
        
        return complete_df
        
    except Exception as e:
        print(f'❌ 데이터셋 병합 중 오류 발생: {e}')
        raise


def filter_area_1_data(complete_df):
    """오류 처리와 함께 구역 1 데이터만 필터링하고 구역별로 정렬하여 반환합니다."""
    try:
        # area 컬럼이 존재하고 유효한 데이터를 가지고 있는지 확인
        if 'area' not in complete_df.columns:
            raise ValueError('완성된 데이터에 area 컬럼이 없습니다.')
            
        # 구역 1 데이터가 존재하는지 확인
        area_1_count = len(complete_df[complete_df['area'] == 1])
        if area_1_count == 0:
            print('⚠️ 경고: 구역 1 데이터가 없습니다.')
            return pd.DataFrame()  # 빈 DataFrame 반환
            
        # 구역 1 데이터만 필터링
        area_1_df = complete_df[complete_df['area'] == 1].copy()
        
        # 구역별로 정렬 (모두 구역 1이지만, 그 다음 x, y 좌표순으로)
        area_1_df = area_1_df.sort_values(['area', 'x', 'y'])
        
        # 깔끔한 출력을 위해 인덱스 재설정
        area_1_df = area_1_df.reset_index(drop=True)
        
        print(f'✅ 구역 1 데이터 필터링 완료: {len(area_1_df)}개 레코드')
        
        return area_1_df
        
    except Exception as e:
        print(f'❌ 구역 1 데이터 필터링 중 오류 발생: {e}')
        raise


def analyze_data():
    """Stage 1 요구사항에 따라 데이터 분석을 수행하는 메인 함수입니다."""
    try:
        print('=== 데이터 분석 시작 ===')
        
        print('데이터 파일을 로딩하는 중...')
        area_map_df, area_struct_df, area_category_df = load_data_files()
        
        print('구조물 ID를 이름으로 변환하는 중...')
        area_struct_with_names = convert_struct_ids_to_names(area_struct_df, area_category_df)
        
        print('데이터셋을 병합하는 중...')
        complete_df = merge_all_datasets(area_map_df, area_struct_with_names)
        
        # 전체 데이터 개요 표시
        print('\n=== 전체 데이터 개요 ===')
        print(f'전체 구역의 총 레코드 수: {len(complete_df)}')
        
        # 구역 데이터가 있는지 확인
        if 'area' in complete_df.columns and not complete_df['area'].isnull().all():
            print('구역별 분포:')
            area_distribution = complete_df['area'].value_counts().sort_index()
            print(area_distribution)
        else:
            print('⚠️ 경고: 구역 정보를 사용할 수 없습니다.')
        
        # 모든 구역에서 내 집 위치 확인
        if 'struct' in complete_df.columns:
            my_home_all = complete_df[complete_df['struct'] == 'MyHome']
            if not my_home_all.empty:
                home_area = my_home_all.iloc[0]['area'] if 'area' in my_home_all.columns else '알 수 없음'
                print(f'\n내 집은 구역 {home_area}에 위치 (좌표: x={my_home_all.iloc[0]["x"]}, y={my_home_all.iloc[0]["y"]})')
            else:
                print('\n내 집 정보를 찾을 수 없습니다.')
        
        print('\n구역 1 데이터로 필터링하는 중...')
        area_1_result = filter_area_1_data(complete_df)
        
        # 구역 1 데이터가 있는지 확인
        if area_1_result.empty:
            print('❌ 구역 1 데이터가 없어 분석을 중단합니다.')
            return area_1_result
        
        # 분석 결과 표시
        print('\n=== 구역 1 분석 결과 ===')
        print(f'구역 1의 총 레코드 수: {len(area_1_result)}')
        
        if 'struct' in area_1_result.columns:
            print('\n구역 1 내 구조물 분포:')
            print(area_1_result['struct'].value_counts())
        
        if 'ConstructionSite' in area_1_result.columns:
            construction_count = area_1_result['ConstructionSite'].sum()
            print('\n구역 1 내 공사장 분포:')
            print(f'공사장: {construction_count}개')
            print(f'비공사장: {len(area_1_result) - construction_count}개')
        
        print('\n구역 1 데이터의 첫 10개 레코드:')
        print(area_1_result.head(10))
        
        if 'x' in area_1_result.columns and 'y' in area_1_result.columns:
            print('\n구역 1 내 좌표 범위:')
            print(f'X 좌표: {area_1_result["x"].min()}부터 {area_1_result["x"].max()}까지')
            print(f'Y 좌표: {area_1_result["y"].min()}부터 {area_1_result["y"].max()}까지')
        
        # 구역 1 내 특정 구조물 확인
        if 'struct' in area_1_result.columns:
            print('\n구역 1 내 특수 구조물:')
            my_home = area_1_result[area_1_result['struct'] == 'MyHome']
            bandalgom_coffee = area_1_result[area_1_result['struct'] == 'BandalgomCoffee']
            
            if not my_home.empty:
                print(f'내 집 위치: x={my_home.iloc[0]["x"]}, y={my_home.iloc[0]["y"]}')
            else:
                print('내 집이 구역 1에서 발견되지 않음 (예상됨 - 커피 분석을 위해 구역 1에 집중)')
            
            if not bandalgom_coffee.empty:
                print(f'반달곰커피 위치: {len(bandalgom_coffee)}개 발견')
                for _, cafe in bandalgom_coffee.iterrows():
                    print(f'  - 카페 위치: x={cafe["x"]}, y={cafe["y"]}')
            else:
                print('반달곰커피가 구역 1에서 발견되지 않음')
        
        return area_1_result
        
    except Exception as e:
        print(f'❌ 데이터 분석 중 치명적 오류 발생: {e}')
        print('분석을 중단합니다.')
        sys.exit(1)


if __name__ == '__main__':
    try:
        # 데이터 분석 실행
        result_df = analyze_data()
        
        if not result_df.empty:
            print('\n=== 분석 완료 ===')
            print('구역 1 데이터가 성공적으로 분석 및 필터링되었습니다.')
            print(f'최종 데이터셋에는 {len(result_df)}개의 레코드가 포함되어 있습니다.')
        else:
            print('\n=== 분석 완료 (데이터 없음) ===')
            print('구역 1 데이터가 없어 빈 데이터셋을 반환합니다.')
            
    except KeyboardInterrupt:
        print('\n\n❌ 사용자에 의해 중단되었습니다.')
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ 프로그램 실행 중 오류 발생: {e}')
        sys.exit(1)
