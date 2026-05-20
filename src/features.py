import numpy as np
import pandas as pd

from src.utils import assert_columns


def safe_divide(
    numerator: pd.Series,
    denominator: pd.Series,
) -> pd.Series:
    """
    Safely divide two numeric series.

    Returns NaN where the denominator is missing or zero.
    """
    return pd.Series(
        np.where(
            denominator.notna() & (denominator != 0),
            numerator / denominator,
            np.nan,
        ),
        index=numerator.index,
    )


def add_emissions_trade_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add features comparing consumption-based and production-based CO2 emissions.
    """
    assert_columns(
        df,
        [
            "consumption_co2_per_capita",
            "co2_per_capita",
        ],
    )

    df = df.copy()

    df["co2_consumption_production_gap"] = (
        df["consumption_co2_per_capita"] - df["co2_per_capita"]
    )

    df["co2_consumption_production_ratio"] = safe_divide(
        df["consumption_co2_per_capita"],
        df["co2_per_capita"],
    )

    return df


def add_wellbeing_efficiency_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add wellbeing efficiency features.

    These measure how much reported wellbeing is achieved per unit of
    environmental or resource pressure.
    """
    assert_columns(
        df,
        [
            "happiness_index",
            "co2_per_capita",
            "consumption_co2_per_capita",
            "material_footprint_per_capita",
            "energy_per_capita",
        ],
    )

    df = df.copy()

    df["happiness_per_co2"] = safe_divide(
        df["happiness_index"],
        df["co2_per_capita"],
    )

    df["happiness_per_consumption_co2"] = safe_divide(
        df["happiness_index"],
        df["consumption_co2_per_capita"],
    )

    df["happiness_per_material_footprint"] = safe_divide(
        df["happiness_index"],
        df["material_footprint_per_capita"],
    )

    df["happiness_per_energy"] = safe_divide(
        df["happiness_index"],
        df["energy_per_capita"],
    )

    return df


def add_inequality_adjusted_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add inequality-adjusted wellbeing and corresponding efficiency features.

    The inequality adjustment is exploratory and defined as:

        happiness_index * (1 - gini_index / 100)

    It should be interpreted as a project-specific constructed indicator,
    not as an official wellbeing measure.
    """
    assert_columns(
        df,
        [
            "happiness_index",
            "gini_index",
            "co2_per_capita",
            "consumption_co2_per_capita",
            "material_footprint_per_capita",
            "energy_per_capita",
        ],
    )

    df = df.copy()

    df["inequality_adjusted_happiness"] = (
        df["happiness_index"] * (1 - df["gini_index"] / 100)
    )

    df["ineq_adj_happiness_per_co2"] = safe_divide(
        df["inequality_adjusted_happiness"],
        df["co2_per_capita"],
    )

    df["ineq_adj_happiness_per_consumption_co2"] = safe_divide(
        df["inequality_adjusted_happiness"],
        df["consumption_co2_per_capita"],
    )

    df["ineq_adj_happiness_per_material_footprint"] = safe_divide(
        df["inequality_adjusted_happiness"],
        df["material_footprint_per_capita"],
    )

    df["ineq_adj_happiness_per_energy"] = safe_divide(
        df["inequality_adjusted_happiness"],
        df["energy_per_capita"],
    )

    return df


def add_energy_intensity_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add energy-related environmental intensity features.

    These are diagnostic/contextual features rather than direct wellbeing
    efficiency measures.
    """
    assert_columns(
        df,
        [
            "co2_per_capita",
            "material_footprint_per_capita",
            "energy_per_capita",
        ],
    )

    df = df.copy()

    df["co2_per_energy"] = safe_divide(
        df["co2_per_capita"],
        df["energy_per_capita"],
    )

    df["material_footprint_per_energy"] = safe_divide(
        df["material_footprint_per_capita"],
        df["energy_per_capita"],
    )

    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build analytical features for the EDA stage.
    """
    df = df.copy()

    df = add_emissions_trade_features(df)
    df = add_wellbeing_efficiency_features(df)
    df = add_inequality_adjusted_features(df)
    df = add_energy_intensity_features(df)

    return df