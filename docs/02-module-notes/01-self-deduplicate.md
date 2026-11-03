# SemHash 核心模块阅读笔记（一）

## 1. 阅读文件

文件名称：semhash.py

核心函数：self_deduplicate()

## 2. 函数作用

self_deduplicate() 用于对同一数据集内部的数据进行语义去重。

其主要思路是利用文本向量和相似度阈值寻找相似邻居，并将相关数据组织成去重结果。

## 3. 核心参数

| 参数 | 含义 |
|---|---|
| self | 当前 SemHash 对象 |
| threshold | 相似度阈值，默认 0.9 |

## 4. 核心执行过程

### 第一步：寻找相似邻居

```python
neighbors = self.index.query_threshold(
    self.index.vectors,
    threshold=threshold
)
```

利用索引中的向量，根据设定阈值查询相似邻居。

### 第二步：获取数据分组

```python
groups = self.index.items
```

获取索引中存储的数据项。

### 第三步：处理字符串格式

```python
if self._was_string:
    groups = [
        [dict_to_string(record, self.columns) for record in group]
        for group in groups
    ]
```

当原始数据为字符串时，将数据转换回字符串形式。

### 第四步：生成去重结果

```python
return DeduplicationResult._from_groups(
    groups=groups,
    neighbors=neighbors,
    vectors=self.index.vectors,
    threshold=threshold,
    columns=self.columns
)
```

将分组、邻居信息、向量和阈值传入结果构造函数。

## 5. 初步理解

该函数本身并没有直接实现完整的向量相似度计算，而是调用索引对象中的 query_threshold() 完成邻居查询。

因此，后续需要继续阅读：

1. index.py 中的 query_threshold()
2. semhash.py 中的 _from_groups()
3. DeduplicationResult 的定义

## 6. 待研究问题

1. 文本向量具体由什么模型生成？
2. query_threshold() 使用什么相似度计算方式？
3. 两条文本之间的相似度如何计算？
4. 当多个文本互相相似时，SemHash 如何决定保留哪条？
5. threshold 对最终去重结果有什么影响？

## 7. 当前结论

已经初步理解 SemHash 的核心去重入口，下一阶段重点研究向量索引、相似邻居查询和结果分组机制。
