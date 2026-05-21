from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # Goes up from src/ to wellbeing_efficiency_project/

# Import path setup
import sys
sys.path.insert(0, str(ROOT))

# Data paths
CO2_PATH = ROOT / "data" / "raw" / "_owid_co2_data.csv"
ENERGY_PATH = ROOT / "data" / "raw" / "owid_energy_data.csv"
HAPPINESS_PATH = ROOT / "data" / "raw" / "world_happiness_index_data.csv"
MATERIAL_FOOTPRINT_PATH = ROOT / "data" / "raw" / "material_footprint_data_wide.csv"
GINI_PATH = ROOT / "data" / "raw" / "gini_data_wide.csv"
MERGED_RAW_PATH = ROOT / "data" / "processed_raw" / "global_sustainability_wellbeing_resource_data_raw.csv"
SUPPLEMENTARY_PATH = ROOT / "data" / "supplementary" / "country-territory-groups.json"
CLEAN_PATH = ROOT / "data" / "processed" / "sustainability_wellbeing_resource_data_clean.csv"
CLEAN_FEATURES_PATH = ROOT / "data" / "processed" / "sustainability_wellbeing_resource_data_clean_features.csv"
EDA_FEATURES_PATH = ROOT / "data" / "processed" / "sustainability_wellbeing_resource_data_eda.csv"
EDA_FIGURES_DIR = ROOT / "outputs" / "eda_figures"