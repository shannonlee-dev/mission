"""
테스트 케이스: Stage 3 - 최단 경로 찾기

map_direct_save.py의 기능들을 검증하는 테스트 케이스들을 포함합니다.
"""

import pytest
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import tempfile
import shutil
from unittest.mock import patch
from collections import deque


# map_direct_save 모듈을 import하기 위한 경로 설정
sys.path.append('/Users/ittae/development/codyssey-team')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import map_direct_save


class TestMapDirectSave:
    """Stage 3 최단 경로 찾기 테스트 클래스"""
    
    @pytest.fixture
    def setup_test_data(self):
        """테스트용 임시 데이터 파일들을 생성합니다."""
        # 임시 디렉토리 생성
        test_dir = tempfile.mkdtemp()
        data_dir = os.path.join(test_dir, 'data')
        os.makedirs(data_dir)
        
        # 테스트용 간단한 그리드 생성 (5x5)
        area_map_data = {
            'x': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
            'y': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
            'ConstructionSite': [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
        area_map_df = pd.DataFrame(area_map_data)
        area_map_df.to_csv(os.path.join(data_dir, 'area_map.csv'), index=False)
        
        area_struct_data = {
            'x': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
            'y': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
            'category': [1, 2, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4],  # 1: MyHome, 2: Construction, 3: Coffee, 4: Others
            'area': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        }
        area_struct_df = pd.DataFrame(area_struct_data)
        area_struct_df.to_csv(os.path.join(data_dir, 'area_struct.csv'), index=False)
        
        area_category_data = {
            'category': [1, 2, 3, 4],
            'struct': ['MyHome', 'ConstructionSite', 'BandalgomCoffee', 'Apartment']
        }
        area_category_df = pd.DataFrame(area_category_data)
        area_category_df.to_csv(os.path.join(data_dir, 'area_category.csv'), index=False)
        
        # 현재 작업 디렉토리 변경
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        yield test_dir
        
        # 정리
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)
    
    def test_load_map_data(self, setup_test_data):
        """지도 데이터 로드 테스트"""
        complete_df = map_direct_save.load_map_data()
        
        # 기본 검증
        assert isinstance(complete_df, pd.DataFrame)
        assert not complete_df.empty
        
        # 필수 컬럼 존재 확인
        required_columns = ['x', 'y', 'ConstructionSite', 'struct']
        for col in required_columns:
            assert col in complete_df.columns, f"컬럼 '{col}'이 없습니다."
    
    def test_find_key_locations(self, setup_test_data):
        """핵심 위치 찾기 테스트"""
        complete_df = map_direct_save.load_map_data()
        home_pos, cafe_positions, construction_sites = map_direct_save.find_key_locations(complete_df)
        
        # MyHome 위치 확인
        assert isinstance(home_pos, tuple)
        assert len(home_pos) == 2
        
        # 커피샵 위치들 확인
        assert isinstance(cafe_positions, list)
        assert len(cafe_positions) > 0
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in cafe_positions)
        
        # 공사장 위치들 확인
        assert isinstance(construction_sites, set)
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in construction_sites)
    
    def test_create_grid_map(self, setup_test_data):
        """격자 지도 생성 테스트"""
        complete_df = map_direct_save.load_map_data()
        valid_positions, grid_bounds = map_direct_save.create_grid_map(complete_df)
        
        # 유효한 위치 집합 확인
        assert isinstance(valid_positions, set)
        assert len(valid_positions) > 0
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in valid_positions)
        
        # 격자 범위 확인
        x_min, x_max, y_min, y_max = grid_bounds
        assert x_min <= x_max
        assert y_min <= y_max
    
    def test_bfs_shortest_path(self, setup_test_data):
        """BFS 최단 경로 찾기 테스트"""
        complete_df = map_direct_save.load_map_data()
        home_pos, cafe_positions, construction_sites = map_direct_save.find_key_locations(complete_df)
        valid_positions, _ = map_direct_save.create_grid_map(complete_df)
        
        # BFS 알고리즘 실행
        path, target_cafe = map_direct_save.bfs_shortest_path(
            home_pos, cafe_positions, valid_positions, construction_sites
        )
        
        if path is not None:
            # 경로 검증
            assert isinstance(path, list)
            assert len(path) >= 2  # 최소한 시작점과 끝점
            assert path[0] == home_pos  # 시작점 확인
            assert path[-1] in cafe_positions  # 끝점이 커피샵 중 하나
            assert target_cafe == path[-1]  # 목표 카페가 경로의 마지막 점
            
            # 경로의 연결성 확인 (인접한 점들이 1칸씩 떨어져 있는지)
            for i in range(len(path) - 1):
                current = path[i]
                next_pos = path[i + 1]
                distance = abs(current[0] - next_pos[0]) + abs(current[1] - next_pos[1])
                assert distance == 1, f"경로가 연결되지 않음: {current} -> {next_pos}"
            
            # 경로가 공사장을 지나지 않는지 확인
            for pos in path:
                assert pos not in construction_sites, f"경로가 공사장을 지남: {pos}"
        else:
            # 경로를 찾을 수 없는 경우도 유효한 결과
            assert target_cafe is None
    
    def test_save_path_to_csv(self, setup_test_data):
        """경로 CSV 저장 테스트"""
        # 테스트용 더미 경로 생성
        test_path = [(1, 1), (2, 1), (3, 1), (3, 2)]
        test_target = (3, 2)
        test_filename = 'test_path.csv'
        
        # CSV 저장
        path_df = map_direct_save.save_path_to_csv(test_path, test_target, test_filename)
        
        # 결과 검증
        assert isinstance(path_df, pd.DataFrame)
        assert os.path.exists(test_filename)
        
        # CSV 파일 내용 검증
        loaded_df = pd.read_csv(test_filename)
        assert len(loaded_df) == len(test_path)
        assert 'step' in loaded_df.columns
        assert 'x' in loaded_df.columns
        assert 'y' in loaded_df.columns
        assert 'type' in loaded_df.columns
        
        # 시작점과 끝점 타입 확인
        assert loaded_df.iloc[0]['type'] == 'Start'
        assert loaded_df.iloc[-1]['type'] == 'End'
        
        # 파일 정리
        if os.path.exists(test_filename):
            os.remove(test_filename)
    
    @patch('matplotlib.pyplot.savefig')
    def test_visualize_path_on_map(self, mock_savefig, setup_test_data):
        """경로 시각화 테스트"""
        complete_df = map_direct_save.load_map_data()
        
        # 테스트용 더미 경로
        test_path = [(1, 1), (2, 1), (3, 1)]
        test_target = (3, 1)
        test_construction_sites = {(1, 2), (2, 2)}
        test_filename = 'test_map.png'
        
        # 시각화 함수 실행
        map_direct_save.visualize_path_on_map(
            complete_df, test_path, test_target, test_construction_sites, test_filename
        )
        
        # savefig가 호출되었는지 확인
        mock_savefig.assert_called_once_with(test_filename, dpi=300, bbox_inches='tight')


def test_pathfinding_algorithm_correctness():
    """경로 찾기 알고리즘 정확성 테스트"""
    # 간단한 격자에서 최단 경로 테스트
    start = (1, 1)
    targets = [(3, 3)]
    valid_positions = {(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)}
    construction_sites = {(2, 2)}  # 중간에 장애물
    
    # BFS 실행
    path, target = map_direct_save.bfs_shortest_path(start, targets, valid_positions, construction_sites)
    
    if path:
        # 경로 길이 확인 (장애물 때문에 우회해야 함)
        expected_min_length = 5  # 최소 5단계 (우회 경로)
        assert len(path) >= expected_min_length
        
        # 시작점과 끝점 확인
        assert path[0] == start
        assert path[-1] == targets[0]
        
        print(f"✅ 경로 찾기 알고리즘 테스트 통과: {len(path)}단계 경로")


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
        try:
            # 기존 결과 파일들 백업 (있다면)
            backup_files = {}
            result_files = ['home_to_cafe.csv', 'map_final.png']
            
            for file in result_files:
                if os.path.exists(file):
                    backup_files[file] = file + '.backup'
                    shutil.copy2(file, backup_files[file])
            
            # 메인 함수 실행
            map_direct_save.main()
            
            # 결과 파일들이 생성되었는지 확인
            for file in result_files:
                assert os.path.exists(file), f"{file} 파일이 생성되지 않았습니다."
            
            # CSV 파일 내용 검증
            if os.path.exists('home_to_cafe.csv'):
                df = pd.read_csv('home_to_cafe.csv')
                assert not df.empty
                assert all(col in df.columns for col in ['step', 'x', 'y', 'type'])
                assert df.iloc[0]['type'] == 'Start'
                assert df.iloc[-1]['type'] == 'End'
            
            print("✅ Stage 3 통합 테스트 통과")
            
            # 백업 파일들 복원
            for original, backup in backup_files.items():
                if os.path.exists(backup):
                    shutil.move(backup, original)
            
        except Exception as e:
            # 백업 파일들 복원
            for original, backup in backup_files.items():
                if os.path.exists(backup):
                    shutil.move(backup, original)
            
            pytest.fail(f"Stage 3 통합 테스트 실패: {e}")
    else:
        pytest.skip("실제 데이터 파일이 없어서 통합 테스트를 건너뜁니다.")


def test_path_validation_with_real_data():
    """실제 데이터로 경로 검증 테스트"""
    if all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
        try:
            complete_df = map_direct_save.load_map_data()
            home_pos, cafe_positions, construction_sites = map_direct_save.find_key_locations(complete_df)
            valid_positions, _ = map_direct_save.create_grid_map(complete_df)
            
            path, target_cafe = map_direct_save.bfs_shortest_path(
                home_pos, cafe_positions, valid_positions, construction_sites
            )
            
            if path:
                print(f"📍 경로 분석:")
                print(f"   - 시작점: {home_pos}")
                print(f"   - 목표점: {target_cafe}")
                print(f"   - 경로 길이: {len(path)}단계")
                print(f"   - 공사장 개수: {len(construction_sites)}개")
                
                # 경로 유효성 검증
                assert path[0] == home_pos
                assert path[-1] == target_cafe
                
                # 모든 경로 점이 유효한 위치인지 확인
                for pos in path:
                    assert pos in valid_positions
                    assert pos not in construction_sites
                
                print("✅ 실제 데이터 경로 검증 통과")
            else:
                print("⚠️ 경로를 찾을 수 없습니다.")
            
        except Exception as e:
            pytest.fail(f"실제 데이터 경로 검증 실패: {e}")
    else:
        pytest.skip("실제 데이터 파일이 없어서 경로 검증을 건너뜁니다.")


if __name__ == '__main__':
    # pytest 실행
    pytest.main([__file__, '-v'])
