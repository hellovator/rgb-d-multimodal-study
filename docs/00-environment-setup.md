# 环境配置记录

硬件：GPU ___ ｜ 显存 ___ ｜ 系统 ___
日期：2026-__-__

| # | 步骤 | 命令 | 结果 | 备注/坑 |
|---|------|------|------|---------|
| 1 | 装 Miniconda | | ✅/❌ | |
| 2 | conda 建环境 | conda create -n dformer python=3.10 | | |
| 3 | PyTorch+CUDA | conda install pytorch==2.1.2 ... | | |
| 4 | mmcv | pip install mmcv==2.1.0 -f <官方索引> | | |
| 5 | 其余依赖 | | | |
| 6 | semhash | pip install semhash sentence-transformers | | |
