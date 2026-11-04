# SemHash 核心模块阅读笔记（三）：_from_groups()

## 1. 所在位置

文件：datamodels.py

函数：DeduplicationResult._from_groups()

## 2. 函数作用

根据文本分组、相似邻居和向量信息，构建最终的去重结果。

主要包括：
- 选择保留的代表文本。
- 记录被过滤的文本。
- 建立重复文本与代表文本之间的对应关系。
- 保存后续重新筛选所需的数据。

## 3. 核心执行过程

### 第一步：创建结果对象

```python
result = cls(threshold=threshold, columns=columns)
```

创建 DeduplicationResult 对象。

### 第二步：选择代表文本

```python
canonicals = select_canonicals(
    vectors=vectors,
    neighbors=neighbors,
    threshold=threshold
)
```

调用 select_canonicals()，根据向量、邻居和阈值选择代表文本。

### 第三步：遍历分组

```python
for i, (group, (canonical, score)) in enumerate(zip(groups, canonicals)):
```

遍历每个分组，同时获取代表文本编号和相似度分数。

### 第四步：判断是否保留

```python
is_selected = canonical == i
```

如果当前分组编号等于代表文本编号，则当前分组被选中。

### 第五步：保存代表文本

```python
if is_selected:
    result.selected.append(group[0])
```

将被选中分组的第一条记录加入保留列表。

### 第六步：确定被过滤的文本

```python
filtered_records = group[1:] if is_selected else group
```

如果当前分组被选中，则过滤第一条以外的记录；否则过滤整个分组。

### 第七步：建立重复关系

```python
DuplicateRecord(
    record=record,
    exact=is_selected,
    duplicate_of=groups[canonical][0],
    score=score
)
```

记录被过滤文本、是否属于组内完全重复、对应代表文本和相似度分数。

### 第八步：保存选择输入并返回

```python
result._selection_inputs = (groups, neighbors, vectors)
return result
```

保存后续重新筛选所需的数据，并返回最终结果。

## 4. 关键知识点

| 名称 | 作用 |
|---|---|
| canonical | 代表文本的分组编号 |
| score | 对应的相似度分数 |
| is_selected | 判断当前分组是否被选中 |
| selected | 保留的文本 |
| filtered | 被过滤的文本 |
| exact | 是否属于代表组内部的完全重复记录 |
| duplicate_of | 当前重复文本对应的代表文本 |

## 5. 阶段性理解

SemHash 的去重过程不仅需要判断文本是否相似，还需要选择代表文本，并记录被过滤文本与代表文本之间的关系。

目前已经初步理解：
1. query_threshold()：查询相似邻居。
2. self_deduplicate()：组织整体去重流程。
3. _from_groups()：构建最终去重结果。

## 6. 待研究问题

1. select_canonicals() 具体如何选择代表文本？
2. 代表文本的选择是否受到文本顺序影响？
3. 多个文本互相相似时，如何确定代表文本？
4. 修改 threshold 后，代表文本会不会发生变化？
5. 能否改进代表文本选择策略？
