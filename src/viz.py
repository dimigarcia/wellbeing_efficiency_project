from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.io import save_plot


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
):
    """
    Plot country-average happiness against consumption-based CO2.
    """

    plot_df = (
        df.groupby(
            ["country", "human_development_groups"],
            observed=True,
        )[
            [
                "happiness_index",
                "consumption_co2_per_capita",
            ]
        ]
        .mean()
        .reset_index()
    )

    median_happiness = (
        plot_df["happiness_index"]
        .median()
    )

    median_consumption = (
        plot_df["consumption_co2_per_capita"]
        .median()
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    sns.scatterplot(
        data=plot_df,
        x="consumption_co2_per_capita",
        y="happiness_index",
        hue="human_development_groups",
        s=90,
        alpha=0.8,
        ax=ax,
    )

    ax.axhline(
        median_happiness,
        linestyle="--",
        alpha=0.6,
    )

    ax.axvline(
        median_consumption,
        linestyle="--",
        alpha=0.6,
    )

    for _, row in plot_df.iterrows():

        if row["country"] in label_countries:

            ax.text(
                row["consumption_co2_per_capita"] + 0.15,
                row["happiness_index"] + 0.02,
                row["country"],
                fontsize=9,
            )

    ax.set_xlabel(
        "Average consumption-based CO₂ per capita"
    )

    ax.set_ylabel(
        "Average happiness index"
    )

    ax.set_title(
        "Average happiness vs consumption-based CO₂"
    )

    ax.legend(title="HDI group")

    return fig


def plot_happiness_vs_material_footprint(
    df: pd.DataFrame,
    label_countries: list[str] = LABEL_COUNTRIES,
):
    """
    Plot country-average happiness against material footprint.
    """

    plot_df = (
        df.groupby(
            ["country", "human_development_groups"],
            observed=True,
        )[
            [
                "happiness_index",
                "material_footprint_per_capita",
            ]
        ]
        .mean()
        .reset_index()
    )

    median_happiness = (
        plot_df["happiness_index"]
        .median()
    )

    median_material = (
        plot_df["material_footprint_per_capita"]
        .median()
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    sns.scatterplot(
        data=plot_df,
        x="material_footprint_per_capita",
        y="happiness_index",
        hue="human_development_groups",
        s=90,
        alpha=0.8,
        ax=ax,
    )

    ax.axhline(
        median_happiness,
        linestyle="--",
        alpha=0.6,
    )

    ax.axvline(
        median_material,
        linestyle="--",
        alpha=0.6,
    )

    for _, row in plot_df.iterrows():

        if row["country"] in label_countries:

            ax.text(
                row["material_footprint_per_capita"] + 0.5,
                row["happiness_index"] + 0.02,
                row["country"],
                fontsize=9,
            )

    ax.set_xlabel(
        "Average material footprint per capita"
    )

    ax.set_ylabel(
        "Average happiness index"
    )

    ax.set_title(
        "Average happiness vs material footprint"
    )

    ax.legend(title="HDI group")

    return fig


def plot_percentile_synthesis(
    df: pd.DataFrame,
    label_countries: list[str] = LABEL_COUNTRIES,
):
    """
    Plot relative happiness, relative material footprint,
    and inequality.
    """

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

    fig, ax = plt.subplots(figsize=(9, 8))

    scatter = ax.scatter(
        plot_df[
            "material_footprint_percentile_by_year"
        ],
        plot_df[
            "happiness_percentile_by_year"
        ],
        c=plot_df["gini_index"],
        s=90,
        alpha=0.85,
    )

    ax.axhline(
        0.5,
        linestyle="--",
        alpha=0.5,
    )

    ax.axvline(
        0.5,
        linestyle="--",
        alpha=0.5,
    )

    for _, row in plot_df.iterrows():

        if row["country"] in label_countries:

            ax.text(
                row[
                    "material_footprint_percentile_by_year"
                ] + 0.01,
                row[
                    "happiness_percentile_by_year"
                ] + 0.01,
                row["country"],
                fontsize=9,
            )

    cbar = fig.colorbar(
        scatter,
        ax=ax,
    )

    cbar.set_label(
        "Average Gini index"
    )

    ax.set_xlabel(
        "Average material footprint percentile"
    )

    ax.set_ylabel(
        "Average happiness percentile"
    )

    ax.set_title(
        "Relative happiness, material footprint, and inequality"
    )

    return fig


def prepare_within_country_deviations(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add within-country deviations used in final
    within-country plots.
    """

    fe_df = df.copy()

    fe_df[
        "material_footprint_within_country"
    ] = (
        fe_df["material_footprint_per_capita"]
        - fe_df.groupby("country")[
            "material_footprint_per_capita"
        ].transform("mean")
    )

    fe_df[
        "happiness_within_country"
    ] = (
        fe_df["happiness_index"]
        - fe_df.groupby("country")[
            "happiness_index"
        ].transform("mean")
    )

    fe_df[
        "ineq_adj_happiness_within_country"
    ] = (
        fe_df["inequality_adjusted_happiness"]
        - fe_df.groupby("country")[
            "inequality_adjusted_happiness"
        ].transform("mean")
    )

    median_co2_gap = (
        fe_df[
            "co2_consumption_production_gap"
        ]
        .median()
    )

    fe_df["co2_gap_group"] = np.where(
        fe_df[
            "co2_consumption_production_gap"
        ] >= median_co2_gap,
        "Net consumption/import-oriented",
        "Net production/export-oriented",
    )

    return fe_df


def plot_within_country_happiness_by_co2_gap(
    df: pd.DataFrame,
):
    """
    Plot within-country material footprint vs happiness
    by CO2 gap group.
    """

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
        "Within-country relationship between happiness "
        "and material footprint\n"
        "by CO₂ trade-balance structure"
    )

    return g.fig


def plot_within_country_adjusted_happiness_by_co2_gap(
    df: pd.DataFrame,
):
    """
    Plot within-country material footprint vs adjusted
    happiness by CO2 gap group.
    """

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
        "Within-country relationship between adjusted wellbeing "
        "and material footprint\n"
        "by CO₂ trade-balance structure"
    )

    return g.fig


def plot_main_exploratory_findings(
    df: pd.DataFrame,
    output_dir: Path | None = None,
) -> None:
    """
    Produce the final core EDA figures used to support the
    main exploratory findings and research-question synthesis.
    """

    figures = [
        (
            plot_happiness_vs_consumption_co2(df),
            "happiness_vs_consumption_co2.png",
        ),
        (
            plot_happiness_vs_material_footprint(df),
            "happiness_vs_material_footprint.png",
        ),
        (
            plot_percentile_synthesis(df),
            "percentile_synthesis.png",
        ),
        (
            plot_within_country_happiness_by_co2_gap(df),
            "within_country_happiness_by_co2_gap.png",
        ),
        (
            plot_within_country_adjusted_happiness_by_co2_gap(df),
            "within_country_adjusted_happiness_by_co2_gap.png",
        ),
    ]

    for fig, filename in figures:

        if output_dir is not None:

            save_plot(
                fig,
                filename,
                output_dir,
            )

        plt.close(fig)