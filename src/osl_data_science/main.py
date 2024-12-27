"""Dashboard Generator."""

from __future__ import annotations

import importlib

from pathlib import Path
from typing import Callable, Dict, List, cast

import plotly.graph_objects as go

from jinja2 import Environment, FileSystemLoader
from typing_extensions import TypeAlias

FnGetFigure: TypeAlias = Callable[[], go.Figure]
MetaData: TypeAlias = Dict[str, str]
DashboardType: TypeAlias = List[Dict[str, MetaData | FnGetFigure]]

STATIC_DIR = Path(__file__).parent.parent.parent / 'pages'
STATIC_DASHBOARDS_DIR = STATIC_DIR / 'projects'
TEMPLATES_DIR = Path(__file__).parent / 'templates'
DASHBOARDS_DIR = Path(__file__).parent / 'projects'


def get_dashboards(
    dashboard_dir: Path = DASHBOARDS_DIR,
) -> DashboardType:
    """Retrieve dashboard metadata and `get_dash` functions."""
    dashboards = []

    # Iterate over all subdirectories in the dashboards directory
    for subdir in dashboard_dir.iterdir():
        if (
            not subdir.is_dir()
            or not (subdir / '__init__.py').exists()
            or subdir.name == 'example'
        ):
            continue

        # Import the module dynamically
        package_name = subdir.name.replace('-', '_')
        package_qualname = f'osl_data_science.projects.{package_name}'
        module = importlib.import_module(package_qualname)

        # Check if the module has `metadata` and `get_dash`
        if hasattr(module, 'metadata') and hasattr(module, 'get_dash'):
            dashboards.append(
                {
                    'metadata': module.metadata,
                    'fn': module.get_dash,
                }
            )
        else:
            print(
                'Warning: Not found `metadata` or `get_dash` '
                'inside package {package_qualname}.'
            )

    return dashboards


def generate_index(dashboards: DashboardType) -> None:
    """Generate the index page using dashboard metadata."""
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template('index.md.tpl')

    dashboards_data = [dashboard['metadata'] for dashboard in dashboards]

    rendered_content = template.render(dashboards=dashboards_data)

    output_file = STATIC_DIR / 'projects' / 'index.md'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(rendered_content, encoding='utf-8')


def generate_dash(
    name: str, metadata: MetaData, get_figure: FnGetFigure
) -> None:
    """Generate the dashboard HTML and Markdown files."""
    dash_dir = STATIC_DASHBOARDS_DIR / metadata['slug']
    dash_html = dash_dir / 'index.html'
    dash_md = dash_dir / 'index.md'

    # Template for the Markdown file linking to the HTML
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    dash_index_md_tpl = env.get_template('dashboard.md.tpl')

    dash_dir.mkdir(parents=True, exist_ok=True)

    # Generate the HTML file
    get_figure().write_html(
        dash_html,
        include_plotlyjs=False,
        full_html=False,
    )

    # Generate the Markdown file
    with open(dash_md, 'w') as f:
        f.write(dash_index_md_tpl.render(metadata))


def main() -> None:
    """Orchestrate dashboard generation."""
    dashboards = get_dashboards()

    # Generate the index file
    generate_index(dashboards)

    # Generate each dashboard
    for dashboard in dashboards:
        metadata = cast(MetaData, dashboard['metadata'])
        get_figure = cast(FnGetFigure, dashboard['fn'])
        generate_dash(str(metadata['title']), metadata, get_figure)


if __name__ == '__main__':
    main()
