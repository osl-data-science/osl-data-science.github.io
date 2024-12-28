"""Prepare models for the prediction."""

from __future__ import annotations

import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def train(sales: pd.DataFrame) -> dict[str, float | pd.Series]:
    """Train a ML model with data from the dataframe."""
    # Features and target
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

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Predictions and evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'Mean Squared Error: {mse}')
    print(f'R-squared: {r2}')

    return {
        'y_pred': y_pred,
        'mse': mse,
        'r2': r2,
    }
