"""Dashboard Generator."""

from __future__ import annotations

import re

from pathlib import Path
from typing import Dict, List

import yaml

from jinja2 import BaseLoader, Environment
from typing_extensions import TypeAlias


def extract_yaml_header(qmd_content):
    """Extracts the YAML header from a Quarto (QMD) file."""
    match = re.search(r'^---\n(.*?)\n---', qmd_content, re.DOTALL)
    if match:
        return match.group(1)
    return None


def parse_yaml_header(qmd_file_path):
    """Reads a QMD file, extracts and parses the YAML header into a dictionary."""
    with open(qmd_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    yaml_header = extract_yaml_header(content)
    if yaml_header:
        return yaml.safe_load(yaml_header)
    return {}


MetaData: TypeAlias = Dict[str, str]
DashboardType: TypeAlias = List[str]

STATIC_DIR = Path(__file__).parent.parent.parent / 'pages'
STATIC_DASHBOARDS_DIR = STATIC_DIR / 'projects'
DASHBOARDS_DIR = STATIC_DASHBOARDS_DIR


TEMPLATE_INDEX_FILE = """
# OSL Data Science Projects Gallery

**Welcome to our Project Gallery!**

Here, you can explore a variety of data science
projects affiliated to the OSL Data Science Internship Program.
Each project showcased here utilizes open data and is freely available as
open-source, embodying our commitment to transparency and collaboration in
science.

<div class="container mt-4">
    <div class="row">
        {% for dash in dashboards %}
        <div class="col-md-12 col-lg-6 col-xl-4">
            <div class="card mb-4 p-0">
                <img src="{{ dash.image.strip() }}" class="card-img-top my-0" alt="{{ dash.title.strip() }}">
                <div class="card-body">
                    <h5 class="card-title">{{ dash.title.strip() }}</h5>
                    <p class="card-text">{{ dash.description.strip() }}</p>
                    <a href="/projects/{{ dash.slug }}/" target="_blank" class="btn btn-primary">View Dashboard</a>
                    <a href="{{ dash.source_code_url }}/" target="_blank" class="btn btn-dark">Source Code</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
"""


def get_dashboards(
    dashboard_dir: Path = DASHBOARDS_DIR,
) -> DashboardType:
    """Retrieve dashboard metadata and `get_dash` functions."""
    dashboards = []

    # Iterate over all subdirectories in the dashboards directory
    for subdir in dashboard_dir.iterdir():
        if (
            not subdir.is_dir() or not (subdir / 'index.qmd').exists()
            # or subdir.name == 'example'
        ):
            continue
        dashboards.append(subdir)

    return dashboards


def generate_index(dashboards: DashboardType) -> None:
    """Generate the index page using dashboard metadata."""
    template = Environment(loader=BaseLoader).from_string(TEMPLATE_INDEX_FILE)

    dashboards_data = [dashboard['metadata'] for dashboard in dashboards]

    rendered_content = template.render(dashboards=dashboards_data)

    output_file = STATIC_DIR / 'projects' / 'index.md'
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(rendered_content, encoding='utf-8')


def main() -> None:
    """Orchestrate dashboard generation."""
    dashboards = get_dashboards()

    generate_index(dashboards)


if __name__ == '__main__':
    main()
