"""
Stage 3: 최단 경로 찾기

"""

import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')  # 반드시 plt, patches 등 import 전에 실행
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque
import sys
# map_draw.py의 지도 그리기 함수들을 import
from map_draw import setup_map_figure, draw_structures, add_legend


def find_key_locations(complete_df):
    """집과 반달곰 커피의 위치를 찾습니다."""
    # MyHome 위치 찾기
    home_locations = complete_df[complete_df['struct'] == 'MyHome']
    if home_locations.empty:
        print('❌ 오류: MyHome 위치를 찾을 수 없습니다.')
        sys.exit(1)
    
    home_pos = (home_locations.iloc[0]['x'], home_locations.iloc[0]['y'])
    print(f'🏠 집 위치: {home_pos}')
    
    # BandalgomCoffee 위치들 찾기
    cafe_locations = complete_df[complete_df['struct'] == 'BandalgomCoffee']
    if cafe_locations.empty:
        print('❌ 오류: BandalgomCoffee 위치를 찾을 수 없습니다.')
        sys.exit(1)
    
    cafe_positions = [(row['x'], row['y']) for _, row in cafe_locations.iterrows()]
    print(f'☕ 반달곰 커피 위치들: {cafe_positions}')
    
    # 공사장 위치들 찾기 (지나갈 수 없는 곳)
    construction_sites = set()
    for _, row in complete_df.iterrows():
        if row['ConstructionSite'] == 1:
            construction_sites.add((row['x'], row['y']))
    
    print(f'🚧 공사장 위치: {len(construction_sites)}개')
    
    return home_pos, cafe_positions, construction_sites


def create_grid_map(complete_df):
    """이동 가능한 격자 지도를 생성합니다."""
    # 좌표 범위 계산
    x_min, x_max = complete_df['x'].min(), complete_df['x'].max()
    y_min, y_max = complete_df['y'].min(), complete_df['y'].max()
    
    # 모든 유효한 좌표 집합 생성
    valid_positions = set(zip(complete_df['x'], complete_df['y']))
    
    return valid_positions


def bfs_shortest_path(start_pos, target_positions, valid_positions, construction_sites):
    """BFS 알고리즘을 사용하여 최단 경로를 찾습니다."""
    print(f'🔍 최단 경로 탐색 시작: {start_pos} → {target_positions}')
    # 도착점이 여러 개일 때 각각 BFS로 최단 경로를 구하고, 가장 짧은 경로를 선택
    min_path = None
    min_target = None
    min_length = float('inf')

    for target in target_positions:
        queue = deque([(start_pos, [start_pos])])
        visited = {start_pos}
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while queue:
            current_pos, path = queue.popleft()
            if current_pos == target:
                if len(path) < min_length:
                    min_length = len(path)
                    min_path = path
                    min_target = target
                break
            x, y = current_pos
            for dx, dy in directions:
                next_x, next_y = x + dx, y + dy
                next_pos = (next_x, next_y)
                if (next_pos in valid_positions and 
                    next_pos not in visited and 
                    next_pos not in construction_sites):
                    visited.add(next_pos)
                    new_path = path + [next_pos]
                    queue.append((next_pos, new_path))
        # 다음 도착점으로 계속 탐색

    if min_path is not None:
        print(f'✅ 최단 경로 발견! 길이: {min_length} 단계, 도착점: {min_target}')
        return min_path, min_target
    else:
        print('❌ 경로를 찾을 수 없습니다.')
        return None, None


def save_path_to_csv(path, target_cafe, filename='home_to_cafe.csv'):
    """경로를 CSV 파일로 저장합니다."""
    try:
        # 경로 데이터를 DataFrame으로 변환
        path_data = []
        for i, (x, y) in enumerate(path):
            step_type = 'Start' if i == 0 else 'End' if i == len(path) - 1 else 'Path'
            path_data.append({
                'step': i + 1,
                'x': x,
                'y': y,
                'type': step_type
            })
        
        path_df = pd.DataFrame(path_data)
        path_df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f'경로가 {filename} 파일로 저장되었습니다.')
        print(f'총 {len(path)}단계, 목표 카페: {target_cafe}')
        
        return path_df
        
    except Exception as e:
        print(f'CSV 저장 중 오류 발생: {e}')
        sys.exit(1)


def visualize_path_on_map(complete_df, path, target_cafe, construction_sites, filename='map_final.png'):
    """경로를 지도에 빨간색 선으로 표시하고 저장합니다."""
    try:
        print('🎨 최종 지도 시각화 시작...')
        
        # map_draw.py의 setup_map_figure 함수 사용
        fig, ax, coord_range = setup_map_figure(complete_df)
        
        # map_draw.py의 draw_structures 함수 사용
        structure_counts = draw_structures(ax, complete_df)
        
        # 경로를 빨간색 선으로 그리기
        if path and len(path) > 1:
            # 격자 범위 구하기
            x_min, x_max = complete_df['x'].min(), complete_df['x'].max()
            y_min, y_max = complete_df['y'].min(), complete_df['y'].max()

            # 경로 좌표 추출
            path_x = [pos[0] for pos in path]
            path_y = [pos[1] for pos in path]

            # 경로가 격자 바깥으로 나갈 경우, 바깥 좌표도 그대로 그림
            ax.plot(path_x, path_y, color='red', linewidth=6, alpha=0.8,
                   marker='o', markersize=4, markerfacecolor='red',
                   markeredgecolor='darkred', label=f'Shortest Path ({len(path)} steps)')

            # 시작점과 끝점 강조 표시 (바깥 좌표도 허용)
            start_x, start_y = path[0]
            end_x, end_y = path[-1]

            ax.plot(start_x, start_y, 'ro', markersize=8, markerfacecolor='blue',
                   markeredgecolor='darkblue', label='Start (MyHome)')
            ax.plot(end_x, end_y, 'ro', markersize=8, markerfacecolor='orange',
                   markeredgecolor='darkorange', label=f'Target Cafe {target_cafe}')

            # 축 범위 확장: 경로가 격자 바깥으로 나가면 자동으로 축을 확장
            ax.set_xlim(min(x_min, min(path_x)) - 1, max(x_max, max(path_x)) + 1)
            ax.set_ylim(max(y_max, max(path_y)) + 1, min(y_min, min(path_y)) - 1)
        
        # 범례 추가 (기존 범례에 경로 정보 추가)
        add_legend(ax)
        if path:
            ax.legend(loc='upper left', fontsize=10)
        
        # 제목 수정 (경로 정보 포함)
        ax.set_title(f'Shortest Path from MyHome to BandalgomCoffee\nPath Length: {len(path) if path else 0} steps', 
                    fontsize=16, fontweight='bold')
        
        # 이미지 저장
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f'🎯 최종 지도가 {filename} 파일로 저장되었습니다.')
                
    except Exception as e:
        print(f'❌ 지도 시각화 중 오류 발생: {e}')
        sys.exit(1)


def main():
    """메인 실행 함수"""

    print('=== Stage 3: 최단 경로 찾기 시작 ===')
    
# 1. 데이터 로딩
    print('Stage 1에서 생성한 지도 통합 데이터 로드 중 ...','\n')
    path = 'data/complete_map_data.csv'
    complete_df = pd.read_csv(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f'오류: 지도 통합 데이터 "{path}"을(를) 찾을 수 없습니다. Stage 1을 먼저 실행하여 파일을 생성해 주세요.')

    if complete_df.empty:
        raise ValueError(f'오류: 통합된 지도 데이터 파일 "{path}"이(가) 비어있습니다.')
        
    print(f'전달된 지도 통합 데이터: {len(complete_df)}개')  
    
    # 2. 핵심 위치 찾기
    home_loc, cafes_loc, blocked_loc = find_key_locations(complete_df)
    
    # 3. 격자 지도 생성
    valid_positions = create_grid_map(complete_df)
    
    # 4. 최단 경로 탐색 (BFS 알고리즘)
    path, target_cafe = bfs_shortest_path(home_loc, cafes_loc, valid_positions, blocked_loc)
    
    if path is None:
        print('집에서 반달곰 커피까지의 경로를 찾을 수 없습니다.')
        sys.exit(1)
    
    # 5. 경로를 CSV 파일로 저장
    save_path_to_csv(path, target_cafe)
    
    # 6. 경로가 표시된 지도 시각화 및 저장
    visualize_path_on_map(complete_df, path, target_cafe, blocked_loc)
    
    print('=' * 60)
    print('Stage 3 완료!')

if __name__ == '__main__':
    main()
