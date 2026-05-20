import re
import pandas as pd


START_YEAR = 2013
END_YEAR = 2021


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise dataframe column names.

    Transformations:
    - lowercase
    - strip leading/trailing whitespace
    - remove parentheses
    - replace non-alphanumeric characters with underscores
    - collapse repeated underscores
    """
    df = df.copy()

    cleaned_columns = []

    for col in df.columns:
        col = col.strip().lower()
        col = re.sub(r"[()]", "", col)
        col = re.sub(r"[^a-z0-9]+", "_", col)
        col = re.sub(r"_+", "_", col)
        col = col.strip("_")

        cleaned_columns.append(col)

    df.columns = cleaned_columns

    return df


def wide_to_long(
    df: pd.DataFrame,
    id_vars: list[str],
    year_pattern: str,
    value_name: str,
) -> pd.DataFrame:
    """
    Reshape a dataframe from wide to long format by extracting year columns
    with a regex pattern.

    Parameters
    ----------
    df : pd.DataFrame
        Wide dataframe.
    id_vars : list[str]
        Identifier columns to preserve.
    year_pattern : str
        Regex pattern containing one capture group for the year.
    value_name : str
        Name of the resulting value column.
    """
    df = df.copy()

    rename_map = {}

    for col in df.columns:
        match = re.search(year_pattern, col)
        if match:
            rename_map[col] = match.group(1)

    value_vars = list(rename_map.values())

    df_renamed = df.rename(columns=rename_map)[id_vars + value_vars]

    df_long = pd.melt(
        df_renamed,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="year",
        value_name=value_name,
    )

    df_long["year"] = df_long["year"].astype(int)

    return df_long


def filter_year_range(
    df: pd.DataFrame,
    year_col: str = "year",
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
) -> pd.DataFrame:
    """
    Filter dataframe to the selected project year range.
    """
    return df[
        (df[year_col] >= start_year)
        & (df[year_col] <= end_year)
    ].copy()


def prepare_co2_data(
    co2_df: pd.DataFrame,
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
) -> pd.DataFrame:
    """
    Prepare OWID CO2 data as the base dataset for merging.

    Drops non-country aggregate rows by requiring a valid ISO code, filters to
    the common year window, and keeps selected variables.
    """
    co2_df = clean_column_names(co2_df)

    co2_df = co2_df.dropna(subset=["iso_code"]).copy()

    co2_df = filter_year_range(
        co2_df,
        start_year=start_year,
        end_year=end_year,
    )

    keep_cols = [
        "country",
        "iso_code",
        "year",
        "co2_per_capita",
        "consumption_co2_per_capita",
        "energy_per_capita",
        "temperature_change_from_co2",
        "share_global_co2",
        "land_use_change_co2_per_capita",
    ]

    return co2_df[keep_cols].copy()


def prepare_energy_data(
    energy_df: pd.DataFrame,
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
) -> pd.DataFrame:
    """
    Prepare OWID energy data for merging.

    Filters to the common year window and keeps population, GDP, energy use,
    and renewable consumption variables.
    """
    energy_df = clean_column_names(energy_df)

    energy_df = energy_df.dropna(subset=["iso_code"]).copy()

    energy_df = filter_year_range(
        energy_df,
        start_year=start_year,
        end_year=end_year,
    )

    keep_cols = [
        "iso_code",
        "year",
        "population",
        "gdp",
        "energy_per_capita",
        "renewables_consumption",
    ]

    return energy_df[keep_cols].copy()


def prepare_happiness_data(
    happiness_df: pd.DataFrame,
    co2_df: pd.DataFrame,
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
) -> pd.DataFrame:
    """
    Prepare World Happiness Index data for merging.

    Renames key columns, harmonises known country-name mismatch, obtains ISO
    codes from the CO2 dataset, applies manual ISO fixes for known valid
    countries, filters to the common year window, and keeps selected variables.
    """
    happiness_df = clean_column_names(happiness_df)
    co2_df = clean_column_names(co2_df)

    happiness_df = happiness_df.rename(
        columns={
            "index": "happiness_index",
            "rank": "happiness_index_rank",
        }
    )

    happiness_df.loc[
        happiness_df["country"] == "Turkiye",
        "country",
    ] = "Turkey"

    iso_mapping = (
        co2_df[["country", "iso_code"]]
        .drop_duplicates()
        .dropna()
    )

    happiness_df = happiness_df.merge(
        iso_mapping,
        on="country",
        how="left",
    )

    hi_iso_fixes = {
    "Ivory Coast": "CIV",
    "Congo Kinshasa": "COD",
    "Congo Brazzaville": "COG",
    "Swaziland": "SWZ",
    }

    happiness_df["iso_code"] = happiness_df["iso_code"].fillna(
        happiness_df["country"].map(hi_iso_fixes)
    )

    happiness_df = happiness_df.dropna(subset=["iso_code"]).copy()

    happiness_df = filter_year_range(
        happiness_df,
        start_year=start_year,
        end_year=end_year,
    )

    happiness_df = (
        happiness_df
        .sort_values(["iso_code", "year", "happiness_index"], na_position="last")
        .drop_duplicates(subset=["iso_code", "year"], keep="first")
    )

    keep_cols = [
        "iso_code",
        "year",
        "happiness_index",
        "happiness_index_rank",
    ]

    return happiness_df[keep_cols].copy()


def prepare_material_footprint_data(
    material_footprint_df: pd.DataFrame,
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
) -> pd.DataFrame:
    """
    Prepare material footprint data for merging.

    Standardises columns, renames ISO column, reshapes from wide to long,
    filters to the common year window, and keeps selected variables.
    """
    material_footprint_df = clean_column_names(material_footprint_df)

    material_footprint_df = material_footprint_df.rename(
        columns={"iso3": "iso_code"}
    )

    id_vars = [
        "iso_code",
        "country",
        "continent",
        "hemisphere",
        "human_development_groups",
        "undp_developing_regions",
        "hdi_rank_2021",
    ]

    material_footprint_df = wide_to_long(
        df=material_footprint_df,
        id_vars=id_vars,
        year_pattern=r"material_footprint_per_capita_tonnes_(\d{4})",
        value_name="material_footprint_per_capita",
    )

    material_footprint_df = filter_year_range(
        material_footprint_df,
        start_year=start_year,
        end_year=end_year,
    )

    keep_cols = [
        "iso_code",
        "year",
        "continent",
        "hemisphere",
        "human_development_groups",
        "hdi_rank_2021",
        "undp_developing_regions",
        "material_footprint_per_capita",
    ]

    return material_footprint_df[keep_cols].copy()


def prepare_gini_data(
    gini_df: pd.DataFrame,
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
) -> pd.DataFrame:
    """
    Prepare GINI data for merging.

    Standardises columns, renames country and ISO columns, reshapes from wide
    to long, filters to the common year window, and keeps selected variables.
    """
    gini_df = clean_column_names(gini_df)

    gini_df = gini_df.rename(
        columns={
            "country_name": "country",
            "country_code": "iso_code",
        }
    )

    id_vars = [
        "country",
        "iso_code",
        "indicator_name",
        "indicator_code",
    ]

    gini_df = wide_to_long(
        df=gini_df,
        id_vars=id_vars,
        year_pattern=r"^(\d{4})$",
        value_name="gini_index",
    )

    gini_df = filter_year_range(
        gini_df,
        start_year=start_year,
        end_year=end_year,
    )

    keep_cols = [
        "iso_code",
        "year",
        "gini_index",
    ]

    return gini_df[keep_cols].copy()


def build_merged_raw_dataset(
    co2_df: pd.DataFrame,
    energy_df: pd.DataFrame,
    happiness_df: pd.DataFrame,
    material_footprint_df: pd.DataFrame,
    gini_df: pd.DataFrame,
    start_year: int = START_YEAR,
    end_year: int = END_YEAR,
) -> pd.DataFrame:
    """
    Build the merged raw country-year dataset.

    The CO2 dataset is used as the base dataset. Other datasets are left-joined
    onto it using `iso_code` and `year`.
    """
    co2_clean = prepare_co2_data(
        co2_df,
        start_year=start_year,
        end_year=end_year,
    )

    energy_clean = prepare_energy_data(
        energy_df,
        start_year=start_year,
        end_year=end_year,
    )

    happiness_clean = prepare_happiness_data(
        happiness_df,
        co2_df=co2_df,
        start_year=start_year,
        end_year=end_year,
    )

    material_footprint_clean = prepare_material_footprint_data(
        material_footprint_df,
        start_year=start_year,
        end_year=end_year,
    )

    gini_clean = prepare_gini_data(
        gini_df,
        start_year=start_year,
        end_year=end_year,
    )

    df_final_raw = (
        co2_clean
        .merge(
            energy_clean,
            on=["iso_code", "year"],
            how="left",
            validate="one_to_one",
            suffixes=("", "_energy"),
        )
        .merge(
            happiness_clean,
            on=["iso_code", "year"],
            how="left",
            validate="one_to_one",
        )
        .merge(
            material_footprint_clean,
            on=["iso_code", "year"],
            how="left",
            validate="one_to_one",
        )
        .merge(
            gini_clean,
            on=["iso_code", "year"],
            how="left",
            validate="one_to_one",
        )
    )

    df_final_raw = df_final_raw.sort_values(
        by=["iso_code", "year"]
    ).reset_index(drop=True)

    return df_final_raw