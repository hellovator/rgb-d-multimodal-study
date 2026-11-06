import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 中文显示设置
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei"
]
plt.rcParams["axes.unicode_minus"] = False

# 文件路径
result_dir = Path("results")
chart_dir = result_dir / "charts"
chart_dir.mkdir(exist_ok=True)

# 读取实验数据
df2 = pd.read_csv(
    result_dir / "threshold_summary.csv"
)

df3 = pd.read_csv(
    result_dir / "experiment_03_summary.csv"
)

# ==================================
# 图1：阈值对重复率的影响
# ==================================

plt.figure(figsize=(8, 5))

plt.plot(
    df2["threshold"],
    df2["duplicate_ratio"],
    marker="o",
    label="重复率"
)

plt.xlabel("相似度阈值")
plt.ylabel("重复率")
plt.title("不同阈值下 SemHash 的重复率变化")
plt.grid(True)
plt.legend()

plt.savefig(
    chart_dir / "01_threshold_duplicate_ratio.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==================================
# 图2：Precision、Recall、F1 对比
# ==================================

plt.figure(figsize=(8, 5))

plt.plot(
    df3["threshold"],
    df3["precision"],
    marker="o",
    label="Precision"
)

plt.plot(
    df3["threshold"],
    df3["recall"],
    marker="s",
    label="Recall"
)

plt.plot(
    df3["threshold"],
    df3["f1_score"],
    marker="^",
    label="F1-score"
)

plt.xlabel("相似度阈值")
plt.ylabel("评价指标")
plt.title("不同阈值下的去重性能评价")
plt.ylim(0, 1.05)
plt.grid(True)
plt.legend()

plt.savefig(
    chart_dir / "02_evaluation_metrics.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==================================
# 图3：误删与漏检数量
# ==================================

plt.figure(figsize=(8, 5))

plt.plot(
    df3["threshold"],
    df3["false_positive"],
    marker="o",
    label="误删数量"
)

plt.plot(
    df3["threshold"],
    df3["false_negative"],
    marker="s",
    label="漏检数量"
)

plt.xlabel("相似度阈值")
plt.ylabel("文本数量")
plt.title("不同阈值下的误删与漏检情况")
plt.grid(True)
plt.legend()

plt.savefig(
    chart_dir / "03_error_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("================================")
print("实验图表生成完成！")
print("保存位置：results/charts/")
print("================================")