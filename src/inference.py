# Script for inference and analytical functions

# Importing necessary libraries
import pandas as pd
import numpy as np
from scipy.stats import beta


def calculate_posterior(
    alpha: float, beta: float, num_conversions: int, num_observations: int
) -> tuple[float, float]:
    """
    Calculates the posterior distribution given:
    Args:
    - alpha: prior alpha parameter value
    - beta: prior beta parameter value
    - num_conversions: number of conversions for the variant
    - num_observations: number of observations for the variant

    Returns:
    tuple[float, float]: posterior alpha and beta parameter values
    """
    posterior_alpha = alpha + num_conversions
    posterior_beta = beta + num_observations - num_conversions
    return posterior_alpha, posterior_beta


def generate_posterior_dataframe(
    posterior_alpha_a: float,
    posterior_beta_a: float,
    posterior_alpha_b: float,
    posterior_beta_b: float,
    bins: int = 1000,
) -> pd.DataFrame:
    """
    Creates a pandas DataFrame to plot the posterior's probability
    density functions with 'bins' number of values.

    Args:
    - posterior_alpha_a: posterior alpha parameter value for variant A
    - posterior_beta_a: posterior beta parameter value for variant A
    - posterior_alpha_b: posterior alpha parameter value for variant B
    - posterior_beta_b: posterior beta parameter value for variant B
    - bins: number of bins to use for the posterior distribution

    Returns:
    pd.DataFrame: DataFrame with the posterior's probability density functions values to plot
    """
    # Creating range of values between 0 and 1 for the posterior distribution
    x_values = np.linspace(0, 1, bins)
    posterior_a_values = beta.pdf(x_values, a=posterior_alpha_a, b=posterior_beta_a)
    posterior_b_values = beta.pdf(x_values, a=posterior_alpha_b, b=posterior_beta_b)

    # Creating and returning DataFrame
    return pd.DataFrame(
        {
            "Conversion rate": np.concatenate([x_values, x_values]),
            "Density": np.concatenate([posterior_a_values, posterior_b_values]),
            "Variant": ["A"] * bins + ["B"] * bins,
        }
    )


def monte_carlo_simulation(
    posterior_alpha_a: float,
    posterior_beta_a: float,
    posterior_alpha_b: float,
    posterior_beta_b: float,
    num_samples: int = 10000,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Performs a Monte Carlo simulation to generate 'num_samples' random values
    from the posterior distribution for both variants.

    Args:
    - posterior_alpha_a: posterior alpha parameter value for variant A
    - posterior_beta_a: posterior beta parameter value for variant A
    - posterior_alpha_b: posterior alpha parameter value for variant B
    - posterior_beta_b: posterior beta parameter value for variant B
    - num_samples: number of samples to use for the simulation

    Returns:
    list[np.ndarray, np.ndarray]: list containing the posterior samples for variant A and variant B
    """
    # Drawing samples from the posterior distribution
    samples_a = beta.rvs(a=posterior_alpha_a, b=posterior_beta_a, size=num_samples)
    samples_b = beta.rvs(a=posterior_alpha_b, b=posterior_beta_b, size=num_samples)

    return samples_a, samples_b


def calculate_probability_better(samples_a: np.ndarray, samples_b: np.ndarray) -> float:
    """
    Calculates the probability of variant B being better than variant A
    """
    return np.mean(samples_b > samples_a)


def calculate_expected_loss(samples_a: np.ndarray, samples_b: np.ndarray) -> float:
    """
    Calculates the expected loss of variant B being better than variant A. In other words,
    it calculates a measure of how much we would lose on average if we choose variant B
    when variant A is actually better.
    """
    return np.mean(np.maximum(samples_a - samples_b, 0))
