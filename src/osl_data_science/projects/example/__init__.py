"""
Example fo how to create a dashboard.

Please, create also a **get_dash** function for your own implementation.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .dash import get_dash

__all__ = ['get_dash', 'metadata']

with open(Path(__file__).parent / 'metadata.yaml') as f:
    metadata = yaml.safe_load(f)
