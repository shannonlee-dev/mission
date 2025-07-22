"""
Stage 3: 최단 경로 찾기 (A* 알고리즘 적용)
"""

import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import deque
import heapq
import sys

# map_draw.py의 지도 그리기 함수들을 import
from map_draw import setup_map_figure, draw_structures, add_legend

def find_key_locations(df):
    """구조물들의 위치를 찾습니다."""

    valid_coord = set(zip(df['x'], df['y']))


    home_loc = df[df['struct'] == 'MyHome']
    if home_loc.empty:
        print('MyHome 위치 없음')
        sys.exit(1)

    home_coord = (home_loc.iloc[0]['x'], home_loc.iloc[0]['y'])

    cafes_loc = df[df['struct'] == 'BandalgomCoffee']
    if cafes_loc.empty:
        print('BandalgomCoffee 위치 없음')
        sys.exit(1)

    cafe_coord = [(row['x'], row['y']) for _,row in cafes_loc.iterrows()]

    construction_coord = { (r['x'],r['y']) for _,r in df[df['ConstructionSite']==1].iterrows() }
    
    print(f'\n지도 위 구조물 파악 계산 완료')

    return home_coord, cafe_coord, construction_coord, valid_coord

def compute_heuristic_map(targets, valid, blocked):
    # 목표 지점들로부터 역방향 BFS를 통해 휴리스틱 맵을 계산합니다.

    hmap = { pos: float('inf') for pos in valid if pos not in blocked }
    # 임시로 inf로 초기화

    dq = deque()

    for t in targets:
        hmap[t] = 0
        dq.append(t)
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    while dq:
        cur = dq.popleft()
        for dx,dy in dirs: #dx,dy 는 변화량
            nb = (cur[0]+dx, cur[1]+dy)
            if nb in hmap and hmap[nb] == float('inf'):
                hmap[nb] = hmap[cur] + 1
                dq.append(nb)
    return hmap


def astar_algorithm(start, targets, blocked, valid):
    print(f'역방향 BFS로 휴리스틱 계산 시작')
    hmap = compute_heuristic_map(targets, valid, blocked)
    open_set = []
    heapq.heappush(open_set, (hmap[start], 0, start))
    came_from = {} # 경로 복원을 위한 딕셔너리
    gscore = { start: 0 } #도착까지 최단거리 딕셔너리
    visited = set()
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    goal = None

    while open_set:
        f, g, cur = heapq.heappop(open_set)
        if cur in visited: continue
        visited.add(cur)
        if cur in targets:
            goal = cur
            break
        for dx,dy in dirs:
            nb = (cur[0]+dx, cur[1]+dy)
            if nb in valid and nb not in blocked:
                ng = g + 1
                if ng < gscore.get(nb, float('inf')):
                    gscore[nb] = ng
                    came_from[nb] = cur
                    heapq.heappush(open_set, (ng + hmap.get(nb), ng, nb))

    if not goal:
        print('경로 없음')
        return None, None

    # 경로 복원
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    path.reverse()
    print(f'경로 발견: {len(path)}단계')
    return path, goal

def save_path(path, goal, filename='home_to_cafe2.csv'):
    """경로를 CSV 파일로 저장합니다."""

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


def visualize_path_on_map(complete_df, path, target_cafe, filename='map_final2.png'):
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

            # 좌표를 잇는 빨간색 선 그리기
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
        ax.set_title(f'Shortest Path from MyHome to BandalgomCoffee\nPath Length: {len(path) if path else 0} steps', 
                    fontsize=16, fontweight='bold')
        
        # 이미지 저장
        plt.tight_layout()
        plt.savefig(filename, dpi=500, bbox_inches='tight')
        plt.close()
        
        print(f'최종 지도가 {filename} 파일로 저장되었습니다.')
                
    except Exception as e:
        print(f'지도 시각화 중 오류 발생: {e}')
        sys.exit(1)



def main():
    """메인 실행 함수"""
    
    print('=== Stage 3: 최단 경로 찾기 시작 ===')
    

    print('Stage 1에서 생성한 지도 통합 데이터 로드 중 ...','\n')
    
    try:
        # 1. 데이터 로딩
         
        path = 'data/complete_map_data.csv'
        complete_df = pd.read_csv(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f'오류: 지도 통합 데이터 "{path}"을(를) 찾을 수 없습니다. Stage 1을 먼저 실행하여 파일을 생성해 주세요.')
                   

        if complete_df.empty:
            raise ValueError(f'오류: 통합된 지도 데이터 파일 "{path}"이(가) 비어있습니다.')
            
        print(f'로드된 지도 통합 데이터: {len(complete_df)}개')

        # 2. 핵심 위치 찾기
        home_loc, cafes_loc, blocked_loc, valid = find_key_locations(complete_df)
        
        # 3. 최단 경로 탐색
        path, goal = astar_algorithm(home_loc, cafes_loc, blocked_loc, valid)

        if path is None:
            print('집에서 반달곰 커피까지의 경로를 찾을 수 없습니다.')
            sys.exit(1)
        
        # 4. 경로를 CSV 파일로 저장
        save_path(path, goal)

        # 5. 경로가 표시된 지도 시각화 및 저장
        visualize_path_on_map(complete_df, path, goal)

    except Exception as e:
        print(f'오류 발생: {e}')
        sys.exit(1)


    print('============\nStage 3 완료\n=============')

if __name__ == '__main__':
    main()
