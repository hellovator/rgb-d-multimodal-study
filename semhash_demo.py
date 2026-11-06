
from semhash import SemHash
from pathlib import Path
from collections import Counter
import csv
import json
from datetime import datetime

# =====================================
# 1. 构建人工标注测试集
# =====================================

texts = [
    "The cat is sleeping on the sofa.",
    "The cat is sleeping on the sofa.",
    "A cat is taking a nap on the couch.",
    "The weather is sunny today.",
    "It is a beautiful sunny day.",
    "Python is a popular programming language.",
    "Python is widely used for software development.",
    "I like eating apples.",
    "I enjoy eating apples.",
    "The football match starts at eight."
]

# 人工认定应该被过滤的重复文本
expected_duplicates = [
    "The cat is sleeping on the sofa.",
    "A cat is taking a nap on the couch.",
    "It is a beautiful sunny day.",
    "I enjoy eating apples."
]

print("原始文本数量：", len(texts))
print("人工标注的重复文本数量：", len(expected_duplicates))

# =====================================
# 2. 创建结果保存目录
# =====================================

save_dir = Path("results")
save_dir.mkdir(exist_ok=True)

# =====================================
# 3. 设置实验阈值
# =====================================

thresholds = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]

summary = []
details = []

# =====================================
# 4. 逐个阈值进行实验
# =====================================

for threshold in thresholds:

    semhash = SemHash.from_records(records=texts)

    result = semhash.self_deduplicate(
        threshold=threshold
    )

    # 获取模型过滤的文本
    predicted_duplicates = [
        item.record for item in result.filtered
    ]

    # 使用 Counter 统计，避免完全相同的文本
    # 在集合比较时被错误地合并
    expected_count = Counter(expected_duplicates)
    predicted_count = Counter(predicted_duplicates)

    # 计算真正识别正确的重复文本数量
    true_positive = sum(
        (expected_count & predicted_count).values()
    )

    # 误删数量
    false_positive = len(predicted_duplicates) - true_positive

    # 漏检数量
    false_negative = len(expected_duplicates) - true_positive

    # Precision：准确率（查准率）
    precision = (
        true_positive / len(predicted_duplicates)
        if predicted_duplicates else 0
    )

    # Recall：召回率
    recall = (
        true_positive / len(expected_duplicates)
        if expected_duplicates else 0
    )

    # F1-score：综合评价指标
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    print("\n" + "=" * 40)
    print("当前阈值：", threshold)
    print("原始数量：", len(texts))
    print("保留数量：", len(result.selected))
    print("过滤数量：", len(result.filtered))
    print("真正识别数量：", true_positive)
    print("误删数量：", false_positive)
    print("漏检数量：", false_negative)
    print("Precision：", round(precision, 4))
    print("Recall：", round(recall, 4))
    print("F1-score：", round(f1, 4))

    # 保存汇总数据
    summary.append({
        "threshold": threshold,
        "original_count": len(texts),
        "selected_count": len(result.selected),
        "filtered_count": len(result.filtered),
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    })

    # 保存详细过滤记录
    for item in result.filtered:
        details.append({
            "threshold": threshold,
            "record": item.record,
            "duplicate_of": item.duplicate_of,
            "score": item.score
        })

# =====================================
# 5. 保存实验结果
# =====================================

# 保存汇总 CSV
with open(
    save_dir / "experiment_03_summary.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=summary[0].keys()
    )

    writer.writeheader()
    writer.writerows(summary)

# 保存详细 CSV
with open(
    save_dir / "experiment_03_details.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=details[0].keys()
    )

    writer.writeheader()
    writer.writerows(details)

# 保存完整 JSON
experiment_data = {
    "experiment": "实验三：人工标注测试集评价",
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "original_texts": texts,
    "expected_duplicates": expected_duplicates,
    "threshold_results": summary
}

with open(
    save_dir / "experiment_03.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        experiment_data,
        f,
        ensure_ascii=False,
        indent=4
    )

print("\n========== 实验三完成 ==========")
print("汇总结果：results/experiment_03_summary.csv")
print("详细结果：results/experiment_03_details.csv")
print("完整数据：results/experiment_03.json")
