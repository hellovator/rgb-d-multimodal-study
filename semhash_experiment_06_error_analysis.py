
import pandas as pd
from pathlib import Path

# ==============================
# Experiment 06: Error Analysis
# ==============================

input_file = Path("results/experiment_06_pair_scores.csv")
output_file = Path("results/experiment_06_error_analysis.csv")

if not input_file.exists():
    raise FileNotFoundError(f"找不到文件：{input_file}")

df = pd.read_csv(input_file)

required = [
    "pair_id", "text_a", "text_b",
    "gold_label", "category", "similarity"
]

missing = [col for col in required if col not in df.columns]
if missing:
    raise ValueError(
        f"CSV 缺少字段：{missing}\n"
        f"实际字段为：{df.columns.tolist()}"
    )

df["gold_label"] = df["gold_label"].astype(int)
df["similarity"] = pd.to_numeric(
    df["similarity"], errors="coerce"
)

if df["similarity"].isna().any():
    raise ValueError("相似度列存在无法转换的数值")

# 使用本次单阈值探索中 F1 最高的阈值
threshold = 0.50

df["predicted_label"] = (
    df["similarity"] >= threshold
).astype(int)

def get_error_type(row):
    if row["gold_label"] == 0 and row["predicted_label"] == 1:
        return "FP_false_duplicate"
    if row["gold_label"] == 1 and row["predicted_label"] == 0:
        return "FN_missed_duplicate"
    return "correct"

df["error_type"] = df.apply(get_error_type, axis=1)

# 输出整体统计
print("=" * 65)
print("Experiment 06: Error Analysis")
print("=" * 65)

print(f"\n分析样本数：{len(df)}")
print(f"分析阈值：{threshold}")

print("\n一、预测结果统计")
print(df["error_type"].value_counts().to_string())

# 输出误判样本
errors = df[df["error_type"] != "correct"].copy()

print("\n二、误判样本详情")
if errors.empty:
    print("没有发现误判样本")
else:
    for _, row in errors.iterrows():
        print("-" * 65)
        print(f"编号：{row['pair_id']}")
        print(f"类别：{row['category']}")
        print(f"人工标签：{row['gold_label']}")
        print(f"模型预测：{row['predicted_label']}")
        print(f"相似度：{row['similarity']:.4f}")
        print(f"误判类型：{row['error_type']}")
        print(f"文本A：{row['text_a']}")
        print(f"文本B：{row['text_b']}")

# 按类别分析
print("\n三、各类别相似度和误判情况")

category_stats = (
    df.groupby("category")
    .agg(
        sample_count=("pair_id", "count"),
        mean_similarity=("similarity", "mean"),
        min_similarity=("similarity", "min"),
        max_similarity=("similarity", "max"),
        error_count=(
            "error_type",
            lambda x: (x != "correct").sum()
        )
    )
    .reset_index()
)

print(category_stats.to_string(index=False))

# 保存完整误判分析数据
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"\n完整分析结果已保存：{output_file}")
print("\n误判分析完成。")
