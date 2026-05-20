from pathlib import Path


def load_csv(path: str | Path):
    """Load a CSV file into a DataFrame."""
    import pandas as pd
    return pd.read_csv(path)

def load_json(path: str | Path):
    """Load a JSON file into a DataFrame."""
    import pandas as pd
    return pd.read_json(path)


def save_csv(df, path: str | Path, index: bool = False):
    """Save a DataFrame to CSV."""
    df.to_csv(path, index=index)