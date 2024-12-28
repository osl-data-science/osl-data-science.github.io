"""Dashboard module."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from plotly.subplots import make_subplots


def get_dash() -> go.Figure:
    """Prepare and return a dashboard figure."""
    # note: you can load the data and train and predict info
    #       from your data here, e.g.:
    # df = get_data()
    # results = train(df)

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            'Sales Over Time',
            'Revenue Breakdown',
            'Customer Distribution',
            'Profit Trends',
        ),
        specs=[
            [{'type': 'xy'}, {'type': 'xy'}],
            [{'type': 'domain'}, {'type': 'xy'}],
        ],
    )

    fig.add_trace(
        go.Scatter(
            x=[2020, 2021, 2022, 2023],
            y=[100, 150, 200, 250],
            mode='lines+markers',
            name='Sales',
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            x=['Product A', 'Product B', 'Product C'],
            y=[50, 100, 150],
            name='Revenue',
        ),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Pie(
            labels=['Region 1', 'Region 2', 'Region 3'],
            values=[30, 50, 20],
            name='Customers',
        ),
        row=2,
        col=1,  # Place the pie chart in the first column of the second row
    )

    fig.add_trace(
        go.Heatmap(
            z=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            x=['Q1', 'Q2', 'Q3'],
            y=['2019', '2020', '2021'],
            colorscale='Viridis',
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        title='OSL Data Science: Dashboard Example',
        height=800,
        width=np.inf,
        showlegend=True,
    )

    return fig
