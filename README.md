# Exploring Sustainable Wellbeing: A Cross-Country Analysis of Resource Use, Emissions and Quality of Life

## <p align="center">🚧 Work in progress 🚧</p>

### 1) Objective
The objective of this project is to build a coherent cross-country dataset by merging multiple public data sources related to wellbeing, inequality, economic development, energy use, emissions, and material consumption.  

Using this merged dataset, the project applies data cleaning, transformation, feature engineering, and visualization techniques to explore whether countries can achieve high levels of wellbeing with lower environmental and material impact.  

The analysis aims to demonstrate a complete and reproducible data analysis workflow, from raw heterogeneous datasets to interpretable insights and visual exploration of potential decoupling between quality of life and resource consumption.

### 2) Dataset
- We build the *Global Wellbeing, Sustainability and Resource Use Dataset* drawing on various public data sources.
- Sources:
- Coverage: 2013 - 2021
- Rows/columns: Variable (depende del archivo cargado)
- Key variables:

### 3) Questions
- Q1: 
- Q2: 
- Q3:
- ...

### 4) Data issues & fixes
- Several data sources with inconsistent wide format → Wide-to-long transformation.
- Different years of coverage per data source → Identify overlap window and constrain dataset within it.
- Inconsistent/Missing ISO Country codes for merging → Normalisation of merge keys accross all 5 datasets.
- Unmerged data → Merging the data correclty into a final single raw dataset.

### 5) Pipeline
- pre-merge raw → merged raw → clean → features → viz → (export opcional a `data/processed/`)

### 6) Hallazgos
- Insight 1: 
- Insight 2: 
- Insight 3: 

### 7) Estructura del proyecto
- `src/` contiene funciones reutilizables (`io`, `cleaning`, `features`, `viz`)
- `main.py` ejecuta el pipeline end-to-end

### 8) Execution
- `pip install -r requirements.txt`
- Execute pipeline: `python main.py`
- (Optional) Open and execute: `notebooks/eda.ipynb`

## Project structure

Estructura sugerida:

```
project/
├── main.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
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