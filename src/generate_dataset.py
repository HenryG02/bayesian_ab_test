import pandas as pd
import numpy as np


def generate_ab_data(n_a=1000, n_b=1000, rate_a=0.12, rate_b=0.15, seed=42):
    np.random.seed(seed)

    data_a = np.random.binomial(1, rate_a, n_a)
    data_b = np.random.binomial(1, rate_b, n_b)

    df_a = pd.DataFrame({"group": "A", "converted": data_a})
    df_b = pd.DataFrame({"group": "B", "converted": data_b})

    return pd.concat([df_a, df_b]).reset_index(drop=True)


# Gerando e salvando
df = generate_ab_data()
df.to_csv("data/ab_test_data.csv", index=False)
