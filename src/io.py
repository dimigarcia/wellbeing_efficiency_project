from pathlib import Path
import matplotlib.pyplot as plt


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


def save_plot(
    fig,
    filename: str,
    output_dir: Path,
    dpi: int = 300,
) -> None:
    """
    Save a matplotlib figure to disk.
    """

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        output_dir / filename,
        bbox_inches="tight",
        dpi=dpi,
    )