"""Dashboard module."""

from __future__ import annotations

import plotly.graph_objects as go

from plotly.subplots import make_subplots

from .data import get_eda_info, get_raw_data, prepare_data
from .model import train


def get_dash() -> go.Figure:
    """Generate the dashboard figure for video game sales analysis."""
    # Prepare data
    sales = get_raw_data()
    sales = prepare_data(sales)
    eda_info = get_eda_info(sales)

    region_sales = eda_info.get('region_sales')
    yearly_sales = eda_info.get('yearly_sales')
    top_genres = eda_info.get('top_genres')
    # top_platforms = eda_info.get('top_platforms')

    train(sales)

    # Create subplots layout (2 rows, 2 columns)
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            'Regional Sales Distribution',
            'Global Sales Trend Over Years',
            'Market Share by Genre',
            'Top Games by Global Sales',
        ],
        specs=[
            [{'type': 'bar'}, {'type': 'scatter'}],
            [{'type': 'pie'}, {'type': 'scatter'}],
        ],
    )

    fig.add_trace(
        go.Bar(
            x=region_sales.index,
            y=region_sales.values,
            name='Regional Sales',
            marker_color='steelblue',
        ),
        row=1,
        col=1,
    )

    # Add Line Chart: Global sales trend over years
    fig.add_trace(
        go.Scatter(
            x=yearly_sales.index,
            y=yearly_sales.values,
            mode='lines+markers',
            name='Global Sales Trend',
            marker=dict(color='darkorange'),
            line=dict(width=2),
        ),
        row=1,
        col=2,
    )

    # Add Pie Chart: Market share by genre
    fig.add_trace(
        go.Pie(
            labels=top_genres.index,
            values=top_genres.values,
            name='Genre Market Share',
            textinfo='label+percent',
            insidetextorientation='radial',
        ),
        row=2,
        col=1,
    )

    # Add Scatter Plot: Top games by global sales
    top_games = sales.nlargest(
        10, 'Global_Sales'
    )  # Show only top 10 for clarity
    fig.add_trace(
        go.Scatter(
            x=top_games['Name'],
            y=top_games['Global_Sales'],
            mode='markers+text',
            text=top_games['Name'],  # Show game names as tooltips
            marker=dict(size=15, color='mediumseagreen'),
            name='Top Games',
        ),
        row=2,
        col=2,
    )

    # Update layout for the entire figure
    fig.update_layout(
        title=dict(
            text='Video Games Sales Analysis Dashboard',
            x=0.5,  # Center align the title
            font=dict(size=20),
        ),
        height=900,  # Adjust height to fit all subplots
        width=1100,  # Set appropriate width
        showlegend=True,
        legend=dict(
            orientation='h',
            x=0.5,
            xanchor='center',
            y=-0.1,
        ),
        template='plotly_white',
    )

    # Update axis titles
    fig.update_xaxes(title_text='Regions', row=1, col=1)
    fig.update_yaxes(title_text='Sales (in millions)', row=1, col=1)
    fig.update_xaxes(title_text='Year', row=1, col=2)
    fig.update_yaxes(title_text='Sales (in millions)', row=1, col=2)
    fig.update_xaxes(title_text='Game Titles', row=2, col=2)
    fig.update_yaxes(title_text='Global Sales (in millions)', row=2, col=2)

    return fig
