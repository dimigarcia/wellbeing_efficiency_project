from scr.config import RAW_PATH, OUT_PATH
from scr.io import load_csv
from scr.cleaning import clean
from scr.features import build_features
from scr.utils import assert_columns
from scr.viz import plot_graph


def main():
    df = load_csv(RAW_PATH)
    df = clean(df)
    df = build_features(df)
    # assert_columns(df, ['column_1', 'column_2'])

    plot_graph(df)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
