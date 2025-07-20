"""
Stage 2: 지도 시각화

이 모듈은 분석된 데이터를 기반으로 지역 지도를 시각화합니다.
좌표계는 왼쪽 상단을 (1,1)로, 오른쪽 하단을 가장 큰 좌표로 설정하며,
각 구조물을 지정된 색상과 모양으로 표현합니다.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 반드시 plt, patches 등 import 전에 실행
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys


def load_analyzed_data():
    """Stage 1에서 분석한 데이터를 로드합니다."""
    try:
        print('분석된 데이터를 로드하는 중...')
        
        # Stage 1의 함수들을 재사용하기 위해 import
        # 직접 데이터를 다시 로드하여 전체 맵 데이터를 얻음
        area_map_df = pd.read_csv('data/area_map.csv')
        area_struct_df = pd.read_csv('data/area_struct.csv')
        area_category_df = pd.read_csv('data/area_category.csv')
        
        # 카테고리 데이터 정리
        area_category_df.columns = area_category_df.columns.str.strip()
        area_category_df['struct'] = area_category_df['struct'].str.strip()
        
        # 구조물 이름 매핑
        merged_df = pd.merge(area_struct_df, area_category_df, on='category', how='left')
        merged_df['struct'] = merged_df['struct'].fillna('Empty')
        
        # 전체 데이터 병합 (모든 구역 포함)
        complete_df = pd.merge(area_map_df, merged_df, on=['x', 'y'], how='inner')
        
        print(f'✅ 전체 지도 데이터 로드 완료: {len(complete_df)}개 레코드')
        return complete_df
        
    except Exception as e:
        print(f'❌ 데이터 로드 중 오류 발생: {e}')
        sys.exit(1)


def setup_map_figure(complete_df):
    """지도 시각화를 위한 matplotlib figure와 좌표계를 설정합니다."""
    # 좌표 범위 계산
    x_min, x_max = complete_df['x'].min(), complete_df['x'].max()
    y_min, y_max = complete_df['y'].min(), complete_df['y'].max()

    print(f'좌표 범위: X({x_min}~{x_max}), Y({y_min}~{y_max})')

    # figure 크기 설정 (좌표 비율에 맞춤)
    fig_width = max(10, (x_max - x_min + 1) * 0.8)
    fig_height = max(8, (y_max - y_min + 1) * 0.8)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # 좌표계 설정: 왼쪽 상단이 (1,1), 오른쪽 하단이 최대 좌표
    # matplotlib에서 y축을 뒤집어야 함 (기본적으로 아래가 원점)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_max, y_min)

    # 격자선 그리기 (건물이 격자선 위에 위치하도록)
    for x in range(x_min, x_max + 1):
        ax.axvline(x=x, color='lightgray', linestyle='-', alpha=0.7)
    for y in range(y_min, y_max + 1):
        ax.axhline(y=y, color='lightgray', linestyle='-', alpha=0.7)

    # 축 설정 (번호가 격자선 위에 오도록)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    ax.set_title('Regional Map Visualization', fontsize=16, fontweight='bold')

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
                                     facecolor='gray', edgecolor='darkgray',
                                     alpha=0.8, linewidth=1)
            ax.add_patch(square)
            structure_counts['ConstructionSite'] += 1

        else:
            # 구조물 타입에 따른 시각화
            if struct_type == 'Apartment':
                # 갈색 원으로 아파트 표시
                circle = patches.Circle((x, y), 0.4, facecolor='brown',
                                      edgecolor='darkred', alpha=1.0, linewidth=1)
                ax.add_patch(circle)
                structure_counts['Apartment'] += 1

            elif struct_type == 'Building':
                # 갈색 원으로 빌딩 표시
                circle = patches.Circle((x, y), 0.4, facecolor='brown',
                                      edgecolor='darkred', alpha=1.0, linewidth=1)
                ax.add_patch(circle)
                structure_counts['Building'] += 1

            elif struct_type == 'BandalgomCoffee':
                # 초록색 사각형으로 반달곰커피 표시
                square = patches.Rectangle((x - 0.4, y - 0.4), 0.8, 0.8,
                                         facecolor='green', edgecolor='darkgreen',
                                         alpha=0.9, linewidth=2)
                ax.add_patch(square)
                structure_counts['BandalgomCoffee'] += 1

            elif struct_type == 'MyHome':
                # 초록색 삼각형으로 내 집 표시 (Polygon 사용)
                triangle_points = [(x, y - 0.35), (x - 0.35, y + 0.3), (x + 0.35, y + 0.3)]
                triangle = patches.Polygon(triangle_points,
                                         facecolor='limegreen',
                                         edgecolor='darkgreen',
                                         alpha=0.9, linewidth=2)
                ax.add_patch(triangle)
                structure_counts['MyHome'] += 1
    
    return structure_counts


def add_legend(ax):
    """범례를 추가합니다."""
    legend_elements = [
        patches.Circle((0, 0), 0.3, facecolor='brown', edgecolor='darkred', 
                      alpha=0.8, label='Apartment/Building'),
        patches.Rectangle((0, 0), 0.6, 0.6, facecolor='green', edgecolor='darkgreen', 
                         alpha=0.9, label='Bandalkom Coffee'),
        patches.Polygon([(0, -0.3), (-0.3, 0.2), (0.3, 0.2)],
                       facecolor='limegreen', 
                       edgecolor='darkgreen', alpha=0.9, label='My Home'),
        patches.Rectangle((0, 0), 0.8, 0.8, facecolor='gray', edgecolor='darkgray', 
                         alpha=0.8, label='Construction Site')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.0, 1.0))


def save_map(fig, filename='map.png'):
    """지도를 PNG 파일로 저장합니다."""
    try:
        plt.tight_layout()
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        print(f'✅ 지도가 {filename} 파일로 저장되었습니다.')
        
    except Exception as e:
        print(f'❌ 지도 저장 중 오류 발생: {e}')


def create_map_visualization():
    """메인 함수: 지도 시각화를 생성하고 저장합니다."""
    try:
        print('=== Stage 2: 지도 시각화 시작 ===')
        
        # 1. 데이터 로드
        complete_df = load_analyzed_data()
        
        # 2. 그래프 설정
        print('지도 figure 설정 중...')
        fig, ax, coord_range = setup_map_figure(complete_df)
        
        # 3. 구조물 그리기
        print('구조물을 지도에 표시하는 중...')
        structure_counts = draw_structures(ax, complete_df)
        
        # 4. 범례 추가
        add_legend(ax)
        
        # 5. 지도 저장
        save_map(fig, 'map.png')
        
        # 6. 결과 요약 출력
        print('\n=== 지도 시각화 완료 ===')
        print('구조물 분포:')
        for struct_type, count in structure_counts.items():
            if count > 0:
                print(f'  - {struct_type}: {count}개')
                
        print(f'좌표 범위: X({coord_range[0]}~{coord_range[1]}), Y({coord_range[2]}~{coord_range[3]})')
        
        # matplotlib 창 표시 (필요한 경우)
        # plt.show()
        
        plt.close(fig)  # 메모리 정리
        
    except Exception as e:
        print(f'❌ 지도 시각화 중 치명적 오류 발생: {e}')
        sys.exit(1)


if __name__ == '__main__':
    try:
        create_map_visualization()
        print('\n✅ Stage 2 완료: map.png 파일이 생성되었습니다.')
        
    except KeyboardInterrupt:
        print('\n\n❌ 사용자에 의해 중단되었습니다.')
        sys.exit(1)
    except Exception as e:
        print(f'\n❌ 프로그램 실행 중 오류 발생: {e}')
        sys.exit(1)
