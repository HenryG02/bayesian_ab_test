# bayesian_ab_test

## 1. Project Summary
This project aims to apply Bayesian A/B testing to compare two versions of a fictional website, A and B, and determine which one is better.

## 2. Configuration
This project uses uv as the dependency manager. To install dependencies, run the following command:

```bash
uv sync
```

To run commands, you use the following syntax:
```bash
uv run example.py
```

## 3. Dataset Generation
A synthetic dataset will be used throughout the project. The code to generate it is in the file `src/generate_dataset.py`. The dataset will be stored in the file `data/ab_test_data.csv`. You should run the aforementioned script first before running any other script in the project.

