import pandas as pd
import numpy as np
import os


def generate_ab_data(
    n_a: int = 1000,
    n_b: int = 1000,
    rate_a: float = 0.12,
    rate_b: float = 0.15,
    seed: int = 42,
) -> pd.DataFrame:
    """
    This functions generates a synthetic dataset for A/B testing.

    Args:
      - n_a, n_b (float): Number of samples for groups A and B, respectively;
      - rate_a, rate_b (float): Conversion rates for groups A and B, respectively;
      - seed (int): Seed for reproducibility.

    Returns:
      - pd.DataFrame: DataFrame with columns ["group", "converted"] in which
        0 indicates no conversion and 1 indicates conversion
    """
    np.random.seed(seed)

    data_a = np.random.binomial(1, rate_a, n_a)
    data_b = np.random.binomial(1, rate_b, n_b)

    df_a = pd.DataFrame({"group": "A", "converted": data_a})
    df_b = pd.DataFrame({"group": "B", "converted": data_b})

    return pd.concat([df_a, df_b]).reset_index(drop=True)


# Generating and saving synthetic dataset
if __name__ == "__main__":
    df = generate_ab_data()
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/ab_test_data.csv", index=False)
