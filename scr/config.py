from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # Goes up from scr/ to wellbeing_efficiency_project/

# Import path setup
import sys
sys.path.insert(0, str(ROOT))

# Data paths
RAW_PATH = ROOT / "data" / "processed_raw" / "global_sustainability_wellbeing_resource_data_raw.csv"
OUT_PATH = ROOT / "data" / "processed" / "sustainability_wellbeing_resource_data_clean.csv"