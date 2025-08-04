"""Functionality related to TAS diagram file upload handling."""

import base64
import io

import pandas as pd
from dash import dcc
from dash import html
from geoplotnik.components.ids import DATA_UPLOAD_AREA


def render() -> html.Div:
    """Render the uploader's UI."""
    return html.Div(
        [
            dcc.Upload(
                id=DATA_UPLOAD_AREA,
                children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                multiple=False,
            ),
        ],
    )
