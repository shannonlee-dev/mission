"""
테스트 케이스: Stage 2 - 지도 시각화

map_draw.py의 기능들을 검증하는 테스트 케이스들을 포함합니다.
"""

import pytest
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import tempfile
import shutil
from unittest.mock import patch


# map_draw 모듈을 import하기 위한 경로 설정
sys.path.append('/Users/ittae/development/codyssey-team')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import map_draw


class TestMapDraw:
    """Stage 2 지도 시각화 테스트 클래스"""
    
    @pytest.fixture
    def setup_test_data(self):
        """테스트용 임시 데이터 파일들을 생성합니다."""
        # 임시 디렉토리 생성
        test_dir = tempfile.mkdtemp()
        data_dir = os.path.join(test_dir, 'data')
        os.makedirs(data_dir)
        
        # 테스트용 데이터 생성
        area_map_data = {
            'x': [1, 2, 3, 4, 5],
            'y': [1, 2, 3, 4, 5],
            'ConstructionSite': [0, 1, 0, 0, 1]
        }
        area_map_df = pd.DataFrame(area_map_data)
        area_map_df.to_csv(os.path.join(data_dir, 'area_map.csv'), index=False)
        
        area_struct_data = {
            'x': [1, 2, 3, 4, 5],
            'y': [1, 2, 3, 4, 5],
            'category': [1, 2, 3, 4, 2],
            'area': [1, 1, 1, 1, 1]
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
    
    def test_load_analyzed_data(self, setup_test_data):
        """분석된 데이터 로드 테스트"""
        complete_df = map_draw.load_analyzed_data()
        
        # 기본 검증
        assert isinstance(complete_df, pd.DataFrame)
        assert not complete_df.empty
        
        # 필수 컬럼 존재 확인
        required_columns = ['x', 'y', 'ConstructionSite', 'struct']
        for col in required_columns:
            assert col in complete_df.columns, f"컬럼 '{col}'이 없습니다."
    
    def test_setup_map_figure(self, setup_test_data):
        """지도 figure 설정 테스트"""
        complete_df = map_draw.load_analyzed_data()
        fig, ax, bounds = map_draw.setup_map_figure(complete_df)
        
        # figure와 axis 객체 확인
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        
        # 좌표 범위 확인
        x_min, x_max, y_min, y_max = bounds
        assert x_min <= x_max
        assert y_min <= y_max
        
        # 축 설정 확인
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        assert xlim[0] < xlim[1]
        assert ylim[0] > ylim[1]  # y축이 뒤집어져 있는지 확인
        
        # 정리
        plt.close(fig)
    
    def test_draw_structures_counts(self, setup_test_data):
        """구조물 그리기 및 개수 확인 테스트"""
        complete_df = map_draw.load_analyzed_data()
        fig, ax, bounds = map_draw.setup_map_figure(complete_df)
        
        # draw_structures 함수 실행
        map_draw.draw_structures(ax, complete_df)
        
        # 그려진 patches 개수 확인
        patches_count = len(ax.patches)
        assert patches_count > 0, "구조물이 그려지지 않았습니다."
        
        # 정리
        plt.close(fig)
    
    def test_create_map_visualization(self, setup_test_data):
        """지도 시각화 생성 테스트"""
        # 기존 map.png 백업
        backup_file = None
        if os.path.exists('map.png'):
            backup_file = 'map_backup.png'
            shutil.copy2('map.png', backup_file)
        
        try:
            # create_map_visualization 함수 실행
            map_draw.create_map_visualization()
            
            # map.png 파일이 생성되었는지 확인
            assert os.path.exists('map.png'), "map.png 파일이 생성되지 않았습니다."
            
            # 파일이 비어있지 않은지 확인
            assert os.path.getsize('map.png') > 0, "map.png 파일이 비어있습니다."
            
        finally:
            # 백업 파일 복원
            if backup_file and os.path.exists(backup_file):
                shutil.move(backup_file, 'map.png')


def test_map_visualization_integration():
    """지도 시각화 통합 테스트"""
    # 실제 데이터 파일이 있는지 확인
    required_files = [
        'data/area_map.csv',
        'data/area_struct.csv', 
        'data/area_category.csv'
    ]
    
    files_exist = all(os.path.exists(f) for f in required_files)
    
    if files_exist:
        try:
            # 실제 지도 생성 테스트
            map_draw.create_map_visualization()
            
            # map.png 파일이 생성되었는지 확인
            assert os.path.exists('map.png'), "map.png 파일이 생성되지 않았습니다."
            
            print("✅ Stage 2 통합 테스트 통과")
            
        except Exception as e:
            pytest.fail(f"Stage 2 통합 테스트 실패: {e}")
    else:
        pytest.skip("실제 데이터 파일이 없어서 통합 테스트를 건너뜁니다.")


def test_structure_rendering_validation():
    """구조물 렌더링 검증 테스트"""
    # 실제 데이터로 테스트
    if all(os.path.exists(f) for f in ['data/area_map.csv', 'data/area_struct.csv', 'data/area_category.csv']):
        try:
            complete_df = map_draw.load_analyzed_data()
            
            # 각 구조물 타입별 개수 확인
            structure_types = complete_df['struct'].value_counts()
            construction_sites = (complete_df['ConstructionSite'] == 1).sum()
            
            print(f"📊 구조물 분포:")
            for struct_type, count in structure_types.items():
                print(f"   - {struct_type}: {count}개")
            print(f"   - ConstructionSite: {construction_sites}개")
            
            # 기본적인 구조물들이 존재하는지 확인
            expected_structures = ['MyHome', 'BandalgomCoffee']
            for struct in expected_structures:
                assert struct in structure_types.index, f"{struct}이 데이터에 없습니다."
            
            print("✅ 구조물 렌더링 검증 통과")
            
        except Exception as e:
            pytest.fail(f"구조물 렌더링 검증 실패: {e}")
    else:
        pytest.skip("실제 데이터 파일이 없어서 구조물 렌더링 검증을 건너뜁니다.")


if __name__ == '__main__':
    # pytest 실행
    pytest.main([__file__, '-v'])
