import pandas as pd

KEY_VARS = [
    "happiness_index",
    "gini_index",
    "material_footprint_per_capita",
    "consumption_co2_per_capita",
    "co2_per_capita",
    "energy_per_capita",
    "renewables_consumption",
]


def countries_with_missing_vars(
    df: pd.DataFrame,
    key_vars: list[str],
    thresh_missing_vars: int,
) -> pd.DataFrame:
    """
    Return a country-level missingness summary for countries that have at least
    one country-year observation with more than `thresh_missing_vars` missing
    key variables.
    """
    missing_by_country = (
        df[key_vars]
        .isna()
        .groupby(df["country"])
        .sum()
    )

    missing_by_country_year = (
        df[key_vars]
        .isna()
        .groupby([df["country"], df["year"]])
        .sum()
    )

    filtered = missing_by_country_year[
        missing_by_country_year.sum(axis=1) > thresh_missing_vars
    ]

    affected_countries = (
        filtered.index
        .get_level_values("country")
        .unique()
    )

    subset = missing_by_country[
        missing_by_country.index.isin(affected_countries)
    ]

    return subset.sort_index()


def resolve_energy_per_capita_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resolve duplicated energy_per_capita columns created during merging.

    Keeps `energy_per_capita_y` as `energy_per_capita` and drops
    `energy_per_capita_x`, matching the notebook decision.
    """
    df = df.copy()

    if {"energy_per_capita_x", "energy_per_capita_y"}.issubset(df.columns):
        df = df.rename(columns={"energy_per_capita_y": "energy_per_capita"})
        df = df.drop(columns=["energy_per_capita_x"])

    return df


def drop_countries_from_missingness_thresholds(
    df: pd.DataFrame,
    key_vars: list[str] = KEY_VARS,
    thresholds: tuple[int, ...] = (6, 5, 4),
) -> pd.DataFrame:
    """
    Sequentially drop countries that exceed high missingness thresholds.

    This formalises the early notebook steps where countries with more than
    6, then 5, then 4 missing key variables in any country-year observation
    are removed.
    """
    df = df.copy()

    for threshold in thresholds:
        subset_missing = countries_with_missing_vars(
            df=df,
            key_vars=key_vars,
            thresh_missing_vars=threshold,
        )

        iso_codes_to_drop = (
            df.loc[df["country"].isin(subset_missing.index), "iso_code"]
            .dropna()
            .unique()
        )

        df = df[~df["iso_code"].isin(iso_codes_to_drop)].copy()

    return df


def interpolate_happiness_2014(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing 2014 happiness_index values by linear interpolation within
    each country.
    """
    df = df.copy()

    interpolated = (
        df.groupby("iso_code")["happiness_index"]
        .transform(lambda x: x.interpolate(method="linear"))
    )

    mask_2014 = (
        (df["year"] == 2014)
        & (df["happiness_index"].isna())
    )

    df.loc[mask_2014, "happiness_index"] = interpolated[mask_2014]

    return df


def drop_remaining_high_missingness_countries(
    df: pd.DataFrame,
    key_vars: list[str] = KEY_VARS,
) -> pd.DataFrame:
    """
    Apply the remaining country exclusion rules from the notebook after the
    2014 happiness interpolation step.
    """
    df = df.copy()

    subset_missing_3 = countries_with_missing_vars(
        df=df,
        key_vars=key_vars,
        thresh_missing_vars=3,
    )

    iso_codes_to_drop = (
        df.loc[df["country"].isin(subset_missing_3.index), "iso_code"]
        .dropna()
        .unique()
    )

    df = df[~df["iso_code"].isin(iso_codes_to_drop)].copy()

    subset_missing_2 = countries_with_missing_vars(
        df=df,
        key_vars=key_vars,
        thresh_missing_vars=2,
    )

    key_missing = subset_missing_2[
        (
            (subset_missing_2["material_footprint_per_capita"] == 9)
            & (subset_missing_2["consumption_co2_per_capita"] == 9)
        )
        |
        (
            (subset_missing_2["happiness_index"] > 3)
            | (subset_missing_2["gini_index"] > 3)
        )
    ]

    countries_to_drop = (
        df.loc[df["country"].isin(key_missing.index), "iso_code"]
        .dropna()
        .unique()
    )

    df = df[~df["iso_code"].isin(countries_to_drop)].copy()

    subset_missing_2 = countries_with_missing_vars(
        df=df,
        key_vars=key_vars,
        thresh_missing_vars=2,
    )

    gini_missing = subset_missing_2[
        (subset_missing_2["gini_index"] == 9)
        & (
            (subset_missing_2["consumption_co2_per_capita"] == 9)
            | (subset_missing_2["material_footprint_per_capita"] == 9)
        )
    ]

    countries_to_drop = (
        df.loc[df["country"].isin(gini_missing.index), "iso_code"]
        .dropna()
        .unique()
    )

    df = df[~df["iso_code"].isin(countries_to_drop)].copy()

    iso_to_drop = (
        df.groupby("iso_code")[key_vars]
        .apply(lambda x: (x.isna().sum() == 9).any())
    )

    df = df[
        ~df["iso_code"].isin(iso_to_drop[iso_to_drop].index)
    ].copy()

    return df


def impute_qatar_happiness(df: pd.DataFrame) -> pd.DataFrame:
    """
    Impute missing QAT happiness_index values for 2020 and 2021 using the
    peer-adjusted method developed in the cleaning notebook.

    Peer countries are defined as countries sharing Qatar's continent and
    human-development group.
    """
    df = df.copy()

    if "QAT" not in df["iso_code"].unique():
        return df

    qat_missing_years = [2020, 2021]

    if not df.loc[
        (df["iso_code"] == "QAT")
        & (df["year"].isin(qat_missing_years)),
        "happiness_index",
    ].isna().any():
        return df

    qat_meta = (
        df.loc[
            df["iso_code"] == "QAT",
            ["continent", "human_development_groups"],
        ]
        .drop_duplicates()
        .iloc[0]
    )

    qat_continent = qat_meta["continent"]
    qat_hdi = qat_meta["human_development_groups"]

    peer_countries = (
        df.loc[
            (df["continent"] == qat_continent)
            & (df["human_development_groups"] == qat_hdi),
            "iso_code",
        ]
        .unique()
    )

    qat_diff = (
        df.loc[df["iso_code"] == "QAT", ["year", "happiness_index"]]
        .sort_values("year", ascending=False)
        .assign(diff=lambda x: x["happiness_index"].diff(-1))["diff"]
        .dropna()
    )

    peer_diffs = (
        df.loc[
            df["iso_code"].isin(peer_countries),
            ["iso_code", "year", "happiness_index"],
        ]
        .sort_values(["iso_code", "year"], ascending=[True, False])
        .groupby("iso_code")
        .apply(lambda x: x.assign(diff=x["happiness_index"].diff(-1)))
        .reset_index(drop=True)["diff"]
        .dropna()
    )

    qat_variance = qat_diff.var()
    peer_variance = peer_diffs.var()

    qat_diffs = (
        df.loc[df["iso_code"] == "QAT", ["year", "happiness_index"]]
        .sort_values("year")
        .assign(diff=lambda x: x["happiness_index"].diff())
    )

    qat_observed_diffs = qat_diffs["diff"].dropna()
    qat_diff_mean = qat_observed_diffs.mean()
    qat_diff_std = qat_observed_diffs.std()

    peer_yearly = (
        df.loc[
            df["iso_code"].isin(peer_countries),
            ["iso_code", "year", "happiness_index"],
        ]
        .sort_values(["iso_code", "year"])
        .groupby("iso_code")
        .apply(lambda x: x.assign(diff=x["happiness_index"].diff()))
        .reset_index(drop=True)
    )

    peer_diff_stats = (
        peer_yearly
        .groupby("year")["diff"]
        .agg(["mean", "std"])
        .rename(
            columns={
                "mean": "peer_mean_diff",
                "std": "peer_std_diff",
            }
        )
    )

    variance_ratio = qat_variance / peer_variance

    qat_series = (
        df.loc[df["iso_code"] == "QAT", ["year", "happiness_index"]]
        .sort_values("year")
        .copy()
    )

    for yr in qat_missing_years:
        prev_year = yr - 1

        prev_value = qat_series.loc[
            qat_series["year"] == prev_year,
            "happiness_index",
        ].iloc[0]

        peer_change = peer_diff_stats.loc[yr, "peer_mean_diff"]

        peer_z = (
            (peer_change - peer_diff_stats["peer_mean_diff"].mean())
            / peer_diff_stats["peer_mean_diff"].std()
        )

        qat_scaled_z = peer_z * variance_ratio

        qat_change = qat_diff_mean + qat_scaled_z * qat_diff_std

        imputed_value = prev_value + qat_change

        qat_series.loc[
            qat_series["year"] == yr,
            "happiness_index",
        ] = imputed_value

    for yr in qat_missing_years:
        imputed_val = qat_series.loc[
            qat_series["year"] == yr,
            "happiness_index",
        ].iloc[0]

        df.loc[
            (df["iso_code"] == "QAT") & (df["year"] == yr),
            "happiness_index",
        ] = imputed_val

    return df

# Add sample yearly rank
def add_sample_yearly_rank(df, value_col="happiness_index"):
    df = df.copy()

    df["happiness_index_rank_62"] = (
        df.groupby("year")[value_col]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    return df

def prepare_supplementary_country_data(
    supplementary_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Prepare supplementary country classification/geographic metadata.
    """
    un_df = supplementary_data.copy()

    un_df.columns = (
        un_df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[()]", "", regex=True)
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    un_df = un_df.rename(
        columns={
            "alpha_3_code_1": "iso_code",
            "group_1": "continent_un",
            "latitude_average": "latitude",
            "longitude_average": "longitude",
            "group_2": "sub_continent_un",
            "ldc": "least_devpd_country",
            "lldc": "landlock_deving_country",
            "sids": "small_island_deving_country",
        }
    )

    cols_to_drop = [
        "development_classification",
        "country_or_area",
        "alpha_2_code",
        "group_3",
    ]

    un_df = un_df.drop(
        columns=[col for col in cols_to_drop if col in un_df.columns]
    )

    return un_df


def add_supplementary_country_data(
    df: pd.DataFrame,
    supplementary_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge supplementary country classification/geographic metadata into the
    cleaned dataset.
    """
    df = df.copy()

    un_df = prepare_supplementary_country_data(supplementary_data)

    df = df.merge(
        un_df,
        on="iso_code",
        how="left",
        validate="many_to_one",
    )

    if "continent_un" in df.columns:
        df = df.drop(columns=["continent_un"])

    return df


def interpolate_gini_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill sparse gini_index missing values using within-country linear
    interpolation, filling endpoints from nearest available values.
    """
    df = df.copy()

    df["gini_index"] = (
        df.groupby("country")["gini_index"]
        .transform(lambda x: x.interpolate(method="linear", limit_direction="both"))
    )

    return df


def convert_integer_columns(
    df: pd.DataFrame,
    int_cols: tuple[str, ...] = ("hdi_rank_2021", "population"),
) -> pd.DataFrame:
    """
    Convert integer-like columns to integer dtype.
    """
    df = df.copy()

    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)

    return df


def reorder_clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorder final clean dataset columns by conceptual group.
    """
    index_vars = [
        "numeric_code",
        "iso_code",
        "country",
        "year",
    ]

    country_group_vars = [
        "human_development_groups",
        "hdi_rank_2021",
        "undp_developing_regions",
        "least_devpd_country",
        "landlock_deving_country",
        "small_island_deving_country",
    ]

    socioeconomic_vars = [
        "population",
        "gdp",
        "happiness_index",
        "gini_index",
        "income_group",
        "happiness_index_rank_62",
    ]

    impact_vars = [
        "co2_per_capita",
        "consumption_co2_per_capita",
        "material_footprint_per_capita",
        "energy_per_capita",
        "renewables_consumption",
        "temperature_change_from_co2",
        "share_global_co2",
        "land_use_change_co2_per_capita",
    ]

    location_vars = [
        "continent",
        "sub_continent_un",
        "hemisphere",
        "latitude",
        "longitude",
    ]

    ordered_cols = (
        index_vars
        + country_group_vars
        + socioeconomic_vars
        + impact_vars
        + location_vars
    )

    df = df[ordered_cols].copy()

    df = (
        df.sort_values(by=["iso_code", "year"])
        .reset_index(drop=True)
    )

    return df


def clean(
    df: pd.DataFrame,
    supplementary_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean the merged raw sustainability-wellbeing-resource dataset.

    This function formalises the stable cleaning decisions from the
    data_cleaning notebook.
    """
    df = df.copy()

    df = resolve_energy_per_capita_columns(df)

    df = drop_countries_from_missingness_thresholds(
        df,
        key_vars=KEY_VARS,
        thresholds=(6, 5, 4),
    )

    df = interpolate_happiness_2014(df)

    df = drop_remaining_high_missingness_countries(
        df,
        key_vars=KEY_VARS,
    )

    df = impute_qatar_happiness(df)

    df = df.copy()

    df = add_sample_yearly_rank(df)

    if "happiness_index_rank" in df.columns:
        df = df.drop(columns=["happiness_index_rank"])

    df["undp_developing_regions"] = (
        df["undp_developing_regions"]
        .fillna("NOTAPPLICABLE")
    )

    df = add_supplementary_country_data(
        df,
        supplementary_data=supplementary_data,
    )

    df = interpolate_gini_by_country(df)

    df = reorder_clean_columns(df)

    df = convert_integer_columns(df)

    return df