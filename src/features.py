import numpy as np
import pandas as pd

from src.utils import assert_columns


ROUND_DECIMALS = 3

EMISSIONS_TRADE_REQUIRED = [
    "consumption_co2_per_capita",
    "co2_per_capita",
]

WELLBEING_EFFICIENCY_REQUIRED = [
    "happiness_index",
    "co2_per_capita",
    "consumption_co2_per_capita",
    "material_footprint_per_capita",
    "energy_per_capita",
]

INEQUALITY_ADJUSTED_REQUIRED = [
    "happiness_index",
    "gini_index",
    "co2_per_capita",
    "consumption_co2_per_capita",
    "material_footprint_per_capita",
    "energy_per_capita",
]

ENERGY_INTENSITY_REQUIRED = [
    "co2_per_capita",
    "material_footprint_per_capita",
    "energy_per_capita",
]


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


def round_feature(series: pd.Series, decimals: int = ROUND_DECIMALS) -> pd.Series:
    """
    Round a feature series to a fixed number of decimal places.
    """
    return series.round(decimals)


def add_emissions_trade_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add features comparing consumption-based and production-based CO2 emissions.
    """
    assert_columns(df, EMISSIONS_TRADE_REQUIRED)

    df = df.copy()

    df["co2_consumption_production_gap"] = round_feature(
        df["consumption_co2_per_capita"] - df["co2_per_capita"]
    )

    df["co2_consumption_production_ratio"] = round_feature(
        safe_divide(
            df["consumption_co2_per_capita"],
            df["co2_per_capita"],
        )
    )

    return df


def add_wellbeing_efficiency_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add wellbeing efficiency features.

    These measure how much reported wellbeing is achieved per unit of
    environmental or resource pressure.
    """
    assert_columns(df, WELLBEING_EFFICIENCY_REQUIRED)

    df = df.copy()

    df["happiness_per_co2"] = round_feature(
        safe_divide(
            df["happiness_index"],
            df["co2_per_capita"],
        )
    )

    df["happiness_per_consumption_co2"] = round_feature(
        safe_divide(
            df["happiness_index"],
            df["consumption_co2_per_capita"],
        )
    )

    df["happiness_per_material_footprint"] = round_feature(
        safe_divide(
            df["happiness_index"],
            df["material_footprint_per_capita"],
        )
    )

    df["happiness_per_1000_energy"] = round_feature(
    safe_divide(
        df["happiness_index"],
        df["energy_per_capita"],
    )
    * 1000
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
    assert_columns(df, INEQUALITY_ADJUSTED_REQUIRED)

    df = df.copy()

    df["inequality_adjusted_happiness"] = round_feature(
        df["happiness_index"] * (1 - df["gini_index"] / 100)
    )

    df["ineq_adj_happiness_per_co2"] = round_feature(
        safe_divide(
            df["inequality_adjusted_happiness"],
            df["co2_per_capita"],
        )
    )

    df["ineq_adj_happiness_per_consumption_co2"] = round_feature(
        safe_divide(
            df["inequality_adjusted_happiness"],
            df["consumption_co2_per_capita"],
        )
    )

    df["ineq_adj_happiness_per_material_footprint"] = round_feature(
        safe_divide(
            df["inequality_adjusted_happiness"],
            df["material_footprint_per_capita"],
        )
    )

    df["ineq_adj_happiness_per_1000_energy"] = round_feature(
    safe_divide(
        df["inequality_adjusted_happiness"],
        df["energy_per_capita"],
    )
    * 1000
    )

    return df


def add_energy_intensity_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add energy-related environmental intensity features.

    These are diagnostic/contextual features rather than direct wellbeing
    efficiency measures.

    The ratios are scaled per 1,000 units of energy use because
    energy_per_capita is measured on a much larger numerical scale than
    CO2 per capita or material footprint per capita.
    """
    assert_columns(df, ENERGY_INTENSITY_REQUIRED)

    df = df.copy()

    df["co2_per_1000_energy"] = round_feature(
        safe_divide(
            df["co2_per_capita"],
            df["energy_per_capita"],
        )
        * 1000
    )

    df["material_footprint_per_1000_energy"] = round_feature(
        safe_divide(
            df["material_footprint_per_capita"],
            df["energy_per_capita"],
        )
        * 1000
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
