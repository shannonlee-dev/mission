import os
from typing import Tuple

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_data(train_path: str = "train.csv", test_path: str = "test.csv") -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    bool_like = ["CryoSleep", "VIP", "Transported"]
    for df in (train_df, test_df):
        for col in bool_like:
            if col in df.columns:
                if df[col].dtype == object:
                    df[col] = df[col].map({"True": True, "False": False})
                if str(df[col].dtype) in ("bool", "boolean"):
                    df[col] = df[col].astype("boolean")
    return train_df, test_df


def merge_data(train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:
    train_df = train_df.copy()
    test_df = test_df.copy()
    train_df["dataset"] = "train"
    test_df["dataset"] = "test"
    combined = pd.concat([train_df, test_df], ignore_index=True, sort=False)
    return combined


def most_correlated_with_transported(train_df: pd.DataFrame) -> Tuple[str, float]:
    if "Transported" not in train_df.columns:
        raise ValueError("Transported column not found in train data")

    df = train_df.copy()
    df = df[df["Transported"].notna()]

    num_bool_df = df.select_dtypes(include=["number", "boolean"]).copy()

    if "Transported" in num_bool_df.columns:
        if str(num_bool_df["Transported"].dtype) == "boolean":
            target = num_bool_df["Transported"].astype("Int64").astype(float)
        else:
            target = num_bool_df["Transported"].astype(float)
    else:
        target = df["Transported"].astype("boolean").astype("Int64").astype(float)

    features = num_bool_df.drop(columns=["Transported"], errors="ignore").copy()

    for c in features.columns:
        if str(features[c].dtype) == "boolean":
            features[c] = features[c].astype("Int64").astype(float)

    corrs = features.apply(lambda s: s.corr(target), axis=0).dropna()
    if corrs.empty:
        return "<none>", float("nan")

    top_feature = corrs.abs().idxmax()
    return top_feature, float(corrs[top_feature])


def plot_age_by_transported(train_df: pd.DataFrame, out_path: str = "age_transport.png") -> str:

    df = train_df[["Age", "Transported"]].dropna(subset=["Age", "Transported"]).copy()
    bins = [10, 20, 30, 40, 50, 60, 70, 80]
    labels = ["10대", "20대", "30대", "40대", "50대", "60대", "70대"]
    df["age_group"] = pd.cut(df["Age"], bins=bins, right=False, labels=labels)
    df = df.dropna(subset=["age_group"]) 

    count_tbl = (
        df.groupby(["age_group", "Transported"]).size().unstack(fill_value=0)
    )
    if True not in count_tbl.columns:
        count_tbl[True] = 0
    if False not in count_tbl.columns:
        count_tbl[False] = 0
    count_tbl = count_tbl[[False, True]]

    ax = count_tbl.plot(kind="bar", figsize=(10, 6))
    ax.set_xlabel("연령대")
    ax.set_ylabel("인원 수")
    ax.set_title("연령대별 Transported 여부")
    ax.legend(["False", "True"], title="Transported")
    plt.tight_layout()

    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path


def main():
    train_df, test_df = load_data()
    combined = merge_data(train_df, test_df)

    total_count = len(combined)

    top_feat, top_corr = most_correlated_with_transported(train_df)

    out_img = plot_age_by_transported(train_df)

    print("전체 데이터 수량:", total_count)
    if top_feat == "<none>" or np.isnan(top_corr):
        print("관련성 계산을 위한 유효한 숫자형 특징을 찾지 못했습니다.")
    else:
        print(f"Transported와 가장 관련성 높은 (수치형) 항목: {top_feat} (상관계수: {top_corr:.4f})")
    print(f"연령대별 Transported 그래프 저장: {os.path.abspath(out_img)}")


if __name__ == "__main__":
    main()