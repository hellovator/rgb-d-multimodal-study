# SemHash 核心模块阅读笔记（四）：select_canonicals()

## 1. 函数位置

文件：utils.py

函数：select_canonicals()

作用：按照输入顺序贪心选择代表文本，并为其他文本分配对应的代表文本编号。

## 2. 输入与输出

输入：
- vectors：每条文本对应的向量。
- neighbors：每条文本的相似邻居及其相似度。
- threshold：相似度阈值。

输出：
- 每条文本对应的代表文本编号。
- 每条文本与代表文本之间的相似度。

## 3. 核心执行过程

### 第一步：向量归一化

```python
unit_vectors = normalize(vectors)
```

将文本向量归一化，为后续余弦相似度计算做准备。

### 第二步：初始化变量

```python
canonical_indices = np.empty(len(neighbors), dtype=np.int64)
selected_indices = []
canonicals = []
```

- canonical_indices：记录每条文本对应的代表编号。
- selected_indices：记录已经选中的代表文本。
- canonicals：保存最终代表编号和相似度。

### 第三步：定义 closest()

```python
scores = unit_vectors[candidates] @ unit_vectors[i]
best = int(np.argmax(scores))
```

计算当前文本与候选代表的余弦相似度，并找到最相似的候选。

如果最高相似度达到 threshold，就返回候选编号和相似度，否则返回 None。

### 第四步：筛选相似邻居

```python
matches = indices[scores >= threshold]
```

保留相似度达到阈值的邻居。

### 第五步：寻找之前选中的代表

```python
best_match = closest(
    i,
    np.unique(canonical_indices[matches[matches < i]])
)
```

只考虑已经处理过的邻居，并将它们转换为对应的代表编号，避免传递性匹配。

### 第六步：特殊情况处理

```python
if best_match is None and len(matches) >= MAX_NEIGHBORS:
    best_match = closest(i, np.array(selected_indices))
```

当邻居数量达到上限且没有找到合适代表时，直接与所有已选代表进行比较。

### 第七步：选择代表或归属已有代表

```python
if best_match is None:
    selected_indices.append(i)
    best_match = (i, 1.0)
```

如果没有找到合适的代表，就将当前文本选为新代表。

### 第八步：记录最终结果

```python
canonical_indices[i] = best_match[0]
canonicals.append(best_match)
```

记录当前文本对应的代表编号和相似度。

最后返回：

```python
return canonicals
```

## 4. 关键知识点

| 名称 | 作用 |
|---|---|
| normalize() | 向量归一化 |
| closest() | 找到最相似的候选代表 |
| np.argmax() | 找到最大值的位置 |
| np.unique() | 去除重复元素 |
| np.empty() | 创建未初始化数组 |
| selected_indices | 已选代表编号 |
| canonical_indices | 每条文本对应的代表编号 |
| MAX_NEIGHBORS | 邻居查询数量上限 |

## 5. 算法特点

1. 按照输入顺序进行贪心选择。
2. 只有达到相似度阈值的文本才会归入已有代表。
3. 当前文本与已选代表进行直接相似度比较。
4. 没有找到合适代表时，当前文本成为新代表。
5. 每条被处理的文本都会得到一个代表编号。

## 6. 值得研究的问题

1. 输入顺序是否影响最终去重结果？
2. 不同阈值下，保留文本数量有什么变化？
3. 能否使用其他代表选择策略改善去重效果？
4. 当前贪心策略在高密度相似文本数据中表现如何？

## 7. 阶段性总结

目前已经阅读：
- index.py：query_threshold()
- semhash.py：self_deduplicate()
- datamodels.py：_from_groups()
- utils.py：select_canonicals()

初步理解了 SemHash 从相似邻居查询、代表文本选择到最终去重结果构建的主要流程。
