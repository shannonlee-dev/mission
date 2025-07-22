"""
Stage 2: 지도 시각화

"""

import pandas as pd
import os
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys


def setup_map_figure(complete_df):
    """지도 시각화를 위한 matplotlib figure와 좌표계를 설정합니다."""
    # 좌표 범위 계산
    x_min, x_max = complete_df['x'].min(), complete_df['x'].max()
    y_min, y_max = complete_df['y'].min(), complete_df['y'].max()

    print(f'좌표 범위: X({x_min}~{x_max}), Y({y_min}~{y_max})')
    
    # figure 크기 설정 (좌표 비율에 맞춤)
    fig_width = (x_max - x_min + 1) * 0.8
    fig_height = (y_max - y_min + 1) * 0.8
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    for spine in ax.spines.values():
        spine.set_edgecolor('white') # 테두리 색상 설정
        spine.set_linewidth(2) 

    ax.set_xlim(x_min-1, x_max+1)
    ax.set_ylim(y_max+1, y_min-1)

            # 격자선 그리기 (건물이 격자선 위에 위치하도록 중심 좌표를 정수로 사용)
    for x in range(x_min, x_max + 1):
        ax.axvline(x=x, color='#212529', linestyle='-', alpha=0.8, zorder=0)
    for y in range(y_min, y_max + 1):
        ax.axhline(y=y, color='#212529', linestyle='-', alpha=0.8, zorder=0)

    # 축 설정 
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title('Map Visualization', fontsize=16, fontweight='bold')

    # 격자 눈금 설정 (번호가 격자선 위에 오도록)
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))

    return fig, ax, (x_min, x_max, y_min, y_max)


def draw_structures(ax, complete_df):
    """각 구조물을 지정된 색상과 모양으로 그립니다."""
    structure_counts = {
        'Apartment': 0,
        'Building': 0, 
        'BandalgomCoffee': 0,
        'MyHome': 0,
        'ConstructionSite': 0
    }
    
    for _, row in complete_df.iterrows():
        x, y = row['x'], row['y']
        struct_type = row['struct']
        is_construction = row['ConstructionSite'] == 1

        # 건물이 격자선 위에 위치하도록 중심 좌표를 정수로 사용
        if is_construction:
            # 회색 사각형으로 공사장 표시
            square = patches.Rectangle((x - 0.5, y - 0.5), 1.0, 1.0,
                                     facecolor='gray', edgecolor='gray',
                                     alpha=0.8, linewidth=0)
            ax.add_patch(square)
            structure_counts['ConstructionSite'] += 1

        else:
            # 구조물 타입에 따른 시각화
            if struct_type == 'Apartment':
                # 갈색 원으로 아파트 표시
                circle = patches.Circle((x, y), 0.4, facecolor='saddlebrown',
                                      edgecolor='#800000', alpha=1.0, linewidth=5)
                ax.add_patch(circle)
                structure_counts['Apartment'] += 1

            elif struct_type == 'Building':
                # 갈색 원으로 빌딩 표시
                circle = patches.Circle((x, y), 0.4, facecolor='saddlebrown',
                                      edgecolor='#003458', alpha=1.0, linewidth=5)
                ax.add_patch(circle)
                structure_counts['Building'] += 1

            elif struct_type == 'BandalgomCoffee':
                # 초록색 사각형으로 반달곰커피 표시
                square = patches.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8,
                                         facecolor='green', edgecolor='darkgreen',
                                         alpha=0.9, linewidth=3)
                ax.add_patch(square)
                structure_counts['BandalgomCoffee'] += 1

            elif struct_type == 'MyHome':
                # 초록색 삼각형으로 내 집 표시
                triangle_points = [(x, y - 0.35), (x - 0.35, y + 0.3), (x + 0.35, y + 0.3)]
                triangle = patches.Polygon(triangle_points,
                                         facecolor='green',
                                         edgecolor='darkgreen',
                                         alpha=0.9, linewidth=3)
                ax.add_patch(triangle)
                structure_counts['MyHome'] += 1
    
    return structure_counts


def add_legend(ax):
    """범례"""
    legend_elements = [
        patches.Circle((0, 0), 0.3, facecolor='saddlebrown', edgecolor='saddlebrown', 
                      alpha=0.8, label='Apartment/Building'),
        patches.Rectangle((0, 0), 0.6, 0.6, facecolor='green', edgecolor='darkgreen', 
                         alpha=0.9, label='Bandalgom Coffee'),
        patches.Polygon([(0, -0.3), (-0.3, 0.2), (0.3, 0.2)],
                       facecolor='green', 
                       edgecolor='darkgreen', alpha=0.9, label='My Home'),
        patches.Rectangle((0, 0), 0.8, 0.8, facecolor='gray', edgecolor='darkgray', 
                         alpha=0.8, label='Construction Site')
    ]
    
    ax.legend(handles=legend_elements, loc='upper left')


def save_map(fig, filename='map.png'):
    """지도를 PNG 파일로 저장합니다."""
    try:
        plt.tight_layout()
        fig.savefig(filename, dpi=500, bbox_inches='tight')
        print(f'지도가 {filename} 파일로 저장되었습니다.')
        
    except Exception as e:
        print(f'지도 저장 중 오류 발생: {e}')


def create_map_visualization():
    """메인 함수: 지도 시각화를 생성하고 저장합니다."""
    try:
        print('=== Stage 2: 지도 시각화 시작 ===')
        # 1. 데이터 로딩
        print('Stage 1에서 생성한 지도 통합 데이터 로드 중 ...','\n')
        path = 'data/complete_map_data.csv'

        if not os.path.exists(path):
            raise FileNotFoundError(f'오류: 지도 통합 데이터 "{path}"을(를) 찾을 수 없습니다. Stage 1을 먼저 실행하여 파일을 생성해 주세요.')

        complete_df = pd.read_csv(path)

        if complete_df.empty:
            raise ValueError(f'오류: 통합된 지도 데이터 파일 "{path}"이(가) 비어있습니다.')
        
        print(f'전달된 지도 통합 데이터: {len(complete_df)}개')  


        # 2. 그래프 설정
        print('지도 figure 설정 중...')
        fig, ax, coord_range = setup_map_figure(complete_df)
        
        # 3. 구조물 그리기
        print('구조물을 지도에 표시하는 중...')
        structure_counts = draw_structures(ax, complete_df)
        
        # 4. 범례 추가
        print('범례 추가 중...')
        add_legend(ax)
        
        # 5. 지도 저장
        save_map(fig, 'map.png')
    
        plt.close(fig)  

    except Exception as e:
        print(f'지도 시각화 중 치명적 오류 발생: {e}')
        sys.exit(1)


if __name__ == '__main__':
    try:  # 데이터 파일 경로
        create_map_visualization()
        print('\n Stage 2 완료: map.png 파일이 생성되었습니다.')
        
    except KeyboardInterrupt:
        print('\n\n사용자에 의해 중단되었습니다.')
        sys.exit(1)
    except Exception as e:
        print(f'\n프로그램 실행 중 오류 발생: {e}')
        sys.exit(1)
