"""
Example fo how to create a dashboard.

Please, create also a **get_dash** function for your own implementation.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .dash import generate_dash

__all__ = ['generate_dash', 'metadata']

PROJECT_DIR = Path(__file__).parent

with open(PROJECT_DIR / 'metadata.yaml') as f:
    metadata = yaml.safe_load(f)
