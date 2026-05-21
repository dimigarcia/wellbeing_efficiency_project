from src.config import (
    CO2_PATH,
    ENERGY_PATH,
    HAPPINESS_PATH,
    MATERIAL_FOOTPRINT_PATH,
    GINI_PATH,
    SUPPLEMENTARY_PATH,
    MERGED_RAW_PATH,
    CLEAN_PATH,
    CLEAN_FEATURES_PATH,
)
from src.io import load_csv, load_json, save_csv
from src.setup import build_merged_raw_dataset
from src.cleaning import clean
from src.features import build_features
from src.viz import plot_graph


def main():
    # 1. Load raw source datasets
    co2_df = load_csv(CO2_PATH)
    energy_df = load_csv(ENERGY_PATH)
    happiness_df = load_csv(HAPPINESS_PATH)
    material_footprint_df = load_csv(MATERIAL_FOOTPRINT_PATH)
    gini_df = load_csv(GINI_PATH)

    # 2. Build merged raw dataset
    merged_raw_df = build_merged_raw_dataset(
        co2_df=co2_df,
        energy_df=energy_df,
        happiness_df=happiness_df,
        material_footprint_df=material_footprint_df,
        gini_df=gini_df,
    )

    save_csv(merged_raw_df, MERGED_RAW_PATH)
    print(f"Saved merged raw dataset: {MERGED_RAW_PATH}")

    # 3. Load supplementary data for cleaning/enrichment
    supplementary_data = load_json(SUPPLEMENTARY_PATH)

    # 4. Clean merged raw dataset
    clean_df = clean(
        merged_raw_df,
        supplementary_data=supplementary_data,
    )

    # 5. Save clean dataset
    save_csv(clean_df, CLEAN_PATH)
    print(f"Saved clean dataset: {CLEAN_PATH}")
    
    # 6. Build final analytical features
    final_df = build_features(clean_df)

    # # 7. Optional quick plot/check
    # plot_graph(final_df)

    # 8. Save final clean dataset
    save_csv(final_df, CLEAN_FEATURES_PATH)
    print(f"Saved clean dataset with features: {CLEAN_FEATURES_PATH}")


if __name__ == "__main__":
    main()