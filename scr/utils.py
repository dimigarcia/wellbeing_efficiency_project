import pandas as pd
import re

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize dataframe column names.

    Transformations:
    - lowercase
    - strip leading/trailing whitespace
    - replace spaces with underscores
    - remove parentheses
    - replace special characters with underscores
    - collapse repeated underscores

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.

    Returns
    -------
    pd.DataFrame
        Dataframe with cleaned column names.
    """

    cleaned_columns = []

    for col in df.columns:

        col = col.strip().lower()

        # Remove parentheses
        col = re.sub(r"[()]", "", col)

        # Replace non-alphanumeric characters with underscores
        col = re.sub(r"[^a-z0-9]+", "_", col)

        # Remove repeated underscores
        col = re.sub(r"_+", "_", col)

        # Remove leading/trailing underscores
        col = col.strip("_")

        cleaned_columns.append(col)

    df.columns = cleaned_columns

    return df


####################


def wide_to_long(
    df: pd.DataFrame, id_vars: list, year_pattern: str, value_name: str
) -> pd.DataFrame:
    """Reshapes a dataframe from wide to long by identifying and renaming year
    columns internally using a regex pattern.

    Parameters
    ----------
    df : pd.DataFrame
        The wide dataframe.
    id_vars : list
        The identifier columns to keep.
    year_pattern : str
        Regex pattern containing a capture group () for the 4-digit year.
    value_name : str
        Name for the final metric column.
    """
    # 1. Map original column names to the extracted 4-digit year
    rename_map = {}
    for col in df.columns:
        match = re.search(year_pattern, col)
        if match:
            # Extract the year from the first capture group
            rename_map[col] = match.group(1)

    value_vars = list(rename_map.values())

    # 2. Rename columns and subset the dataframe
    # This automatically ignores/drops any columns not in id_vars or rename_map (like unnamed_70)
    df_renamed = df.rename(columns=rename_map)[id_vars + value_vars]

    # 3. Melt the dataframe using the clean year strings
    df_long = pd.melt(
        df_renamed,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="year",
        value_name=value_name,
    )

    # 4. Convert year to integer
    df_long["year"] = df_long["year"].astype(int)

    return df_long


####################

def compare_values(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    col1: str,
    col2: str,
    name1: str = "Dataset 1",
    name2: str = "Dataset 2",
) -> dict:
    """
    Compare unique values between two dataframe columns.

    Returns values:
    - only in df1
    - only in df2
    - shared values
    """

    set1 = set(df1[col1].dropna())
    set2 = set(df2[col2].dropna())

    only_in_1 = sorted(set1 - set2)
    only_in_2 = sorted(set2 - set1)
    shared = sorted(set1 & set2)

    print(
        f"Unique values | {name1}: {len(set1)} | {name2}: {len(set2)}"
    )

    print(f"\nShared values: {len(shared)}")

    print(
        f"\n[1/2] In {name1} but missing from {name2} ({len(only_in_1)}):"
    )
    print(only_in_1 if only_in_1 else "None")

    print(
        f"\n[2/2] In {name2} but missing from {name1} ({len(only_in_2)}):"
    )
    print(only_in_2 if only_in_2 else "None")

    return {
        "shared": shared,
        "only_in_df1": only_in_1,
        "only_in_df2": only_in_2,
    }


####################

from difflib import get_close_matches
def check_close_matches(
    only_in_1,
    only_in_2,
    n_matches=10,
    cutoff=0.6
):
    """
    Find close string matches between two mismatch lists.

    Parameters
    ----------
    only_in_1 : list
        Values only found in dataset 1.

    only_in_2 : list
        Values only found in dataset 2.

    n_matches : int
        Maximum number of suggested matches.

    cutoff : float
        Similarity threshold between 0 and 1.
    """

    for value in only_in_1:

        matches = get_close_matches(
            value,
            only_in_2,
            n=n_matches,
            cutoff=cutoff
        )

        if matches:
            print(f"{value} -> {matches}")

# Define common overlapping window
START_YEAR = 2013
END_YEAR = 2021

def filter_year_range(df, year_col="year",
                      start_year=START_YEAR,
                      end_year=END_YEAR):
    """
    Filter dataframe to a selected year range.
    """

    return df[
        (df[year_col] >= start_year) &
        (df[year_col] <= end_year)
    ].copy()


def countries_with_missing_vars(
    df,
    key_vars,
    thresh_missing_vars
):
    """
    Returns a country-level summary of missing values for countries
    that have at least one country-year observation with more than
    `min_missing_vars` missing variables.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe.

    key_vars : list
        Variables to inspect.

    min_missing_vars : int
        Threshold for number of missing variables within a country-year.

    Returns
    -------
    pd.DataFrame
        Country-level missingness summary.
    """

    # Missing values by country
    missing_by_country = (
    df[key_vars]
    .isna()
    .groupby(df['country'])
    .sum()
    )

    # Missing values by country-year
    missing_by_country_year = (
    df[key_vars]
    .isna()
    .groupby([df['country'], df['year']])
    .sum()
    )

    # Keep country-years exceeding threshold
    filtered = missing_by_country_year[
        missing_by_country_year.sum(axis=1) > thresh_missing_vars
    ]

    # Extract affected countries
    affected_countries = (
        filtered.index
        .get_level_values('country')
        .unique()
    )

    # Subset country-level summary
    subset = missing_by_country[
        missing_by_country.index.isin(affected_countries)
    ]

    return subset.sort_index()

# Add sample yearly rank
def add_sample_yearly_rank(df, value_col="happiness_index"):
    df = df.copy()

    df["happiness_index_rank_62"] = (
        df.groupby("year")[value_col]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    return df



import pandas as pd
def assert_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}')
