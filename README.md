# Exploring Sustainable Wellbeing: A Cross-Country Analysis of Resource Use, Emissions and Quality of Life

## Table of contents

- [1) Objective](#1-objective)
- [2) Research questions](#2-research-questions)
- [3) About the dataset](#3-about-the-dataset)
- [4) Data issues & fixes](#4-data-issues--fixes)
- [5) Pipeline](#5-pipeline)
- [6) Findings](#6-findings)
  - [Key insights](#key-insights)
  - [Dataset construction findings](#dataset-construction-findings)
  - [Conceptual and exploratory findings](#conceptual-and-exploratory-findings)
  - [Insight-to-research-question mapping](#insight-to-research-question-mapping)
- [7) Project structure](#7-project-structure)
- [8) Execution](#8-execution)
- [9) Limitations](#9-limitations)
- [10) Further research](#10-further-research)
- [11) Conclusion](#11-conclusion)

### 1) Objective

The objective of this project is to build a coherent cross-country dataset by merging multiple public data sources related to wellbeing, inequality, economic development, energy use, emissions, and material consumption.

Using this merged dataset, the project applies data cleaning, transformation, feature engineering, and visualisation techniques to explore whether countries can achieve high levels of wellbeing with lower environmental and material impact.

The analysis also examines the role and limits of subjective wellbeing measures. Since happiness indices are based on self-reported evaluations, they may partly reflect adaptation, expectations, cultural response patterns, or normalised social conditions. The project therefore compares raw happiness with inequality-adjusted happiness to explore how incorporating a more objective distributional condition changes interpretations of wellbeing, sustainability, and apparent wellbeing-efficiency.

Overall, the project aims to demonstrate a complete and reproducible data analysis workflow, from raw heterogeneous datasets to interpretable insights about wellbeing, resource use, emissions, and inequality.

### 2) Research questions

This project is organised around two sets of research questions.

**Dataset construction:**

1. How can public datasets on wellbeing, inequality, emissions, energy use, material footprint, and country classifications be combined into a coherent country-year panel?

2. What countries and years can be retained when requiring overlapping information on wellbeing, inequality, emissions, material footprint, and energy use?

3. How is the resulting analytical dataset distributed across regions, income groups, and human development categories?

4. What data availability constraints or representational imbalances should be considered when interpreting the final dataset?

**Wellbeing, sustainability, and inequality:**

1. What is the relationship between subjective wellbeing and environmental or material pressure across countries?

2. How do production-based and consumption-based CO₂ emissions differ, and what does this imply for cross-country environmental comparisons?

3. How does subjective wellbeing relate to material footprint per capita?

4. Which countries appear to achieve relatively high wellbeing with comparatively lower environmental or material pressure?

5. How does incorporating income inequality change the interpretation of national wellbeing outcomes?

6. Do within-country changes in material footprint correspond to changes in subjective or inequality-adjusted wellbeing over time?

### 3) About the dataset

The *Sustainability, Wellbeing and Resource Use Dataset* is a constructed country-year panel combining multiple public data sources on subjective wellbeing, inequality, emissions, energy use, material footprint, development status, income group, and geography.

The dataset is not taken from a single source. A major part of the project involved harmonising heterogeneous source datasets, reshaping wide-format data, aligning countries and years, resolving merge inconsistencies, cleaning missing values, and constructing a final analytical panel.

**Sources:**
- Our World in Data: CO₂ emissions, consumption-based CO₂, energy use, population, GDP, and related environmental indicators.
- World Happiness Report: subjective wellbeing / happiness index.
- World Bank: Gini index.
- UN Human Development Reports: human development groups, HDI rank, and income groups.
- Supplementary UN-style country metadata: region, sub-region, hemisphere, and country classification flags.

**Coverage:**
- Years: 2013–2021
- Countries: 62
- Observations: 558 country-years
- Final clean dataset: balanced 62 × 9 country-year panel
- Missing values in final clean dataset: 0

**Main variable groups:**
- **Wellbeing:** `happiness_index`, `happiness_index_rank_62`
- **Inequality:** `gini_index`
- **Environmental pressure:** `co2_per_capita`, `consumption_co2_per_capita`, `material_footprint_per_capita`
- **Energy and economic context:** `energy_per_capita`, `renewables_consumption`, `gdp`, `population`
- **Development and income classifications:** `human_development_groups`, `hdi_rank_2021`, `income_group`
- **Geographic and country classifications:** `continent`, `sub_continent_un`, `hemisphere`, `least_devpd_country`, `landlock_deving_country`, `small_island_deving_country`

The final dataset should be interpreted as a clean analytical panel of countries with sufficient overlapping data across the required wellbeing, inequality, and environmental variables. It is not a fully representative global sample. European, high-income, and very-high-HDI countries are comparatively well represented, while some lower-income regions are less represented due to data availability constraints.

### 4) Data issues & fixes

Building the final analytical dataset required several cleaning, harmonisation, and validation steps.

- **Heterogeneous source formats** → Several datasets were provided in wide format, with years stored as separate columns. These were reshaped into long country-year format before merging.

- **Different temporal coverage across sources** → Source datasets covered different year ranges. The analysis was restricted to the common 2013–2021 window to maximise comparability across variables.

- **Inconsistent country identifiers** → Country names, ISO codes, and merge keys were standardised across sources to support reliable country-year merging.

- **Duplicate energy variable after merging** → Both the CO₂ and energy datasets contained an `energy_per_capita` variable. The dedicated energy-source version was retained and renamed consistently.

- **Countries with insufficient overlapping data** → Countries with substantial missingness across key wellbeing, inequality, emissions, material-footprint, and energy variables were removed. This prioritised a complete and conceptually rich analytical panel over maximising the number of countries.

- **Missing 2014 happiness values** → The World Happiness data contained missing 2014 happiness values. These were filled using within-country linear interpolation between surrounding years.

- **Missing Qatar happiness values for 2020–2021** → Qatar had missing happiness values for 2020 and 2021. These were imputed using a peer-adjusted approach based on Qatar’s previous trend and average changes among countries in the same continent and human-development group.

- **Missing happiness rank values** → The original happiness-rank variable was replaced with a sample-specific yearly rank, `happiness_index_rank_62`, calculated within the final 62-country analytical sample.

- **Missing UNDP developing-region values** → Countries not classified under UNDP developing-region categories were assigned `"NOTAPPLICABLE"` rather than leaving these values missing.

- **Sparse missing Gini values** → Remaining sparse `gini_index` gaps were filled using within-country linear interpolation, with endpoint values filled from the nearest available observations.

- **Interpolated and imputed values rounded for readability** → Interpolated/imputed happiness and Gini values were rounded consistently to match the feature-engineering conventions used later in the project.

- **Integer-like columns stored as floats** → Variables such as population and HDI rank were checked for non-zero decimal values and converted to integer type where appropriate.

- **Categorical variables typed explicitly** → Ordered categorical types were applied where meaningful, such as income group and human-development group. Nominal classifications such as continent, sub-region, and hemisphere were also converted to categorical type.

- **Final validation** → The final clean dataset was checked for structure, missing values, duplicate country-year records, and column consistency before feature engineering.


### 5) Pipeline

The project follows a modular and reproducible pipeline:

1. **Raw data preparation**  
   Source datasets are standardised, reshaped where needed, harmonised by country/year identifiers, and restricted to a common 2013–2021 analysis window.  
   Implemented mainly in `src/setup.py`.

2. **Merged raw dataset construction**  
   The prepared source datasets are merged into a single country-year dataset and exported to:

   `data/processed_raw/global_sustainability_wellbeing_resource_data_raw.csv`

3. **Cleaning and validation**  
   The merged dataset is cleaned through missingness-based country filtering, targeted interpolation/imputation, supplementary country metadata enrichment, type conversion, and column reordering.  
   Implemented in `src/cleaning.py`.

   Output:

   `data/processed/sustainability_wellbeing_resource_data_clean.csv`

4. **Core feature engineering**  
   Reusable analytical features are added, including emissions-accounting gaps, wellbeing-efficiency ratios, inequality-adjusted happiness, and diagnostic energy-intensity indicators.  
   Implemented in `src/features.py`.

   Output:

   `data/processed/sustainability_wellbeing_resource_data_clean_features.csv`

5. **EDA-specific feature construction**  
   Year-relative percentile variables and exploratory high-wellbeing/lower-pressure flags are added separately from the core feature dataset.  
   Implemented in `src/eda_features.py`.

   Optional output:

   `data/processed/sustainability_wellbeing_resource_data_eda.csv`

6. **Exploratory visualisation and synthesis**  
   Final figures are produced from the EDA-ready dataset using `src/viz.py`.

   Optional output:

   `outputs/eda_figures/`

7. **End-to-end execution**  
   The full pipeline can be run from:

   `main.py`

   This rebuilds the merged raw, clean, and core feature datasets. It can also optionally export the EDA-ready dataset (default=TRUE) and the final EDA figures (default=FALSE).

### Notebooks

The project also includes three notebooks that document the analytical workflow in more detail:

- `notebooks/data_raw_setup.ipynb`  
  Documents the raw data preparation stage, including source inspection, reshaping, harmonisation of country/year identifiers, and construction of the merged raw dataset.

- `notebooks/data_cleaning.ipynb`  
  Documents the cleaning logic in depth, including missingness checks, country exclusion decisions, interpolation/imputation choices, supplementary metadata enrichment, type conversion, and final validation.

- `notebooks/eda.ipynb`  
  Documents the exploratory analysis, including feature construction, dataset overview, environmental-pressure comparisons, wellbeing-efficiency analysis, inequality-adjusted wellbeing, percentile comparisons, within-country checks, and final synthesis.

The notebooks provide the narrative and diagnostic reasoning behind the modular functions in `src/`, while `main.py` provides the reproducible end-to-end execution path.

### 6) Findings

The project produced findings at two levels: first, about the construction and scope of the dataset itself; second, about the exploratory relationships between wellbeing, environmental pressure, and inequality.

#### Key insights

- The final dataset provides a clean and balanced 62-country × 9-year analytical panel covering 2013–2021, but it is not globally representative.

- Data availability is uneven across regions and development groups, with European, high-income, and very-high-HDI countries better represented than lower-income regions.

- High subjective wellbeing is often associated with higher environmental and material intensity, but the relationship shows clear diminishing returns.

- Material footprint is particularly useful for examining decoupling because very high material consumption does not appear to produce proportionally higher wellbeing.

- Countries that appear environmentally wellbeing-efficient do not necessarily perform equally well once inequality is considered.

- Very few countries simultaneously combine high wellbeing, low material-resource intensity, and low income inequality.

- Within-country changes in material footprint show only weak associations with changes in raw or inequality-adjusted wellbeing.

---

#### Dataset construction findings

1. **A coherent country-year panel can be constructed, but only after substantial harmonisation.**  
   The final dataset combines heterogeneous public sources on wellbeing, inequality, emissions, energy use, material footprint, development status, income group, and geography. Building it required reshaping wide-format sources, standardising identifiers, resolving duplicated variables, aligning time coverage, and merging supplementary country metadata.

2. **The final clean dataset is balanced across retained countries and years.**  
   After cleaning, the dataset contains 558 observations: 62 countries observed annually from 2013 to 2021. This provides a consistent country-year panel for exploratory analysis.

3. **The dataset prioritises overlapping analytical completeness over maximum country coverage.**  
   Countries with substantial missingness across key wellbeing, inequality, emissions, material-footprint, and energy variables were removed. This reduced geographic breadth but improved the reliability and comparability of the final analytical dataset.

4. **The final sample is unevenly distributed across regions and development categories.**  
   European, high-income, and very-high-HDI countries are comparatively well represented, while some lower-income regions are less represented. This imbalance is an important limitation when interpreting global patterns.

5. **The dataset is suitable for multidimensional exploratory analysis, not full global generalisation.**  
   The final panel supports analysis of relationships between wellbeing, inequality, emissions, and material footprint, but findings should be interpreted as patterns within the retained analytical sample rather than as fully representative global conclusions.

---

#### Conceptual and exploratory findings

1. **Higher wellbeing is associated with higher environmental and material intensity, but with diminishing returns.**  
   Countries with higher average happiness often have higher consumption-based CO₂ emissions and material footprints. However, countries with extremely high environmental pressure are not proportionally happier than countries with substantially lower resource use.

2. **Production-based and consumption-based CO₂ are closely related but not interchangeable.**  
   The two emissions measures are strongly associated, but their gap reveals meaningful differences between consumption/import-oriented and production/export-oriented economies. This supports using consumption-based emissions when examining the environmental pressure associated with lifestyles and domestic consumption.

3. **Material footprint is especially informative for the decoupling question.**  
   Compared with CO₂ alone, material footprint more directly captures broader resource throughput. The EDA suggests that very high material consumption does not systematically correspond to higher subjective wellbeing once moderate levels of development and resource use are reached.

4. **Some countries appear comparatively wellbeing-efficient, but this does not imply that they optimise all dimensions.**  
   Countries such as Colombia, Brazil, Mexico, Chile, and Thailand often appear relatively favourable when happiness is considered against CO₂ emissions or material footprint. However, several of these countries also exhibit comparatively high inequality.

5. **Inequality substantially complicates the interpretation of subjective wellbeing.**  
   Countries with high average happiness may still experience substantial downward adjustment once income inequality is incorporated. This suggests that subjective wellbeing alone should not be interpreted as complete evidence of equitable flourishing or social cohesion.

6. **Few countries simultaneously combine high wellbeing, low material intensity, and low inequality.**  
   The percentile synthesis figure shows a sparse “ideal” region: high relative happiness, low relative material footprint, and low Gini. This is the central structural tension identified by the project.

7. **Within-country material-intensity changes show weak wellbeing effects.**  
   Short-run within-country changes in material footprint are only weakly associated with changes in raw or inequality-adjusted wellbeing. This suggests that much of the cross-country association between wellbeing and environmental intensity reflects broader structural differences rather than simple short-run gains from material intensification.

---

#### Insight-to-research-question mapping

| Key insight | Related research question(s) | How the insight addresses the question |
|---|---|---|
| A coherent country-year panel can be built from heterogeneous public sources, but only after substantial harmonisation. | Dataset RQ1: How can public datasets on wellbeing, inequality, emissions, energy use, material footprint, and country classifications be combined into a coherent country-year panel? | The setup and cleaning notebooks show that source-specific reshaping, identifier harmonisation, year filtering, and merge validation are necessary to construct the final analytical dataset. |
| The final dataset retains 62 countries over 2013–2021, producing 558 country-year observations. | Dataset RQ2: What countries and years can be retained when requiring overlapping information on wellbeing, inequality, emissions, material footprint, and energy use? | The cleaning process identifies the common analysis window and removes countries with insufficient overlapping data, producing a balanced 62 × 9 panel. |
| The retained sample is unevenly distributed across regions, income groups, and HDI categories. | Dataset RQ3: How is the resulting analytical dataset distributed across regions, income groups, and human development categories? | The dataset overview shows that European, high-income, and very-high-HDI countries are comparatively overrepresented. |
| Data availability constraints shape the interpretation of the project. | Dataset RQ4: What data availability constraints or representational imbalances should be considered when interpreting the final dataset? | The final dataset supports a clean multidimensional analysis, but the sample should not be treated as fully representative of all countries globally. |
| Higher subjective wellbeing is often associated with higher environmental and material intensity, but with diminishing returns. | Analysis RQ1: What is the relationship between subjective wellbeing and environmental or material pressure across countries? | The EDA shows a positive cross-country association, but also suggests that very high emissions or material footprint do not correspond to proportionally higher happiness. |
| Production-based and consumption-based CO₂ emissions are strongly related, but their gap reveals important trade-accounting differences. | Analysis RQ2: How do production-based and consumption-based CO₂ emissions differ, and what does this imply for cross-country environmental comparisons? | The CO₂ gap highlights countries whose consumption-based emissions exceed domestic production emissions, and vice versa, showing why both accounting approaches matter. |
| Material footprint is especially informative for the decoupling question. | Analysis RQ3: How does subjective wellbeing relate to material footprint per capita? | Material footprint captures broader resource throughput and shows strong evidence of saturation: beyond moderate levels, higher material consumption is not associated with substantially higher happiness. |
| Some countries appear comparatively wellbeing-efficient, but they do not necessarily optimise all dimensions. | Analysis RQ4: Which countries appear to achieve relatively high wellbeing with comparatively lower environmental or material pressure? | Countries such as Colombia, Brazil, Mexico, Chile, and Thailand often appear favourable on happiness-to-pressure comparisons, but this does not imply overall social or sustainability success. |
| Inequality substantially complicates the interpretation of subjective wellbeing. | Analysis RQ5: How does incorporating income inequality change the interpretation of national wellbeing outcomes? | Several countries with relatively high happiness experience substantial downward adjustment once inequality is incorporated, showing that subjective wellbeing alone may mask distributive tensions. |
| Few countries simultaneously combine high wellbeing, low material intensity, and low inequality. | Analysis RQ4 and Analysis RQ5 | The percentile synthesis figure shows that the desirable combination of high happiness, low material footprint, and low Gini is rare, suggesting a structural tension between wellbeing, sustainability, and equity. |
| Within-country material-intensity changes show weak wellbeing effects. | Analysis RQ6: Do within-country changes in material footprint correspond to changes in subjective or inequality-adjusted wellbeing over time? | Within-country plots suggest only weak relationships between material footprint changes and wellbeing changes, indicating that cross-country patterns should not be interpreted as simple short-run gains from material intensification. | 

### 7) Project structure

The repository is organised around a reproducible pipeline, modular source code, and notebooks that document the analytical reasoning behind each stage.

```
project/
├── main.py                         # Main orchestration script for the reproducible pipeline.
├── data/
│   ├── raw/                        # Original source datasets kept unchanged for reproducibility.
│   ├── processed_raw/              # Harmonised and merged intermediate raw dataset.
│   ├── processed/                  # Final cleaned, feature, and EDA-ready datasets.
│   └── supplementary/              # Supplementary metadata and country classification files.
├── notebooks/
│   ├── data_raw_setup.ipynb        # Documents raw data preparation and merging.
│   ├── data_cleaning.ipynb         # Documents cleaning, imputation, validation, and typing.
│   └── eda.ipynb                   # Documents feature construction, EDA, and final synthesis.
├── outputs/
│   └── eda_figures/                # Exported final figures supporting the main findings.
├── src/
│   ├── __init__.py                 # Marks src as a Python package.
│   ├── config.py                   # Centralised project paths and constants.
│   ├── io.py                       # Dataset loading, saving, and plot export utilities.
│   ├── setup.py                    # Raw source preparation and merged raw dataset construction.
│   ├── cleaning.py                 # Cleaning, imputation, validation, and type conversion.
│   ├── features.py                 # Core feature engineering.
│   ├── eda_features.py             # EDA-specific percentile and flag features.
│   ├── viz.py                      # Final reusable visualisation functions.
│   └── utils.py                    # General validation and helper utilities.
├── README.md                       # Project overview, methodology, findings, and usage instructions.
├── .gitignore                      # Files and folders excluded from version control.
└── requirements.txt                # Python dependencies required for the project.
````

### 8) Execution

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full reproducible pipeline:

```bash
python main.py
```

The pipeline rebuilds the processed datasets from the raw sources. Depending on the options set in `main.py`, it can also export:

- the EDA-ready dataset to `data/processed/sustainability_wellbeing_resource_data_eda.csv`
- the final exploratory figures to `outputs/eda_figures/`

The notebooks can be opened for the full documented workflow:

```bash
jupyter notebook notebooks/data_raw_setup.ipynb
jupyter notebook notebooks/data_cleaning.ipynb
jupyter notebook notebooks/eda.ipynb
```

The notebooks provide the narrative explanation and diagnostic reasoning, while `main.py` provides the reproducible end-to-end execution path.

### 9) Limitations

This project is exploratory and descriptive. It identifies patterns between wellbeing, inequality, emissions, material footprint, and resource use, but it does not make causal claims about the effects of environmental pressure or inequality on wellbeing.

The final dataset is balanced across the retained countries and years, but it is not globally representative. Countries with more complete overlapping data are more likely to be included, meaning that European, high-income, and very-high-HDI countries are comparatively well represented, while some lower-income regions are underrepresented.

The happiness index is based on subjective wellbeing and should be interpreted with care. Self-reported happiness may reflect adaptation, expectations, cultural response styles, social comparison, or normalised social conditions. High average happiness should therefore not be treated as complete evidence of equitable flourishing, social cohesion, or distributive justice.

The inequality-adjusted happiness feature is an exploratory project-specific measure rather than an official welfare metric. It is used to examine how incorporating income inequality changes the interpretation of subjective wellbeing, not to provide a definitive ranking of social welfare.

The environmental indicators capture related but distinct dimensions of impact. CO₂ emissions, consumption-based CO₂, energy use, and material footprint should not be treated as interchangeable. The final analysis focuses especially on consumption-based CO₂ and material footprint, but other impact indicators may produce different or additional insights.

Finally, the within-country analyses are descriptive. They help distinguish short-run within-country patterns from broader cross-country differences, but they do not replace formal panel modelling or causal inference.

### 10) Further research

Several extensions could strengthen and deepen the project.

- **Europe-focused analysis**  
  Europe is strongly represented in the final dataset. A Europe-only analysis could reduce some cross-country heterogeneity and provide a more comparable setting for exploring relationships between material footprint, emissions, inequality, and wellbeing.

- **Additional environmental indicators**  
  The dataset includes variables not central to the final EDA, including renewable energy consumption, energy per capita, temperature change from CO₂, share of global CO₂ emissions, and land-use-change CO₂. Future work could examine whether these indicators produce different interpretations of subjective and inequality-adjusted wellbeing.

- **Alternative inequality adjustments**  
  The current inequality-adjusted happiness measure uses a transparent Gini-based adjustment. Future work could test alternative transformations, weaker or stronger inequality penalties, or approaches that keep wellbeing and inequality as separate analytical dimensions.

- **Formal panel modelling**  
  A later stage could use panel regressions, country fixed effects, interaction terms, or region-restricted models to assess whether the descriptive patterns observed in the EDA persist under more formal statistical controls.

- **Alternative wellbeing measures**  
  Future analysis could compare subjective happiness with other wellbeing indicators, such as life expectancy, education, health, social trust, institutional quality, or multidimensional welfare measures.

- **Distributional and regional extensions**  
  Future work could examine whether the observed relationships differ by region, income group, development category, or production-consumption structure, especially in relation to countries that externalise environmental pressure through trade.

### 11) Conclusion

This project constructed a reproducible country-year dataset linking wellbeing, inequality, emissions, energy use, material footprint, development status, income group, and geography.

The analysis suggests that higher subjective wellbeing is often associated with higher environmental and material intensity, but with clear diminishing returns. It also shows that apparent wellbeing-efficiency changes substantially once inequality is considered.

Overall, the findings support a multidimensional view of progress: wellbeing, sustainability, and distributive equity should be evaluated together rather than through any single indicator in isolation.