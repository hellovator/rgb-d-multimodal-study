# RGB-D Multimodal Study

**A Research-Oriented Study of Semantic Deduplication and RGB-D Multimodal Learning**

## 1. Project Overview

This repository records an undergraduate research project focused on semantic text deduplication and RGB-D multimodal learning.

The initial stage uses SemHash as an entry point to understand semantic similarity, text embeddings, threshold-based deduplication, and evaluation strategies.

The project subsequently explores RGB-D semantic segmentation through the study of DFormer.

## 2. Experimental Environment

| Component | Configuration |
|---|---|
| Operating System | Windows |
| Python | 3.10 |
| Environment Management | Conda |
| Semantic Deduplication Framework | SemHash |
| Memory | 16 GB |
| GPU | No NVIDIA discrete GPU |

## 3. SemHash Experiments

### Experiment 1: Basic Semantic Deduplication

Reproduced the basic SemHash workflow and explored semantic duplicate identification.

### Experiment 2: Similarity Threshold Analysis

Investigated how different similarity thresholds affect the number of retained and filtered texts.

Tested thresholds: `0.5, 0.6, 0.7, 0.8, 0.9, 0.95`.

### Experiment 3: Evaluation on a Manually Annotated Dataset

Evaluated semantic deduplication using Precision, Recall, and F1-score.

The experiments showed that lower thresholds generally improve recall, while higher thresholds improve precision.

### Experiment 4: Dual-Threshold Strategy

Introduced two thresholds to divide candidate duplicates into:

- High-confidence duplicates for automatic filtering.
- Medium-confidence candidates for manual review.
- Other texts retained.

This preliminary experiment explored a more cautious deduplication workflow.

### Experiment 5: Error Analysis and Evaluation

Extended the evaluation with additional error analysis and metric visualizations.

The experiment examined the relationship between threshold selection and false-positive and false-negative predictions.

### Experiment 6: Data Quality Audit and Pair-Level Evaluation

Conducted a more detailed evaluation using a manually annotated dataset of 100 text pairs.

At threshold 0.5, the results were:

| Metric | Result |
|---|---:|
| Correct predictions | 61 |
| False positives | 38 |
| False negatives | 1 |
| Accuracy | 61.00% |
| Precision | 50.65% |
| Recall | 97.50% |
| F1-score | 66.10% |

The error analysis identified two important challenges:

1. Partial-overlap texts may be incorrectly classified as duplicates.
2. Texts with similar topics but different factual details may receive high similarity scores.

These findings suggest that semantic similarity alone may not be sufficient for reliable deduplication.

The experiment also highlights the importance of data quality, annotation consistency, and threshold selection.

**Note:** These results are preliminary and are based on a small manually constructed dataset. They should not be interpreted as general performance benchmarks.

## 4. Repository Structure

```text
rgb-d-multimodal-study/
├── data/
│   └── semhash_pair_dataset.csv
├── docs/
│   ├── 02-module-notes/
│   ├── 00-environment-setup.md
│   ├── 03-reproduce.md
│   ├── 04-experiment-log.md
│   └── experiment_06_annotation.md
├── results/
│   ├── charts/
│   ├── experiment_02.*
│   ├── experiment_03.*
│   ├── experiment_04.*
│   ├── experiment_05_*
│   └── experiment_06_*
├── semhash_demo.py
├── semhash_experiment_04.py
├── semhash_experiment_06_audit.py
├── semhash_experiment_06_error_analysis.py
├── semhash_experiment_06_pair_evaluation.py
├── semhash_plot.py
└── README.md
```

## 5. Current Research Progress

- [x] Configure Python and Conda environments.
- [x] Install and run SemHash.
- [x] Reproduce basic semantic deduplication.
- [x] Conduct similarity threshold experiments.
- [x] Implement a preliminary dual-threshold strategy.
- [x] Perform error analysis and metric evaluation.
- [x] Conduct data quality auditing and pair-level evaluation.
- [x] Organize experimental code, data, documentation, and visualizations.
- [x] Upload initial experimental results to GitHub.
- [ ] Expand the evaluation dataset.
- [ ] Investigate improved semantic deduplication strategies.
- [ ] Continue studying DFormer and RGB-D semantic segmentation.

## 6. Future Research Directions

1. Expand the manually annotated evaluation dataset.
2. Investigate adaptive similarity thresholds.
3. Explore methods for identifying factual conflicts and partial information overlap.
4. Compare different embedding models and deduplication strategies.
5. Study RGB-D multimodal representation learning and semantic segmentation using DFormer.

## 7. Notes

This repository documents an ongoing undergraduate research project.

The SemHash experiments are preliminary explorations intended to develop practical skills in source-code analysis, experimental reproduction, quantitative evaluation, and error analysis.

The later research stage focuses on understanding RGB-D multimodal semantic segmentation and exploring potential improvements based on existing research.

---

**Project Status:** Ongoing research and experimental exploration.

**Research Path:** SemHash Semantic Deduplication → Error Analysis and Evaluation → RGB-D Multimodal Learning.
