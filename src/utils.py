import pandas as pd
import re
from difflib import get_close_matches

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

def check_duplicate_keys(df, keys, name="dataset"):
    """
    Check whether a dataframe has duplicate rows for a given key.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to check.
    keys : list[str]
        Columns that should uniquely identify rows.
    name : str
        Name used in printed output.

    Returns
    -------
    pd.DataFrame
        Rows with duplicated key values.
    """
    duplicated = df[df.duplicated(subset=keys, keep=False)].sort_values(keys)

    if duplicated.empty:
        print(f"No duplicate keys in {name} for {keys}")
    else:
        print(f"{len(duplicated)} rows with duplicate keys in {name} for {keys}")
        print(duplicated)

    return duplicated


def assert_unique_keys(df, keys, name="dataset"):
    """
    Raise an error if a dataframe contains duplicate rows for a given key.

    Use this before merges and before exporting final datasets.
    """
    duplicated = df[df.duplicated(subset=keys, keep=False)]

    if not duplicated.empty:
        raise ValueError(
            f"{name} contains duplicate rows for key {keys}. "
            f"Number of duplicated rows: {len(duplicated)}"
        )

    print(f"{name} has unique keys for {keys}")

import pandas as pd
def assert_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}')
