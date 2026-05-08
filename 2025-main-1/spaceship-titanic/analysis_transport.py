#!/usr/bin/env python3
"""
Spaceship Titanic 분석 스크립트
"""

import os
from pathlib import Path
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="Glyph .* missing from font.*")

# [BASE 경로 설정]
# - 이 스크립트 파일이 있는 폴더 경로를 구한다.
# - 나중에 train.csv, test.csv, 그래프 파일 저장 경로를 만들 때 사용한다.

BASE = Path(__file__).resolve().parent

def set_korean_font():
    """
    Matplotlib에서 한글이 깨지지 않도록 한글 폰트를 찾아 설정하는 함수.
    """

    import matplotlib
    font_name = "Apple SD Gothic Neo"
    matplotlib.rcParams["font.family"] = font_name
    matplotlib.rcParams["axes.unicode_minus"] = False
    return font_name

def read_data():
    """
    현재 스크립트 파일과 같은 폴더(BASE)에 있는
    `train.csv`와 `test.csv`를 읽어서 DataFrame 두 개를 반환한다.

    반환값:
        train, test : pandas DataFrame
    """
    train_path = BASE / "train.csv"
    test_path = BASE / "test.csv"

    # 파일이 실제로 존재하는지 확인
    if not train_path.exists() or not test_path.exists():
        raise FileNotFoundError(f"{BASE}에 train.csv 또는 test.csv가 없습니다.")

    # pandas로 CSV 파일 읽기
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    return train, test

def merge_data(train, test):
    """
    train과 test DataFrame을 위아래로 이어붙여서(행 방향으로) 하나의 DataFrame으로 합친다.

    axis=0 : 행 방향으로 병합
    ignore_index=True : 기존 인덱스를 무시하고 0부터 다시 인덱스를 매김
    sort=False : 컬럼 정렬을 하지 않고 원래 순서를 유지

    반환값:
        merged : train + test가 합쳐진 DataFrame
    """
    merged = pd.concat([train, test], axis=0, ignore_index=True, sort=False)
    return merged


def feature_importance_tree(train_df, target_col="Transported", top_n=10, random_state=42):
    """
    RandomForestClassifier(랜덤포레스트 분류 모델)를 사용해서
    특성 중요도(feature importance)를 계산하고,
    추가로 permutation importance(치환 중요도)도 계산하는 함수.

    1. 타깃(Transported)을 0/1로 변환하고, 나머지를 입력 특성으로 사용한다.
    2. 범주형 컬럼은 LabelEncoder로 숫자 인코딩, 숫자형은 결측치를 중앙값으로 대체한다.
    3. 데이터의 일부를 검증용(Validation set)으로 나누어
       랜덤포레스트 모델을 학습한다.
    4. 학습된 모델에서 제공하는 feature_importances_로 특성 중요도를 구한다.
    5. permutation_importance를 이용해서 검증 데이터 기준 치환 중요도를 구한다.

    반환값:
        (fi, perm)
        - fi   : 랜덤포레스트의 feature_importances_ 기준 상위 top_n (pandas Series)
        - perm : permutation importance 기준 상위 top_n (pandas Series)
    """
    df = train_df.copy()

    if target_col not in df.columns:
        raise ValueError(f"데이터프레임에 {target_col} 컬럼이 없습니다.")

    # 타깃 y: Transported를 0/1 정수로 변환
    y = df[target_col].astype(bool).map({False: 0, True: 1}).astype(int)

    # 입력 특성 X: target_col을 제외한 나머지
    X = df.drop(columns=[target_col])

    # 식별자(ID)로 보이는 컬럼 삭제 (예: PassengerId)
    drop_cols = [c for c in X.columns if c.lower().startswith("passenger")]
    X = X.drop(columns=drop_cols, errors="ignore")

    # 인코딩을 위한 복사본
    X_enc = X.copy()

    # 범주형 -> LabelEncoder, 숫자형 -> 결측치 중앙값 대체
    for col in X_enc.columns:
        if X_enc[col].dtype == object or X_enc[col].dtype.name == "category":
            X_enc[col] = X_enc[col].fillna("<NA>")
            le = LabelEncoder()
            X_enc[col] = le.fit_transform(X_enc[col].astype(str))
        else:
            X_enc[col] = X_enc[col].fillna(X_enc[col].median())

    # 특성이 하나도 없으면 빈 Series 반환
    if X_enc.shape[1] == 0:
        return pd.Series(dtype=float), pd.Series(dtype=float)

    # -----------------------------------------------------------------
    # [train/validation 데이터 분할]
    # - model이 학습에 사용하지 않은 데이터(검증용)를 따로 만들어
    #   permutation importance를 신뢰성 있게 계산하기 위함.
    # - stratify=y : 타깃 값 비율을 train/val에 비슷하게 유지 (분류 문제에서 자주 사용)
    # -----------------------------------------------------------------
    X_train, X_val, y_train, y_val = train_test_split(
        X_enc,
        y,
        test_size=0.25,  # 데이터의 25%를 검증용으로 사용
        random_state=random_state,
        stratify=y if y.nunique() > 1 else None,
    )

    # -----------------------------------------------------------------
    # [랜덤포레스트 모델 생성 및 학습]
    # -----------------------------------------------------------------
    clf = RandomForestClassifier(
        n_estimators=200,  # 트리 개수
        max_depth=7,       # 트리의 최대 깊이 (과적합 방지용)
        random_state=random_state,
        n_jobs=-1,         # 가능한 모든 CPU 코어 사용
    )
    clf.fit(X_train, y_train)

    # feature_importances_ : 모델이 각 특성을 얼마나 많이 사용했는지에 대한 중요도
    fi = pd.Series(clf.feature_importances_, index=X_enc.columns).sort_values(ascending=False)

    # -----------------------------------------------------------------
    # [Permutation Importance 계산]
    # -----------------------------------------------------------------
    try:
        perm = permutation_importance(
            clf,
            X_val,
            y_val,
            n_repeats=10,       # 섞는 실험을 10번 반복
            random_state=random_state,
            n_jobs=-1,
        )
        perm_series = pd.Series(perm.importances_mean, index=X_enc.columns).sort_values(ascending=False)
    except Exception:
        # 에러가 나면 빈 Series 반환
        perm_series = pd.Series(dtype=float)

    # 상위 top_n개만 반환
    return fi.head(top_n), perm_series.head(top_n)


def plot_transported_by_decade(df, target_col="Transported", output_path=None):
    """
    연령대(10대~70대)별로 `Transported` 비율을 계산해서 막대그래프로 그리고,
    그 그래프를 이미지 파일(PNG)로 저장하는 함수.
    """
    d = df.copy()

    if target_col not in d.columns:
        raise ValueError(f"플롯을 위한 데이터프레임에 {target_col} 컬럼이 없습니다.")

    # Age가 NaN이 아닌 행만 사용
    d = d[pd.notnull(d["Age"])].copy()

    # Age를 숫자로 변환 (문자가 끼어 있어도 숫자만 추출되도록)
    d["Age"] = pd.to_numeric(d["Age"], errors="coerce")
    d = d[pd.notnull(d["Age"])].copy()

    # 연령대를 나누기 위한 경계값(bins)과 라벨(labels)
    # 예: 10 <= Age < 20 => "10대"
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    labels = ["0대", "10대", "20대", "30대", "40대", "50대", "60대", "70대"]

    # pd.cut으로 나이를 구간별(연령대별)로 자르고, 해당 구간의 라벨을 decade 컬럼에 저장
    d["decade"] = pd.cut(d["Age"], bins=bins, labels=labels, right=False)

    # 과제에서 요구하는 것은 10대~70대 이므로 0대는 제외
    wanted = ["10대", "20대", "30대", "40대", "50대", "60대", "70대"]
    plot_df = d[d["decade"].isin(wanted)].copy()

    # Transported를 0/1로 변환해서 평균을 내면 곧 비율이 된다.
    plot_df["Transported_bin"] = plot_df[target_col].astype(bool).map({False: 0, True: 1}).astype(int)

    # 연령대별로 Transported 비율(mean)과 샘플 수(count) 계산
    agg = (
        plot_df.groupby("decade")["Transported_bin"]
        .agg(["mean", "count"])   # mean: 비율, count: 사람 수
        .reindex(wanted)          # wanted 순서대로 재정렬
    )

    sns.set(style="whitegrid")  # 배경 스타일 설정

    # 한글 폰트 설정 시도
    font_name = set_korean_font()
    if font_name:
        # seaborn에 폰트가 반영되도록 font 파라미터 설정
        sns.set(font=font_name)

    plt.figure(figsize=(9, 5))  # 그래프 크기 설정

    # 막대그래프 생성: x축은 연령대, y축은 Transported 비율
    ax = sns.barplot(x=agg.index, y=agg["mean"].values)

    ax.set_ylim(0, 1)  # 비율이므로 0~1 범위로 고정
    ax.set_ylabel("Transported 비율 (0-1)")
    ax.set_xlabel("연령대")
    ax.set_title("연령대별 Transported 비율 (10대~70대)")

    # 각 막대 위에 비율 값과 샘플 수(n)를 표시
    for i, (mean_val, cnt) in enumerate(zip(agg["mean"].values, agg["count"].values)):
        ax.text(
            i,                       # x 위치 (막대 중앙)
            mean_val + 0.02,        # y 위치 (막대 위 약간 위)
            f"{mean_val:.2f}\n(n={int(cnt)})",  # 표시할 문자열: 비율, 샘플 수
            ha="center",            # 가운데 정렬
        )

    plt.tight_layout()

    # 파일 저장 경로 설정
    if output_path is None:
        output_path = BASE / "transported_by_decade.png"
    else:
        output_path = Path(output_path)

    # 그래프를 PNG 파일로 저장
    plt.savefig(output_path)
    plt.close()  # 그래프 창 닫기 (메모리 정리용)

    return output_path

def main():
    """
    1. train.csv, test.csv를 읽고 행 수를 출력한다.
    2. 둘을 병합해서 전체 행 수를 출력한다.
    3. train 기준으로 mutual information으로 특성 중요도를 계산하고 출력한다.
    4. 랜덤포레스트 기반 특성 중요도와 permutation importance를 계산하고 출력한다.
    5. 연령대별(10대~70대) Transported 비율을 그래프로 그려 파일로 저장한다.
    """
    print("데이터 읽는 중...")
    train, test = read_data()
    print(f"train 행 수: {len(train):,}  test 행 수: {len(test):,}")

    # train과 test를 단순히 합쳐서 전체 행 수를 확인
    merged = merge_data(train, test)
    print(f"병합 후 총 행 수: {len(merged):,}")

    print("\n랜덤포레스트 기반 특성 중요도 계산 중...")
    try:
        fi, perm = feature_importance_tree(train, target_col="Transported", top_n=15)
        if not fi.empty:
            print("RandomForest feature_importances:")
            for feat, score in fi.items():
                print(f"  {feat}: {score:.6f}")
        if not perm.empty:
            print("Permutation importance (validation set):")
            for feat, score in perm.items():
                print(f"  {feat}: {score:.6f}")
    except Exception as e:
        print("랜덤포레스트 기반 중요도 계산 실패:", e)

    print("\n연령대(10대~70대)별 Transported 비율 그래프 생성 중...")
    try:
        out = plot_transported_by_decade(train, target_col="Transported")
        print(f"그래프 파일 저장 위치: {out}")
    except Exception as e:
        print("연령대별 그래프 생성 실패:", e)

if __name__ == "__main__":
    main()