
import json
from pathlib import Path

import pandas as pd

# =========================
# 1. 文件路径
# =========================
DATA_PATH = Path("data/semhash_pair_dataset.csv")
RESULT_DIR = Path("results")
RESULT_DIR.mkdir(exist_ok=True)

# =========================
# 2. 读取数据
# =========================
df = pd.read_csv(DATA_PATH)

required_columns = [
    "pair_id",
    "text_a",
    "text_b",
    "gold_label",
    "category",
    "annotator",
    "notes",
]

# =========================
# 3. 基础检查
# =========================
missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(f"缺少字段：{missing_columns}")

checks = {}

checks["total_samples"] = int(len(df))
checks["missing_values"] = int(df[required_columns].isnull().sum().sum())
checks["duplicate_ids"] = int(df["pair_id"].duplicated().sum())

checks["empty_texts"] = int(
    (
        df["text_a"].astype(str).str.strip().eq("")
        | df["text_b"].astype(str).str.strip().eq("")
    ).sum()
)

checks["invalid_labels"] = int(
    (~df["gold_label"].isin([0, 1])).sum()
)

# =========================
# 4. 类别和标签分布
# =========================
category_counts = df["category"].value_counts().to_dict()
label_counts = df["gold_label"].value_counts().to_dict()

expected_categories = {
    "exact_duplicate",
    "paraphrase",
    "similar_topic",
    "partial_overlap",
    "unrelated",
}

checks["category_count"] = len(category_counts)
checks["missing_categories"] = sorted(
    expected_categories - set(category_counts.keys())
)

checks["unexpected_categories"] = sorted(
    set(category_counts.keys()) - expected_categories
)

# =========================
# 5. 检查重复文本对
# =========================
normalized_a = df["text_a"].astype(str).str.strip().str.lower()
normalized_b = df["text_b"].astype(str).str.strip().str.lower()

pair_keys = pd.Series(
    [
        tuple(sorted((a, b)))
        for a, b in zip(normalized_a, normalized_b)
    ]
)

checks["duplicate_text_pairs"] = int(
    pair_keys.duplicated().sum()
)

# =========================
# 6. 检查类别与标签的明显冲突
# =========================
expected_labels = {
    "exact_duplicate": 1,
    "paraphrase": 1,
    "similar_topic": 0,
    "partial_overlap": 0,
    "unrelated": 0,
}

conflict_mask = df.apply(
    lambda row: (
        row["category"] in expected_labels
        and row["gold_label"] != expected_labels[row["category"]]
    ),
    axis=1,
)

checks["category_label_conflicts"] = int(conflict_mask.sum())

# =========================
# 7. 汇总结果
# =========================
report = {
    "checks": checks,
    "category_distribution": {
        str(k): int(v)
        for k, v in category_counts.items()
    },
    "label_distribution": {
        str(k): int(v)
        for k, v in label_counts.items()
    },
    "conflict_pair_ids": df.loc[
        conflict_mask, "pair_id"
    ].astype(str).tolist(),
}

output_path = RESULT_DIR / "experiment_06_data_quality_report.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=4)

# 同时保存类别与标签统计表
summary = (
    df.groupby(["category", "gold_label"])
    .size()
    .reset_index(name="count")
)

summary.to_csv(
    RESULT_DIR / "experiment_06_data_quality_summary.csv",
    index=False,
    encoding="utf-8-sig",
)

print("========== 实验六数据质量审查 ==========")
print("总样本数：", checks["total_samples"])
print("缺失值：", checks["missing_values"])
print("重复编号：", checks["duplicate_ids"])
print("空文本：", checks["empty_texts"])
print("非法标签：", checks["invalid_labels"])
print("类别数量：", checks["category_count"])
print("重复文本对：", checks["duplicate_text_pairs"])
print("类别与标签冲突：", checks["category_label_conflicts"])
print("----------------------------------------")
print("类别分布：")
print(df["category"].value_counts())
print("----------------------------------------")
print("标签分布：")
print(df["gold_label"].value_counts())
print("----------------------------------------")
print("报告已保存：", output_path)
print("统计表已保存：results/experiment_06_data_quality_summary.csv")
