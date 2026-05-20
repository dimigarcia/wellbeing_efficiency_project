# Exploring Sustainable Wellbeing: A Cross-Country Analysis of Resource Use, Emissions and Quality of Life

## <p align="center">🚧 Work in progress 🚧</p>

### 1) Objective
The objective of this project is to build a coherent cross-country dataset by merging multiple public data sources related to wellbeing, inequality, economic development, energy use, emissions, and material consumption.  

Using this merged dataset, the project applies data cleaning, transformation, feature engineering, and visualization techniques to explore whether countries can achieve high levels of wellbeing with lower environmental and material impact.  

The analysis aims to demonstrate a complete and reproducible data analysis workflow, from raw heterogeneous datasets to interpretable insights and visual exploration of potential decoupling between quality of life and resource consumption.

### 2) Research questions
**About the dataset:**
- Q1: How many countries and years have enough data to consider wellbeing and resource use and socioeconomic factors within a single comprehensive dataset?
- Q2: Does the dataset represent enough types of countries relative to various UN classifications?
- Q3: Are any country types underrepresented, hence pointing toward some explanation for data missingness based on these types?

**About wellbeing, sustainability and resource use:**
- Q: 

### 3) About the dataset
- The *Sustainability, Wellbeing and Resource Use Dataset* is constructed drawing on various reliable public data sources.
- Sources: Our World in Data, The World Happiness Report, UN Human Development Reports
- Coverage: 2013 - 2021
- Rows/columns: Variable (depende del archivo cargado)
- Key variables:

# Dataset Overview (clean)
## *Sustainability, Wellbeing and Resource Use Dataset*

- **Rows:** 558  
- **Columns:** 29  
- **Total Missing Values:** 0

| Data Type | Count |
|---|---:|
| `str` | 9 |
| `int64` | 4 |
| `float64` | 13 |
| `bool` | 3 |

---

## Variable Dictionary by Type

### 1. Index Variables

| Variable | Data Type | Description |
|---|---|---|
| `numeric_code` | `str` | Numeric country identifier code. |
| `iso_code` | `str` | ISO alpha country code (e.g., ESP, USA, FRA). |
| `country` | `str` | Country name. |
| `year` | `int64` | Observation year associated with the record. |

---

### 2. Country Group Variables

| Variable | Data Type | Description |
|---|---|---|
| `human_development_groups` | `str` | Human Development Index (HDI) classification group (e.g., Low, Medium, High, Very High). |
| `hdi_rank_2021` | `int64` | HDI rank based on the 2021 Human Development Report. Lower values indicate stronger development performance. |
| `undp_developing_regions` | `str` | UNDP regional classification for developing economies. Contains missing values. |
| `least_devpd_country` | `bool` | Indicates whether the country is classified as a Least Developed Country (LDC). |
| `landlock_deving_country` | `bool` | Indicates whether the country is classified as a Landlocked Developing Country (LLDC). |
| `small_island_deving_country` | `bool` | Indicates whether the country is classified as a Small Island Developing State (SIDS). |

---

### 3. Impact Variables

| Variable | Data Type | Description |
|---|---|---|
| `co2_per_capita` | `float64` | Carbon dioxide emissions per capita. |
| `consumption_co2_per_capita` | `float64` | Consumption-based CO₂ emissions per capita, accounting for trade-adjusted emissions. |
| `material_footprint_per_capita` | `float64` | Per-capita material footprint associated with domestic consumption. |
| `energy_per_capita` | `float64` | Energy consumption per capita. |
| `renewables_consumption` | `float64` | Renewable energy consumption share or level. |
| `temperature_change_from_co2` | `float64` | Estimated temperature contribution associated with CO₂ emissions. |
| `share_global_co2` | `float64` | Country share of global CO₂ emissions. |
| `land_use_change_co2_per_capita` | `float64` | Per-capita CO₂ emissions resulting from land-use changes. |

---

### 4. Socioeconomic Variables

| Variable | Data Type | Description |
|---|---|---|
| `population` | `int64` | Total population of the country in the given year. |
| `gdp` | `float64` | Gross Domestic Product (GDP), likely measured in USD. |
| `happiness_index` | `float64` | National happiness or subjective wellbeing score. |
| `gini_index` | `float64` | Income inequality measure; higher values indicate greater inequality. |
| `income_group` | `str` | Income classification category (e.g., low income, upper middle income). |
| `happiness_index_rank_62` | `int64` | Country ranking based on happiness index among sampled countries. |

---

### 5. Location Variables

| Variable | Data Type | Description |
|---|---|---|
| `continent` | `str` | Continent classification of the country. |
| `sub_continent_un` | `str` | United Nations sub-region classification. |
| `hemisphere` | `str` | Geographic hemisphere classification. |
| `latitude` | `float64` | Latitude coordinate of the country reference point or centroid. |
| `longitude` | `float64` | Longitude coordinate of the country reference point or centroid. |

---

## Missing Values Summary

| Variable | Missing Values | Notes |
|---|---:|---|
| `undp_developing_regions` | 324 | Missing for countries outside UNDP developing-region classifications. |

### 4) Data issues & fixes
- Several data sources with inconsistent wide format → Wide-to-long transformation.
- Different years of coverage per data source → Identify overlap window and constrain dataset within it.
- Inconsistent/Missing ISO Country codes for merging → Normalisation of merge keys accross all 5 datasets.
- Unmerged data → Merging the data correclty into a final single raw dataset.
- Countries missing entries for all years within key_variables → Dimensionality is reduced by removing problematic countries in this sense prioritizing data availability for conceptual richness over number of observations.
- Happiness index missing all 2014 values for all countries → These are interpolated linearly between the previous and subsequent years.
- Happiness index missing for 2020 and 2021 for (iso_code) QAT → These are filled by considering its historic trend but accounting for the average changes in countries of similar human development level and continent, to account for important impacts like COVID.
- Happiness index rank missing: Re-secified as a sample specific rank without missing values and attached to the existing happiness_index column.
- UNDP Developing Regions missing values for 36 countries: These are identified as countries that are not classified within this criterion. Missing values are replaced with 'NOTAPPLICABLE' which is more useful and explanatory.
- GINI index missing sparse values for 20 countries → All countries have observations for at least 3 years. Assuming a more control-role for this variable, it is deemed reasonable to linearly interpolate the missing values based on the available ones. Countries with imputed gini_index values are stored in `imputed_gini` to allow for reliability and other checks.
- Rank and population variables as floats → We check whether any non-zero decimals exist. After confirming there arent, we transform to integer as necessary.


### 5) Pipeline
- pre-merge raw → merged raw → clean → features → viz → (optional export to `data/processed/`)

### 6) Findings
- Insight 1: 
- Insight 2: 
- Insight 3: 

### 7) Project structure
- `src/` has reusable functions (`io`, `cleaning`, `features`, `viz`)
- `main.py` ejecuta el pipeline end-to-end

### 8) Execution
- `pip install -r requirements.txt`
- Execute pipeline: `python main.py`
- (Optional) Open and execute: `notebooks/eda.ipynb`

## Project structure

Preliminary structure:

```
project/
├── main.py
├── data/
│   ├── raw/                        # original source files, untouched
│   ├── processed_raw/              # harmonised/merged but not fully cleaned analytical dataset
│   ├── processed/                  # final cleaned/exportable analytical dataset
│   └── supplementary/              # lookup tables, country classifications, manually curated mappings
├── notebooks/
│   └── data_raw_setup.ipynb
│   └── data_cleaning.ipynb
│   └── eda.ipynb
├── src/
│   ├── __init__.py
│   ├── io.py
│   ├── cleaning.py
│   ├── config.py
│   ├── features.py
│   ├── viz.py
│   └── utils.py
├── README.md
├── .gitignore
└── requirements.txt

```