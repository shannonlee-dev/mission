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
    valid_positions = set(zip(complete_df['x'], complete_df['y']))
    
    # MyHome 위치 찾기
    home_locations = complete_df[complete_df['struct'] == 'MyHome']
    if home_locations.empty:
        print('오류: MyHome 위치를 찾을 수 없습니다.')
        sys.exit(1)
    
    home_pos = (home_locations.iloc[0]['x'], home_locations.iloc[0]['y'])
    
    # BandalgomCoffee 위치들 찾기
    cafe_locations = complete_df[complete_df['struct'] == 'BandalgomCoffee']
    if cafe_locations.empty:
        print('오류: BandalgomCoffee 위치를 찾을 수 없습니다.')
        sys.exit(1)
    
    cafe_positions = [(row['x'], row['y']) for _, row in cafe_locations.iterrows()]
    
    # 공사장 위치들 찾기 (지나갈 수 없는 곳)
    construction_sites = set()
    for _, row in complete_df.iterrows():
        if row['ConstructionSite'] == 1:
            construction_sites.add((row['x'], row['y']))
    
    return home_pos, cafe_positions, construction_sites, valid_positions


def bfs_shortest_path(start_pos, target_positions, valid_positions, construction_sites):
    """
    BFS 알고리즘

    Arguments:
        start_pos: 시작 좌표 (x, y)
        target_positions: 도착 후보 좌표 리스트
        valid_positions: 이동 가능한 좌표 집합
        construction_sites: 공사장 좌표 집합 (통과 불가)

    Returns:
        (path, target)
          - path: 시작점부터 목표까지의 좌표 리스트
          - target: 실제 도달한 목표 좌표
    """
    targets = set(target_positions)
    queue = deque([start_pos])
    visited = {start_pos}
    parent = {}
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # BFS 탐색: 가장 먼저 만나는 목표 지점을 반환
    found_target = None
    while queue:
        current = queue.popleft()
        if current in targets:
            found_target = current
            break

        x, y = current
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if (neighbor in valid_positions
                    and neighbor not in visited
                    and neighbor not in construction_sites):
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    # 경로 복원
    if found_target is not None:
        path = []
        node = found_target
        while node != start_pos:
            path.append(node)
            node = parent[node]
        path.append(start_pos)
        path.reverse()
        print(f'최단 경로 발견! 길이: {len(path)} 단계')
        return path, found_target

    print('경로를 찾을 수 없습니다.')
    return None, None


def save_path(path, goal, filename='home_to_cafe.csv'):
    """경로를 CSV 파일로 저장합니다."""

    try:
        data = []

        for i,(x,y) in enumerate(path):
            if i == 0:
                t = 'Start'
            elif (i == len(path) - 1):
                t = 'End'
            else:
                t = 'Path'

            data.append({'step':i+1,'x':x,'y':y,'type':t})


        df = pd.DataFrame(data)

        df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f'경로가 {filename} 파일로 저장되었습니다.')

        return df
        
    except Exception as e:
        print(f'CSV 저장 중 오류 발생: {e}')
        sys.exit(1)


def visualize_path_on_map(complete_df, path, target_cafe,filename='map_final.png'):
    """경로를 지도에 빨간색 선으로 표시하고 저장합니다."""
    try:
        print('최종 지도 시각화 시작...')
        
        # map_draw.py의 setup_map_figure 함수 사용
        _, ax, _ = setup_map_figure(complete_df)
        
        # map_draw.py의 draw_structures 함수 사용
        draw_structures(ax, complete_df)
        
        # 경로를 빨간색 선으로 그리기
        if path and len(path) > 1:

            # 경로 좌표 추출
            path_x = [pos[0] for pos in path]
            path_y = [pos[1] for pos in path]

       
            ax.plot(path_x, path_y, color='red', linewidth=6, alpha=0.8,
                   marker='o', markersize=10, markerfacecolor='red',
                   markeredgecolor='darkred', label=f'Shortest Path ({len(path)} steps)')
            
            # 시작점과 끝점 강조 표시 
            start_x, start_y = path[0]
            end_x, end_y = path[-1]

            ax.plot(start_x, start_y, 'ro', markersize=8, markerfacecolor='blue',
                   markeredgecolor='darkblue', label='Start (MyHome)')
            ax.plot(end_x, end_y, 'ro', markersize=8, markerfacecolor='orange',
                   markeredgecolor='darkorange', label=f'Goal {target_cafe}')

        
        # 범례 추가 (기존 범례에 경로 정보 추가)
        add_legend(ax)
        ax.legend(loc='upper left', fontsize=10)
        
        # 제목 수정 (경로 정보 포함)
        ax.set_title(f'Shortest Path from MyHome to BandalgomCoffee(A*)\nPath Length: {len(path) if path else 0} steps', 
                    fontsize=16, fontweight='bold')
        
        # 이미지 저장
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f'최종 지도가 {filename} 파일로 저장되었습니다.')
                
    except Exception as e:
        print(f'지도 시각화 중 오류 발생: {e}')
        sys.exit(1)


def main():
    """메인 실행 함수"""

    print('=== Stage 3: 최단 경로 찾기 시작 ===')
    
# 1. 데이터 로딩
    print('Stage 1에서 생성한 지도 통합 데이터 로드 중 ...','\n')
    path = 'data/complete_map_data.csv'
    if not os.path.exists(path):
        raise FileNotFoundError(f'오류: 지도 통합 데이터 "{path}"을(를) 찾을 수 없습니다. Stage 1을 먼저 실행하여 파일을 생성해 주세요.')

    complete_df = pd.read_csv(path)

    if complete_df.empty:
        raise ValueError(f'오류: 통합된 지도 데이터 파일 "{path}"이(가) 비어있습니다.')
        
    print(f'로드된 지도 통합 데이터: {len(complete_df)}개')  
    
    # 2. 핵심 위치 찾기
    home_loc, cafes_loc, blocked_loc,valid_positions = find_key_locations(complete_df)
    
    # 3. 최단 경로 탐색 (BFS 알고리즘)
    path, target_cafe = bfs_shortest_path(home_loc, cafes_loc, valid_positions, blocked_loc)
    
    if path is None:
        print('집에서 반달곰 커피까지의 경로를 찾을 수 없습니다.')
        sys.exit(1)
    
    # 4. 경로를 CSV 파일로 저장
    save_path(path, target_cafe)
    
    # 5. 경로가 표시된 지도 시각화 및 저장
    visualize_path_on_map(complete_df, path, target_cafe)
    
    print('=' * 60)
    print('Stage 3 완료!')

if __name__ == '__main__':
    main()
