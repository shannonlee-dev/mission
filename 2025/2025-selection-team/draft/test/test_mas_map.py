"""
테스트 케이스: Stage 1 - 데이터 수집 및 분석

mas_map.py의 기능들을 검증하는 테스트 케이스들을 포함합니다.
"""

import pytest
import pandas as pd
import os
import sys
from unittest.mock import patch, mock_open
import tempfile
import shutil


# mas_map 모듈을 import하기 위한 경로 설정
sys.path.append('/Users/ittae/development/codyssey-team')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import mas_map


class TestCaffeeMap:
    """Stage 1 데이터 분석 테스트 클래스"""
    
    def test_load_data_files_success(self):
        """데이터 파일 로드 성공 테스트 - 실제 데이터 파일 사용"""
        # 상위 디렉토리의 data 폴더 확인
        data_files = ['../data/area_map.csv', '../data/area_struct.csv', '../data/area_category.csv']
        if not all(os.path.exists(f) for f in data_files):
            pytest.skip("실제 데이터 파일이 없어서 테스트를 건너뜁니다.")
        
        # 현재 작업 디렉토리를 상위로 변경
        original_cwd = os.getcwd()
        try:
            if os.path.basename(os.getcwd()) == 'test':
                os.chdir('..')
            
            area_map_df, area_struct_df, area_category_df = mas_map.load_data_files()
        finally:
            os.chdir(original_cwd)
        
        # 데이터 형태 검증
        assert isinstance(area_map_df, pd.DataFrame)
        assert isinstance(area_struct_df, pd.DataFrame)
        assert isinstance(area_category_df, pd.DataFrame)
        
        # 필수 컬럼 존재 확인
        assert 'x' in area_map_df.columns
        assert 'y' in area_map_df.columns
        assert 'ConstructionSite' in area_map_df.columns
        
        assert 'x' in area_struct_df.columns
        assert 'y' in area_struct_df.columns
        assert 'category' in area_struct_df.columns
        assert 'area' in area_struct_df.columns
        
        # 카테고리 컬럼명 정리 후 확인
        area_category_df.columns = area_category_df.columns.str.strip()
        assert 'category' in area_category_df.columns
        assert 'struct' in area_category_df.columns
    
    def test_load_data_files_missing_file(self):
        """파일이 없을 때 오류 처리 테스트"""
        # 현재 디렉토리를 임시로 변경해서 파일이 없는 상황 시뮬레이션
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # 파일이 없는 상태에서 실행하면 sys.exit(1)이 호출되어야 함
                with pytest.raises(SystemExit) as excinfo:
                    mas_map.load_data_files()
                assert excinfo.value.code == 1
            finally:
                os.chdir(original_cwd)
    
    def test_clean_category_data(self):
        """카테고리 데이터 정리 기능 테스트"""
        # 테스트용 데이터 (공백이 있는 데이터)
        test_data = pd.DataFrame({
            'category': [' 1 ', '2', ' 3'],
            'struct': [' MyHome ', 'Apartment', 'BandalgomCoffee ']
        })
        
        cleaned_data = mas_map.clean_category_data(test_data)
        
        # 공백 제거 확인
        assert cleaned_data['struct'].iloc[0] == 'MyHome'
        assert cleaned_data['struct'].iloc[2] == 'BandalgomCoffee'
    
    def test_analyze_data(self):
        """데이터 분석 기능 테스트 - 실제 데이터 파일 사용"""
        if not all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
            pytest.skip("실제 데이터 파일이 없어서 테스트를 건너뜁니다.")
        
        area_map_df, area_struct_df, area_category_df = mas_map.load_data_files()
        
        # convert_struct_ids_to_names 함수 테스트
        merged_df = mas_map.convert_struct_ids_to_names(area_struct_df, area_category_df)
        
        # 병합된 데이터 검증
        assert isinstance(merged_df, pd.DataFrame)
        assert 'struct' in merged_df.columns
        
        # 구조물 이름이 올바르게 매핑되었는지 확인
        struct_names = merged_df['struct'].unique()
        expected_names = ['MyHome', 'BandalgomCoffee']
        for name in expected_names:
            assert name in struct_names, f"Expected structure '{name}' not found in data"
    
    def test_filter_area_1_data(self):
        """구역 1 데이터 필터링 테스트 - 실제 데이터 파일 사용"""
        if not all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
            pytest.skip("실제 데이터 파일이 없어서 테스트를 건너뜁니다.")
        
        area_map_df, area_struct_df, area_category_df = mas_map.load_data_files()
        merged_df = mas_map.convert_struct_ids_to_names(area_struct_df, area_category_df)
        complete_df = mas_map.merge_all_datasets(area_map_df, merged_df)
        
        area_1_df = mas_map.filter_area_1_data(complete_df)
        
        # 모든 데이터가 구역 1인지 확인
        assert all(area_1_df['area'] == 1)
        
        # DataFrame이 비어있지 않은지 확인
        assert not area_1_df.empty


def test_main_integration():
    """전체 실행 통합 테스트"""
    # 실제 데이터 파일이 있는지 확인
    required_files = [
        'data/area_map.csv',
        'data/area_struct.csv', 
        'data/area_category.csv'
    ]
    
    files_exist = all(os.path.exists(f) for f in required_files)
    
    if files_exist:
        # 실제 데이터로 테스트
        try:
            area_map_df, area_struct_df, area_category_df = mas_map.load_data_files()
            merged_df = mas_map.convert_struct_ids_to_names(area_struct_df, area_category_df)
            complete_df = mas_map.merge_all_datasets(area_map_df, merged_df)
            area_1_df = mas_map.filter_area_1_data(complete_df)
            
            # 기본적인 데이터 검증
            assert not area_1_df.empty
            assert 'struct' in area_1_df.columns
            
            print("✅ Stage 1 통합 테스트 통과")
            
        except Exception as e:
            pytest.fail(f"Stage 1 통합 테스트 실패: {e}")
    else:
        pytest.skip("실제 데이터 파일이 없어서 통합 테스트를 건너뜁니다.")


if __name__ == '__main__':
    # pytest 실행
    pytest.main([__file__, '-v'])
