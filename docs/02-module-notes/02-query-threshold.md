# SemHash 核心模块阅读笔记（二）

## 1. 阅读函数

函数名称：query_threshold()

所在模块：index.py

## 2. 函数作用

根据输入的文本向量和相似度阈值，查询满足条件的相似邻居。

返回每个查询向量对应的邻居索引和余弦相似度分数。

## 3. 核心参数

| 参数 | 含义 |
|---|---|
| self | 当前索引对象 |
| vectors | 输入的向量数组 |
| threshold | 相似度阈值 |

## 4. 核心执行过程

### 第一步：执行底层索引查询

调用：

```python
self.backend.threshold()
```

根据距离阈值查找相似向量。

### 第二步：相似度与距离转换（对数学公式的表示）

\begin{align}
\text{余弦相似度：}\quad & s = \cos\theta \\
\text{余弦距离：}\quad & d = 1 - s
\end{align}

代码：

```python
threshold=1 - threshold
```

将相似度阈值转换成余弦距离阈值。

代码：

```python
1 - distances
```

将底层返回的距离转换成相似度。

### 第三步：检查邻居数量上限

利用 enumerate() 遍历查询结果，找出邻居数量达到 NEIGHBORS_PER_QUERY 上限的查询项。

### 第四步：扩大查询范围

对于达到数量上限的查询项，使用 MAX_NEIGHBORS 进行重新查询，并替换原来的查询结果。

### 第五步：返回结果

返回 neighbors 列表，包含邻居索引和对应的相似度。
（邻居（neighbor） = 和当前查询向量相似、命中门槛的向量；邻居索引（neighbor indices / indices）就是这些邻居在向量库里面的编号。）

## 5. 初步理解

query_threshold() 并不直接删除重复文本，而是负责寻找满足相似度条件的邻居。

它还设计了邻居数量上限检查机制，以减少密集相似文本集合被初次查询截断的情况。

## 6. 待研究问题

1. NEIGHBORS_PER_QUERY 和 MAX_NEIGHBORS 分别是多少？
2. backend.threshold() 底层采用什么索引算法？
3. 邻居之间是否需要双向相似？
4. 多条相似文本最终如何分组？
5. SemHash 如何选择最终保留的文本？

## 7. 当前结论

已经初步理解 SemHash 从向量索引中查询相似邻居的过程，下一步继续研究邻居分组和最终结果筛选机制。
