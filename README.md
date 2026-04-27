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

## 4. Running the App
To run the app locally, use the following command:

```bash
uv run streamlit run src/frontend.py
```

## 5. Insights and Analysis
Once the app is running, you can interact with the sliders to simulate different scenarios and observe how the Bayesian inference updates the posterior distributions of the conversion rates for each variant.

## 6. Why Bayesian A/B testing?
Bayesian A/B testing is a statistical method used to compare two or more variants to identify which one performs better based on collected data. 

In traditional, frequentist A/B testing, we calculate p-values and confidence intervals to determine statistical significance. However, they are difficult to interpret as they are based on hypotetical resampling of the data. For the 95% confidence interval, for example, the correct interpretation is: if we were to repeat the experiment many times, 95% of the calculated confidence intervals would contain the true value.

On the other hand, Bayesian A/B testing is more intuitive, since it allows for the direct calculation of the probability that one variant is better than the other, which is more easily understood by business stakeholders and that was the main reason for choosing this approach for this project.

## 7. References
- WAKEFIELD, J. **Bayesian and Frequentist Regression Methods** (2013), Springer

