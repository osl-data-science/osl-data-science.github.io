"""
Example fo how to create a dashboard.

Please, create also a **get_dash** function for your own implementation.
"""

from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go
import yaml

from plotly.subplots import make_subplots

from osl_data_science.datatools import download_and_extract_zip

__all__ = ['get_dash', 'metadata']

with open(Path(__file__).parent / 'metadata.yaml') as f:
    metadata = yaml.safe_load(f)


def get_data() -> None:
    download_url = 'https://www.kaggle.com/api/v1/datasets/download/gregorut/videogamesales'
    output_directory = './extracted_videogamesales'
    download_and_extract_zip(download_url, output_directory)


def get_dash() -> go.Figure:
    """Prepare and return a dashboard figure."""
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go

    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder

    # Load the dataset
    sales = pd.read_csv('vgsales.csv')

    # Step 1: Data Preprocessing
    # Check for missing values
    sales.isnull().sum()

    # Drop rows with missing 'Year' or other important fields
    sales.dropna(subset=['Year', 'Publisher'], inplace=True)

    # Encode categorical variables
    le = LabelEncoder()
    sales['Platform'] = le.fit_transform(sales['Platform'])
    sales['Genre'] = le.fit_transform(sales['Genre'])
    sales['Publisher'] = le.fit_transform(sales['Publisher'])

    # Convert 'Year' to integer
    sales['Year'] = sales['Year'].astype(int)

    # Step 2: Exploratory Data Analysis
    # Sales distribution by region
    region_sales = sales[
        ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
    ].sum()

    # Top genres by global sales
    top_genres = (
        sales.groupby('Genre')['Global_Sales']
        .sum()
        .sort_values(ascending=False)
    )

    # Top publishers by global sales
    top_publishers = (
        sales.groupby('Publisher')['Global_Sales']
        .sum()
        .sort_values(ascending=False)
    )

    # Step 3: Predictive Model
    # Define features and target
    X = sales[
        [
            'Platform',
            'Year',
            'Genre',
            'NA_Sales',
            'EU_Sales',
            'JP_Sales',
            'Other_Sales',
        ]
    ]
    y = sales['Global_Sales']

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train a Random Forest Regressor
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'Mean Squared Error: {mse}')
    print(f'R-squared: {r2}')

    # Step 4: Interactive Dashboard with Plotly
    fig = go.Figure()

    # Add bar chart for regional sales distribution
    fig.add_trace(
        go.Bar(
            x=region_sales.index,
            y=region_sales.values,
            name='Regional Sales Distribution',
        )
    )

    # Add bar chart for top genres
    fig.add_trace(
        go.Bar(
            x=top_genres.index,
            y=top_genres.values,
            name='Top Genres by Global Sales',
        )
    )

    # Add line chart for global sales trend over years
    yearly_sales = sales.groupby('Year')['Global_Sales'].sum()
    fig.add_trace(
        go.Scatter(
            x=yearly_sales.index,
            y=yearly_sales.values,
            mode='lines+markers',
            name='Global Sales Trend',
        )
    )

    # Update layout
    fig.update_layout(
        title='Video Games Sales Analysis',
        xaxis_title='Categories/Years',
        yaxis_title='Sales (in millions)',
        legend_title='Metrics',
        template='plotly_dark',
    )

    return fig
