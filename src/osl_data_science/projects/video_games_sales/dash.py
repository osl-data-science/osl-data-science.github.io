"""Dashboard module."""

from __future__ import annotations

from pathlib import Path

import plotly.graph_objects as go

from .data import get_eda_info, get_raw_data, prepare_data
from .model import train


def get_dash_html() -> str:
    """Generate the dashboard HTML for video game sales analysis."""
    # Prepare data
    sales = get_raw_data()
    sales = prepare_data(sales)
    eda_info = get_eda_info(sales)

    region_sales = eda_info['region_sales']
    yearly_sales = eda_info['yearly_sales']
    top_genres = eda_info['top_genres']

    train(sales)

    # Create individual figures
    # Regional Sales Distribution
    region_fig = go.Figure()
    region_fig.add_trace(
        go.Bar(
            x=region_sales.index,
            y=region_sales.values,
            marker_color='steelblue',
        )
    )
    region_fig.update_layout(
        title='Regional Sales Distribution',
        xaxis_title='Regions',
        yaxis_title='Sales (in millions)',
        template='plotly_white',
    )

    # Global Sales Trend Over Years
    trend_fig = go.Figure()
    trend_fig.add_trace(
        go.Scatter(
            x=yearly_sales.index,
            y=yearly_sales.values,
            mode='lines+markers',
            marker=dict(color='darkorange'),
        )
    )
    trend_fig.update_layout(
        title='Global Sales Trend Over Years',
        xaxis_title='Year',
        yaxis_title='Sales (in millions)',
        template='plotly_white',
    )

    # Market Share by Genre
    genre_fig = go.Figure()
    genre_fig.add_trace(
        go.Pie(
            labels=top_genres.index,
            values=top_genres.values,
            textinfo='label+percent',
        )
    )
    genre_fig.update_layout(
        title='Market Share by Genre',
        template='plotly_white',
    )

    # Top Games by Global Sales
    top_games = sales.nlargest(10, 'Global_Sales')
    games_fig = go.Figure()
    games_fig.add_trace(
        go.Scatter(
            x=top_games['Name'],
            y=top_games['Global_Sales'],
            mode='markers+text',
            text=top_games['Name'],
            marker=dict(size=15, color='mediumseagreen'),
        )
    )
    games_fig.update_layout(
        title='Top Games by Global Sales',
        xaxis_title='Game Titles',
        yaxis_title='Global Sales (in millions)',
        template='plotly_white',
    )

    # Sales by Platform per Year
    year_threshold = 2010
    filtered_sales = sales[sales['Year'] >= year_threshold]
    platform_mapping = sales[
        ['Platform', 'Platform_Mapping']
    ].drop_duplicates()
    platform_mapping = dict(
        zip(platform_mapping['Platform'], platform_mapping['Platform_Mapping'])
    )

    platform_year_sales = (
        filtered_sales.groupby(['Year', 'Platform'])['Global_Sales']
        .sum()
        .unstack(fill_value=0)
    )

    # Map platform IDs back to names and keep only used platforms
    platform_year_sales.columns = platform_year_sales.columns.map(
        platform_mapping
    )

    platform_fig = go.Figure()
    for platform in platform_year_sales.columns:
        platform_fig.add_trace(
            go.Bar(
                x=platform_year_sales.index,
                y=platform_year_sales[platform],
                name=platform,
            )
        )
    platform_fig.update_layout(
        title=f'Sales by Platform Per Year (From {year_threshold})',
        xaxis_title='Year',
        yaxis_title='Sales (in millions)',
        barmode='stack',  # Stack bars for better comparison
        template='plotly_white',
    )

    # Combine HTML for all figures with custom layout
    html_content = (
        '## Regional Sales Distribution\n\n'
        f'{region_fig.to_html(full_html=False, include_plotlyjs=False)}\n\n'
        '## Global Sales Trend Over Years\n\n'
        f'{trend_fig.to_html(full_html=False, include_plotlyjs=False)}\n\n'
        '## Market Share by Genre\n\n'
        f'{genre_fig.to_html(full_html=False, include_plotlyjs=False)}\n\n'
        '## Top Games by Global Sales\n\n'
        f'{games_fig.to_html(full_html=False, include_plotlyjs=False)}\n\n'
        f'## Sales by Platform Per Year (From {year_threshold})\n\n'
        f'{platform_fig.to_html(full_html=False, include_plotlyjs=False)}\n'
    )
    return html_content.strip()


def generate_dash(output_path: Path) -> None:
    """Save the dashboard HTML to a file."""
    html_content = get_dash_html()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
