"""
통합 테스트: 전체 프로젝트 검증

모든 Stage들의 통합 테스트와 전체 워크플로우를 검증합니다.
"""

import pytest
import pandas as pd
import os
import sys
import subprocess
import tempfile
import shutil
from unittest.mock import patch


# 프로젝트 모듈들을 import하기 위한 경로 설정
sys.path.append('/Users/ittae/development/codyssey-team')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import caffee_map
import map_draw
import map_direct_save


class TestProjectIntegration:
    """프로젝트 전체 통합 테스트 클래스"""
    
    def test_data_files_exist(self):
        """필수 데이터 파일들의 존재 여부 테스트"""
        required_files = [
            'data/area_map.csv',
            'data/area_struct.csv',
            'data/area_category.csv'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        assert len(missing_files) == 0, f"필수 파일들이 없습니다: {missing_files}"
        print("✅ 모든 필수 데이터 파일이 존재합니다.")
    
    def test_data_files_structure(self):
        """데이터 파일들의 구조 검증"""
        if not all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
            pytest.skip("데이터 파일이 없어서 구조 검증을 건너뜁니다.")
        
        # area_map.csv 구조 확인
        area_map_df = pd.read_csv('data/area_map.csv')
        required_map_cols = ['x', 'y', 'ConstructionSite']
        for col in required_map_cols:
            assert col in area_map_df.columns, f"area_map.csv에 '{col}' 컬럼이 없습니다."
        
        # area_struct.csv 구조 확인
        area_struct_df = pd.read_csv('data/area_struct.csv')
        required_struct_cols = ['x', 'y', 'category', 'area']
        for col in required_struct_cols:
            assert col in area_struct_df.columns, f"area_struct.csv에 '{col}' 컬럼이 없습니다."
        
        # area_category.csv 구조 확인
        area_category_df = pd.read_csv('data/area_category.csv')
        
        # 컬럼명 정리 (공백 제거)
        area_category_df.columns = area_category_df.columns.str.strip()
        
        required_category_cols = ['category', 'struct']
        for col in required_category_cols:
            assert col in area_category_df.columns, f"area_category.csv에 '{col}' 컬럼이 없습니다."
        
        print("✅ 모든 데이터 파일의 구조가 올바릅니다.")
    
    def test_stage1_to_stage2_data_flow(self):
        """Stage 1에서 Stage 2로의 데이터 흐름 테스트"""
        if not all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
            pytest.skip("데이터 파일이 없어서 데이터 흐름 테스트를 건너뜁니다.")
        
        # Stage 1: 데이터 분석
        area_map_df, area_struct_df, area_category_df = caffee_map.load_data_files()
        merged_df = caffee_map.convert_struct_ids_to_names(area_struct_df, area_category_df)
        complete_df = caffee_map.merge_all_datasets(area_map_df, merged_df)
        
        # Stage 2: 동일한 데이터 구조 확인
        complete_df = map_draw.load_analyzed_data()
        
        # 데이터 일관성 확인
        assert len(merged_df) == len(complete_df), "Stage 1과 Stage 2의 데이터 크기가 다릅니다."
        
        # 필수 컬럼들이 모두 존재하는지 확인
        required_columns = ['x', 'y', 'struct']
        for col in required_columns:
            assert col in merged_df.columns, f"Stage 1 결과에 '{col}' 컬럼이 없습니다."
            assert col in complete_df.columns, f"Stage 2 데이터에 '{col}' 컬럼이 없습니다."
        
        print("✅ Stage 1에서 Stage 2로의 데이터 흐름이 정상입니다.")
    
    def test_stage2_to_stage3_data_flow(self):
        """Stage 2에서 Stage 3으로의 데이터 흐름 테스트"""
        if not all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
            pytest.skip("데이터 파일이 없어서 데이터 흐름 테스트를 건너뜁니다.")
        
        # Stage 2: 지도 데이터 로드
        stage2_df = map_draw.load_analyzed_data()
        
        # Stage 3: 동일한 데이터 로드
        stage3_df = map_direct_save.load_map_data()
        
        # 데이터 일관성 확인
        assert len(stage2_df) == len(stage3_df), "Stage 2와 Stage 3의 데이터 크기가 다릅니다."
        
        # 핵심 구조물들이 모두 존재하는지 확인
        stage2_structures = set(stage2_df['struct'].unique())
        stage3_structures = set(stage3_df['struct'].unique())
        
        essential_structures = {'MyHome', 'BandalgomCoffee'}
        for struct in essential_structures:
            assert struct in stage2_structures, f"Stage 2에 '{struct}'이 없습니다."
            assert struct in stage3_structures, f"Stage 3에 '{struct}'이 없습니다."
        
        print("✅ Stage 2에서 Stage 3으로의 데이터 흐름이 정상입니다.")
    
    def test_end_to_end_workflow(self):
        """전체 워크플로우 종단간 테스트"""
        if not all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
            pytest.skip("데이터 파일이 없어서 종단간 테스트를 건너뜁니다.")
        
        try:
            # 기존 결과 파일들 백업
            result_files = ['map.png', 'home_to_cafe.csv', 'map_final.png']
            backup_files = {}
            
            for file in result_files:
                if os.path.exists(file):
                    backup_files[file] = file + '.backup'
                    shutil.copy2(file, backup_files[file])
            
            # Stage 1: 데이터 분석 실행
            print("🔄 Stage 1 실행 중...")
            area_map_df, area_struct_df, area_category_df = caffee_map.load_data_files()
            merged_df = caffee_map.convert_struct_ids_to_names(area_struct_df, area_category_df)
            complete_df = caffee_map.merge_all_datasets(area_map_df, merged_df)
            area_1_df = caffee_map.filter_area_1_data(complete_df)
            
            assert not area_1_df.empty, "Stage 1: 구역 1 데이터가 비어있습니다."
            
            # Stage 2: 지도 시각화 실행
            print("🔄 Stage 2 실행 중...")
            map_draw.create_map_visualization()
            
            assert os.path.exists('map.png'), "Stage 2: map.png 파일이 생성되지 않았습니다."
            
            # Stage 3: 최단 경로 찾기 실행
            print("🔄 Stage 3 실행 중...")
            complete_df = map_direct_save.load_map_data()
            home_pos, cafe_positions, construction_sites = map_direct_save.find_key_locations(complete_df)
            valid_positions, _ = map_direct_save.create_grid_map(complete_df)
            
            path, target_cafe = map_direct_save.bfs_shortest_path(
                home_pos, cafe_positions, valid_positions, construction_sites
            )
            
            if path:
                path_df = map_direct_save.save_path_to_csv(path, target_cafe)
                map_direct_save.visualize_path_on_map(complete_df, path, target_cafe, construction_sites)
                
                assert os.path.exists('home_to_cafe.csv'), "Stage 3: home_to_cafe.csv 파일이 생성되지 않았습니다."
                assert os.path.exists('map_final.png'), "Stage 3: map_final.png 파일이 생성되지 않았습니다."
                
                # 경로 데이터 검증
                path_df_loaded = pd.read_csv('home_to_cafe.csv')
                assert len(path_df_loaded) == len(path), "저장된 경로 데이터의 길이가 다릅니다."
                
                print(f"✅ 전체 워크플로우 성공! 경로 길이: {len(path)}단계")
            else:
                print("⚠️ 경로를 찾을 수 없지만 워크플로우는 정상 실행되었습니다.")
            
            # 백업 파일들 복원
            for original, backup in backup_files.items():
                if os.path.exists(backup):
                    shutil.move(backup, original)
            
        except Exception as e:
            # 백업 파일들 복원
            for original, backup in backup_files.items():
                if os.path.exists(backup):
                    shutil.move(backup, original)
            
            pytest.fail(f"종단간 테스트 실패: {e}")
    
    def test_output_file_quality(self):
        """출력 파일들의 품질 검증"""
        if not all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
            pytest.skip("데이터 파일이 없어서 출력 파일 품질 검증을 건너뜁니다.")
        
        # 결과 파일들이 존재하는지 확인
        expected_files = ['map.png', 'home_to_cafe.csv', 'map_final.png']
        missing_files = [f for f in expected_files if not os.path.exists(f)]
        
        if missing_files:
            # 파일들이 없다면 생성
            print("🔄 결과 파일들을 생성하는 중...")
            map_draw.create_map_visualization()
            map_direct_save.main()
        
        # 파일 크기 검증
        for file in expected_files:
            if os.path.exists(file):
                file_size = os.path.getsize(file)
                assert file_size > 0, f"{file} 파일이 비어있습니다."
                
                if file.endswith('.png'):
                    assert file_size > 1000, f"{file} 이미지 파일이 너무 작습니다. ({file_size} bytes)"
                elif file.endswith('.csv'):
                    # CSV 파일 내용 검증
                    df = pd.read_csv(file)
                    assert not df.empty, f"{file} CSV 파일이 비어있습니다."
        
        print("✅ 모든 출력 파일들의 품질이 검증되었습니다.")
    
    def test_project_structure_compliance(self):
        """프로젝트 구조 준수 검증"""
        # 필수 Python 파일들 확인
        required_py_files = [
            'caffee_map.py',
            'map_draw.py', 
            'map_direct_save.py'
        ]
        
        for file in required_py_files:
            assert os.path.exists(file), f"필수 Python 파일 '{file}'이 없습니다."
        
        # 데이터 디렉토리 구조 확인
        assert os.path.isdir('data'), "data 디렉토리가 없습니다."
        
        # 테스트 파일들 확인
        test_files = [
            'test/test_caffee_map.py',
            'test/test_map_draw.py',
            'test/test_map_direct_save.py'
        ]
        
        for file in test_files:
            assert os.path.exists(file), f"테스트 파일 '{file}'이 없습니다."
        
        print("✅ 프로젝트 구조가 요구사항에 맞습니다.")
    
    def test_korean_coding_style(self):
        """한국어 코딩 스타일 가이드 준수 검증"""
        py_files = ['caffee_map.py', 'map_draw.py', 'map_direct_save.py']
        
        for file in py_files:
            if os.path.exists(file):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 한국어 주석이 있는지 확인 (기본적인 검증)
                assert '"""' in content, f"{file}에 docstring이 없습니다."
                
                # 함수 정의가 있는지 확인
                assert 'def ' in content, f"{file}에 함수가 정의되지 않았습니다."
                
                print(f"✅ {file} 스타일 검증 완료")


def test_performance_benchmark():
    """성능 벤치마크 테스트"""
    if not all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
        pytest.skip("데이터 파일이 없어서 성능 테스트를 건너뜁니다.")
    
    import time
    
    # Stage 1 성능 측정
    start_time = time.time()
    area_map_df, area_struct_df, area_category_df = caffee_map.load_data_files()
    merged_df = caffee_map.convert_struct_ids_to_names(area_struct_df, area_category_df)
    complete_df = caffee_map.merge_all_datasets(area_map_df, merged_df)
    stage1_time = time.time() - start_time
    
    # Stage 3 경로 찾기 성능 측정
    start_time = time.time()
    complete_df = map_direct_save.load_map_data()
    home_pos, cafe_positions, construction_sites = map_direct_save.find_key_locations(complete_df)
    valid_positions, _ = map_direct_save.create_grid_map(complete_df)
    path, target_cafe = map_direct_save.bfs_shortest_path(home_pos, cafe_positions, valid_positions, construction_sites)
    stage3_time = time.time() - start_time
    
    print(f"📊 성능 벤치마크:")
    print(f"   - Stage 1 (데이터 분석): {stage1_time:.3f}초")
    print(f"   - Stage 3 (경로 찾기): {stage3_time:.3f}초")
    
    # 성능 임계값 확인 (합리적인 시간 내에 완료되는지)
    assert stage1_time < 5.0, f"Stage 1이 너무 오래 걸립니다: {stage1_time:.3f}초"
    assert stage3_time < 30.0, f"Stage 3이 너무 오래 걸립니다: {stage3_time:.3f}초"
    
    print("✅ 성능 벤치마크 통과")


if __name__ == '__main__':
    # pytest 실행
    pytest.main([__file__, '-v'])
