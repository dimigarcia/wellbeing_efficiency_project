import pandas as pd


ROUND_DECIMALS = 3


PERCENTILE_REQUIRED = [
    "year",
    "happiness_index",
    "consumption_co2_per_capita",
    "material_footprint_per_capita",
]

FLAG_REQUIRED = [
    "happiness_percentile_by_year",
    "consumption_co2_percentile_by_year",
    "material_footprint_percentile_by_year",
]


def add_year_relative_percentiles(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add year-relative percentile indicators.

    These features compare each country to other countries within the
    same year rather than across the pooled dataset.

    Percentiles are bounded between 0 and 1.

    Interpretation
    --------------
    - Higher happiness percentiles indicate higher wellbeing relative
      to other countries in the same year.

    - Higher consumption CO2 and material footprint percentiles indicate
      higher environmental/material pressure relative to other countries
      in the same year.
    """

    missing = [
        c for c in PERCENTILE_REQUIRED
        if c not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    df = df.copy()

    df["happiness_percentile_by_year"] = (
        df.groupby("year")["happiness_index"]
        .rank(pct=True)
        .round(ROUND_DECIMALS)
    )

    df["consumption_co2_percentile_by_year"] = (
        df.groupby("year")["consumption_co2_per_capita"]
        .rank(pct=True)
        .round(ROUND_DECIMALS)
    )

    df["material_footprint_percentile_by_year"] = (
        df.groupby("year")["material_footprint_per_capita"]
        .rank(pct=True)
        .round(ROUND_DECIMALS)
    )

    return df


def add_high_wellbeing_lower_pressure_flags(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add exploratory flags identifying country-years with:

    - high relative happiness;
    - lower relative consumption CO2;
    - lower relative material footprint.

    Thresholds
    ----------
    - happiness percentile >= 0.75
    - pressure percentile <= 0.50

    These are heuristic exploratory indicators rather than
    formal sustainability classifications.
    """

    missing = [
        c for c in FLAG_REQUIRED
        if c not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    df = df.copy()

    df["high_happiness_lower_consumption_co2"] = (
        (df["happiness_percentile_by_year"] >= 0.75)
        & (
            df["consumption_co2_percentile_by_year"]
            <= 0.50
        )
    )

    df["high_happiness_lower_material_footprint"] = (
        (df["happiness_percentile_by_year"] >= 0.75)
        & (
            df["material_footprint_percentile_by_year"]
            <= 0.50
        )
    )

    return df


def build_eda_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build EDA-specific exploratory features.

    These features are kept separate from the core analytical
    feature set because they are mainly used for exploratory
    comparison, ranking, and case identification within the EDA.
    """

    df = df.copy()

    df = add_year_relative_percentiles(df)

    df = add_high_wellbeing_lower_pressure_flags(df)

    return df