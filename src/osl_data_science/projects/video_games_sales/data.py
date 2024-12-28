"""Set of functions for handling the data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from osl_data_science.datatools import (
    download_and_extract_zip,
)

PROJECT_DIR = Path(__file__).parent


def extract_data() -> None:
    """Extract the data needed for the current analysis."""
    download_url = 'https://www.kaggle.com/api/v1/datasets/download/gregorut/videogamesales'
    output_directory = PROJECT_DIR / 'data'
    download_and_extract_zip(download_url, output_directory)


def get_raw_data() -> pd.DataFrame:
    """Return the raw data in dataframe format."""
    extract_data()
    return pd.read_csv(PROJECT_DIR / 'data' / 'vgsales.csv')


def prepare_data(sales: pd.DataFrame) -> pd.DataFrame:
    """Prepare the data for the analysis and for the ML training."""
    sales = sales.copy()

    # Drop missing values in critical columns
    sales.dropna(subset=['Year', 'Publisher'], inplace=True)

    # Convert Year to integer
    sales['Year'] = sales['Year'].astype(int)

    # Encode categorical variables and retain mapping
    genre_category = sales['Genre'].astype('category')
    sales['Genre'] = genre_category.cat.codes
    sales['Genre_Mapping'] = genre_category.cat.categories[
        sales['Genre']
    ].values  # Map encoded genres back to names

    sales['Platform'] = sales['Platform'].astype('category').cat.codes
    sales['Publisher'] = sales['Publisher'].astype('category').cat.codes

    return sales


def get_eda_info(sales: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Use the given data to return some interesting data."""
    # Regional sales distribution
    region_sales = sales[
        ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    ].sum()

    # Global sales trend over years
    yearly_sales = sales.groupby('Year')['Global_Sales'].sum()

    # Top genres (use human-readable names)
    top_genres = (
        sales.groupby('Genre_Mapping')['Global_Sales']
        .sum()
        .sort_values(ascending=False)
    )

    # Top platforms
    top_platforms = (
        sales.groupby('Platform')['Global_Sales']
        .sum()
        .sort_values(ascending=False)
    )

    # Correlation heatmap
    correlation_matrix = sales[
        ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    ].corr()

    return {
        'region_sales': region_sales,
        'yearly_sales': yearly_sales,
        'top_genres': top_genres,
        'top_platforms': top_platforms,
        'correlation_matrix': correlation_matrix,
    }
