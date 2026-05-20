from src.config import MERGED_RAW_PATH, CLEAN_PATH
from src.io import load_csv
from src.cleaning import clean
from src.features import build_features
from src.utils import assert_columns
from src.viz import plot_graph


def main():
    df = load_csv(MERGED_RAW_PATH)
    df = clean(df)
    df = build_features(df)
    # assert_columns(df, ['column_1', 'column_2'])

    plot_graph(df)

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)
    print(f"Saved: {CLEAN_PATH}")


if __name__ == "__main__":
    main()
