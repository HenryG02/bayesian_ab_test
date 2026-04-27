# Importing necessary stuff
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from src.generate_dataset import generate_ab_data
from src.inference import (
    calculate_posterior,
    generate_posterior_dataframe,
    calculate_probability_better,
    calculate_expected_loss,
    monte_carlo_simulation,
)

# Title and sidebar
st.title("Bayesian A/B Test")
with st.sidebar:
    st.header("Parameters")
    true_prob_rate_a = st.slider("True probability rate for variant A", 0.01, 0.99)
    true_prob_rate_b = st.slider("True probability rate for variant B", 0.01, 0.99)
    sample_size = st.slider("Sample size", 100, 5000)


# Defining function to generate "true" data and cache it
@st.cache_data
def generate_data_cached(
    prob_rate_a: float, prob_rate_b: float, sample_size: int
) -> pd.DataFrame:
    """
    Generate data for A/B test to be cached
    """
    return generate_ab_data(
        n_a=sample_size, n_b=sample_size, rate_a=prob_rate_a, rate_b=prob_rate_b
    )


# Generating data
generated_df = generate_data_cached(true_prob_rate_a, true_prob_rate_b, sample_size)

# Analysis of generated data
st.header("Generated data analysis")
st.subheader("Table with counts of conversions by variant")
st.dataframe(
    pd.crosstab(generated_df["group"], generated_df["converted"]).rename(
        columns={0: "not converted", 1: "converted"}
    )
)

fig = px.histogram(
    generated_df,
    x="group",
    color=generated_df["converted"].astype(str),
    barmode="group",
    text_auto=True,
    labels={"color": "Converted"},
    title="Count of Conversions by Variant",
)
st.plotly_chart(fig)

# Analysis of posterior distribution
st.header("Making inferences")

posterior_alpha_a, posterior_beta_a = calculate_posterior(
    alpha=1,
    beta=1,
    num_conversions=generated_df[generated_df["group"] == "A"]["converted"].sum(),
    num_observations=generated_df[generated_df["group"] == "A"].shape[0],
)
posterior_alpha_b, posterior_beta_b = calculate_posterior(
    alpha=1,
    beta=1,
    num_conversions=generated_df[generated_df["group"] == "B"]["converted"].sum(),
    num_observations=generated_df[generated_df["group"] == "B"].shape[0],
)


# Defining function to generate DataFrame from the posterior distributions and to cache it
@st.cache_data
def generate_posterior_dataframe_cached(
    posterior_alpha_a: float,
    posterior_beta_a: float,
    posterior_alpha_b: float,
    posterior_beta_b: float,
    bins: int,
) -> pd.DataFrame:
    """
    Generate posterior dataframe to be cached
    """
    return generate_posterior_dataframe(
        posterior_alpha_a, posterior_beta_a, posterior_alpha_b, posterior_beta_b, bins
    )


posterior_df = generate_posterior_dataframe_cached(
    posterior_alpha_a, posterior_beta_a, posterior_alpha_b, posterior_beta_b, 1000
)

# Making plots
st.subheader("Posterior distribution for each variant")
fig = px.line(posterior_df, x="Conversion rate", y="Density", color="Variant")
st.plotly_chart(fig)


# Defining function to generate samples from the posterior distributions and to cache it
@st.cache_data
def monte_carlo_simulation_cached(
    posterior_alpha_a: float,
    posterior_beta_a: float,
    posterior_alpha_b: float,
    posterior_beta_b: float,
    num_samples: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Function that generate samples from the posterior distributions and caches it
    """
    return monte_carlo_simulation(
        posterior_alpha_a,
        posterior_beta_a,
        posterior_alpha_b,
        posterior_beta_b,
        num_samples,
    )


posterior_samples_a, posterior_samples_b = monte_carlo_simulation_cached(
    posterior_alpha_a, posterior_beta_a, posterior_alpha_b, posterior_beta_b, 50000
)

# Displaying metrics
st.metric(
    "Probability of variant B being better than variant A",
    calculate_probability_better(posterior_samples_a, posterior_samples_b),
    format="%.4f",
)

st.metric(
    "Expected loss of choosing variant B when variant A is actually better",
    calculate_expected_loss(posterior_samples_a, posterior_samples_b),
    format="%.4f",
)
