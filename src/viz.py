import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


LABEL_COUNTRIES = [
    "Brazil",
    "Colombia",
    "Mexico",
    "Denmark",
    "Switzerland",
    "United States",
    "Vietnam",
    "Sri Lanka",
]


def plot_happiness_vs_consumption_co2(
    df: pd.DataFrame,
    label_countries: list[str] = LABEL_COUNTRIES,
) -> None:
    """Plot country-average happiness against consumption-based CO2."""

    plot_df = (
        df.groupby(["country", "human_development_groups"], observed=True)[
            [
                "happiness_index",
                "consumption_co2_per_capita",
            ]
        ]
        .mean()
        .reset_index()
    )

    median_happiness = plot_df["happiness_index"].median()

    median_consumption = plot_df[
        "consumption_co2_per_capita"
    ].median()

    plt.figure(figsize=(10, 8))

    sns.scatterplot(
        data=plot_df,
        x="consumption_co2_per_capita",
        y="happiness_index",
        hue="human_development_groups",
        s=90,
        alpha=0.8,
    )

    plt.axhline(
        median_happiness,
        linestyle="--",
        alpha=0.6,
    )

    plt.axvline(
        median_consumption,
        linestyle="--",
        alpha=0.6,
    )

    for _, row in plot_df.iterrows():
        if row["country"] in label_countries:
            plt.text(
                row["consumption_co2_per_capita"] + 0.15,
                row["happiness_index"] + 0.02,
                row["country"],
                fontsize=9,
            )

    plt.xlabel("Average consumption-based CO₂ per capita")
    plt.ylabel("Average happiness index")

    plt.title(
        "Average happiness vs consumption-based CO₂"
    )

    plt.legend(title="HDI group")

    plt.show()

def plot_happiness_vs_material_footprint(
    df: pd.DataFrame,
    label_countries: list[str] = LABEL_COUNTRIES,
) -> None:
    """Plot country-average happiness against material footprint."""

    plot_df = (
        df.groupby(["country", "human_development_groups"], observed=True)[
            [
                "happiness_index",
                "material_footprint_per_capita",
            ]
        ]
        .mean()
        .reset_index()
    )

    median_happiness = plot_df["happiness_index"].median()

    median_material = plot_df[
        "material_footprint_per_capita"
    ].median()

    plt.figure(figsize=(10, 8))

    sns.scatterplot(
        data=plot_df,
        x="material_footprint_per_capita",
        y="happiness_index",
        hue="human_development_groups",
        s=90,
        alpha=0.8,
    )

    plt.axhline(
        median_happiness,
        linestyle="--",
        alpha=0.6,
    )

    plt.axvline(
        median_material,
        linestyle="--",
        alpha=0.6,
    )

    for _, row in plot_df.iterrows():
        if row["country"] in label_countries:
            plt.text(
                row["material_footprint_per_capita"] + 0.5,
                row["happiness_index"] + 0.02,
                row["country"],
                fontsize=9,
            )

    plt.xlabel("Average material footprint per capita")
    plt.ylabel("Average happiness index")

    plt.title(
        "Average happiness vs material footprint"
    )

    plt.legend(title="HDI group")

    plt.show()

def plot_percentile_synthesis(
    df: pd.DataFrame,
    label_countries: list[str] = LABEL_COUNTRIES,
) -> None:
    """Plot relative happiness, relative material footprint, and inequality."""

    plot_df = (
        df.groupby("country")[
            [
                "happiness_percentile_by_year",
                "material_footprint_percentile_by_year",
                "gini_index",
            ]
        ]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(9, 8))

    scatter = plt.scatter(
        plot_df["material_footprint_percentile_by_year"],
        plot_df["happiness_percentile_by_year"],
        c=plot_df["gini_index"],
        s=90,
        alpha=0.85,
    )

    plt.axhline(0.5, linestyle="--", alpha=0.5)
    plt.axvline(0.5, linestyle="--", alpha=0.5)

    for _, row in plot_df.iterrows():
        if row["country"] in label_countries:
            plt.text(
                row["material_footprint_percentile_by_year"] + 0.01,
                row["happiness_percentile_by_year"] + 0.01,
                row["country"],
                fontsize=9,
            )

    plt.colorbar(scatter, label="Average Gini index")
    plt.xlabel("Average material footprint percentile")
    plt.ylabel("Average happiness percentile")
    plt.title("Relative happiness, material footprint, and inequality")
    plt.show()


def prepare_within_country_deviations(df: pd.DataFrame) -> pd.DataFrame:
    """Add within-country deviations used in final within-country plots."""

    fe_df = df.copy()

    fe_df["material_footprint_within_country"] = (
        fe_df["material_footprint_per_capita"]
        - fe_df.groupby("country")[
            "material_footprint_per_capita"
        ].transform("mean")
    )

    fe_df["happiness_within_country"] = (
        fe_df["happiness_index"]
        - fe_df.groupby("country")[
            "happiness_index"
        ].transform("mean")
    )

    fe_df["ineq_adj_happiness_within_country"] = (
        fe_df["inequality_adjusted_happiness"]
        - fe_df.groupby("country")[
            "inequality_adjusted_happiness"
        ].transform("mean")
    )

    median_co2_gap = fe_df["co2_consumption_production_gap"].median()

    fe_df["co2_gap_group"] = np.where(
        fe_df["co2_consumption_production_gap"] >= median_co2_gap,
        "Net consumption/import-oriented",
        "Net production/export-oriented",
    )

    return fe_df


def plot_within_country_happiness_by_co2_gap(
    df: pd.DataFrame,
) -> None:
    """Plot within-country material footprint vs happiness by CO2 gap group."""

    fe_df = prepare_within_country_deviations(df)

    g = sns.lmplot(
        data=fe_df,
        x="material_footprint_within_country",
        y="happiness_within_country",
        col="co2_gap_group",
        height=5,
        aspect=1.1,
        scatter_kws={"alpha": 0.4},
        line_kws={"color": "red"},
    )

    g.set_axis_labels(
        "Within-country deviation in material footprint",
        "Within-country deviation in happiness",
    )

    g.fig.subplots_adjust(top=0.78)

    g.fig.suptitle(
        "Within-country relationship between happiness and material footprint\n"
        "by CO₂ trade-balance structure"
    )

    plt.show()


def plot_within_country_adjusted_happiness_by_co2_gap(
    df: pd.DataFrame,
) -> None:
    """Plot within-country material footprint vs adjusted happiness by CO2 gap group."""

    fe_df = prepare_within_country_deviations(df)

    g = sns.lmplot(
        data=fe_df,
        x="material_footprint_within_country",
        y="ineq_adj_happiness_within_country",
        col="co2_gap_group",
        height=5,
        aspect=1.1,
        scatter_kws={"alpha": 0.4},
        line_kws={"color": "red"},
    )

    g.set_axis_labels(
        "Within-country deviation in material footprint",
        "Within-country deviation in inequality-adjusted happiness",
    )

    g.fig.subplots_adjust(top=0.78)

    g.fig.suptitle(
        "Within-country relationship between adjusted wellbeing and material footprint\n"
        "by CO₂ trade-balance structure"
    )

    plt.show()

def plot_main_exploratory_findings(df: pd.DataFrame) -> None:
    """
    Produce the final core EDA figures used to support the main
    exploratory findings and research-question synthesis.
    """

    plot_happiness_vs_consumption_co2(df)

    plot_happiness_vs_material_footprint(df)

    plot_percentile_synthesis(df)

    plot_within_country_happiness_by_co2_gap(df)

    plot_within_country_adjusted_happiness_by_co2_gap(df)