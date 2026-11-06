
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

# 人工标注的重复文本
expected_duplicates = [
    "The cat is sleeping on the sofa.",
    "A cat is taking a nap on the couch.",
    "It is a beautiful sunny day.",
    "I enjoy eating apples."
]

print("原始文本数量：", len(texts))
print("人工标注的重复文本数量：", len(expected_duplicates))

# =====================================
# 2. 设置双阈值
# =====================================

LOW_THRESHOLD = 0.65
HIGH_THRESHOLD = 0.85

# =====================================
# 3. 创建 SemHash
# =====================================

semhash = SemHash.from_records(records=texts)

# =====================================
# 4. 使用低阈值寻找候选重复文本
# =====================================

result = semhash.self_deduplicate(
    threshold=LOW_THRESHOLD
)

# =====================================
# 5. 双阈值分类
# =====================================

high_confidence = []
manual_review = []

# SemHash 原本保留的文本
kept = list(result.selected)

for item in result.filtered:

    if item.score >= HIGH_THRESHOLD:

        # 高相似度：自动过滤
        high_confidence.append(item)

    else:

        # 中间相似度：进入人工复核
        manual_review.append(item)

        # 暂时保留
        kept.append(item.record)

# =====================================
# 6. 输出实验结果
# =====================================

print("\n========== 实验四：双阈值去重 ==========")

print("低阈值：", LOW_THRESHOLD)
print("高阈值：", HIGH_THRESHOLD)

print("原始数量：", len(texts))
print("自动过滤数量：", len(high_confidence))
print("人工复核数量：", len(manual_review))
print("最终暂时保留数量：", len(kept))

print("\n========== 自动过滤文本 ==========")

for item in high_confidence:
    print("文本：", item.record)
    print("参考文本：", item.duplicate_of)
    print("相似度：", round(item.score, 4))
    print("-" * 40)

print("\n========== 人工复核文本 ==========")

for item in manual_review:
    print("待复核文本：", item.record)
    print("参考文本：", item.duplicate_of)
    print("相似度：", round(item.score, 4))
    print("-" * 40)

# =====================================
# 7. 评价双阈值策略
# =====================================

expected_count = Counter(expected_duplicates)

# 只将自动过滤的文本作为预测删除结果
predicted_count = Counter(
    item.record for item in high_confidence
)

# 正确识别数量
true_positive = sum(
    (expected_count & predicted_count).values()
)

# 误删除数量
false_positive = (
    len(high_confidence) - true_positive
)

# 漏检数量
false_negative = (
    len(expected_duplicates) - true_positive
)

precision = (
    true_positive / len(high_confidence)
    if high_confidence else 0
)

recall = (
    true_positive / len(expected_duplicates)
    if expected_duplicates else 0
)

f1 = (
    2 * precision * recall / (precision + recall)
    if precision + recall else 0
)

print("\n========== 双阈值评价指标 ==========")

print("真正识别数量：", true_positive)
print("误删除数量：", false_positive)
print("漏检数量：", false_negative)

print("Precision：", round(precision, 4))
print("Recall：", round(recall, 4))
print("F1-score：", round(f1, 4))

# =====================================
# 8. 保存实验结果
# =====================================

save_dir = Path("results")
save_dir.mkdir(exist_ok=True)

# 保存详细记录
details = []

for item in result.filtered:

    decision = (
        "自动过滤"
        if item.score >= HIGH_THRESHOLD
        else "人工复核"
    )

    details.append({
        "record": item.record,
        "duplicate_of": item.duplicate_of,
        "score": item.score,
        "decision": decision
    })

# 保存 CSV
with open(
    save_dir / "experiment_04_details.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "record",
            "duplicate_of",
            "score",
            "decision"
        ]
    )

    writer.writeheader()
    writer.writerows(details)

# 保存汇总数据
summary = {
    "experiment": "实验四：双阈值语义去重",
    "date": datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    ),
    "low_threshold": LOW_THRESHOLD,
    "high_threshold": HIGH_THRESHOLD,
    "original_count": len(texts),
    "automatic_filtered_count": len(high_confidence),
    "manual_review_count": len(manual_review),
    "kept_count": len(kept),
    "true_positive": true_positive,
    "false_positive": false_positive,
    "false_negative": false_negative,
    "precision": precision,
    "recall": recall,
    "f1_score": f1,
    "details": details
}

with open(
    save_dir / "experiment_04.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        summary,
        f,
        ensure_ascii=False,
        indent=4
    )

print("\n========== 实验四完成 ==========")

print("详细结果：results/experiment_04_details.csv")
print("完整数据：results/experiment_04.json")
