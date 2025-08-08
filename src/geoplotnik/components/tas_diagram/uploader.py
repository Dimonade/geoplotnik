"""Functionality related to TAS diagram file upload handling."""

import base64
import io

import pandas as pd
from dash import dcc
from dash import html
from geoplotnik.components.ids import DATA_LOADER_BUTTON
from geoplotnik.components.ids import DATA_UPLOAD_AREA
from geoplotnik.components.ids import URL_INPUT


def render() -> html.Div:
    """Render the uploader's UI."""
    return html.Div(
        children=[
            dcc.Upload(
                id=DATA_UPLOAD_AREA,
                children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                style={
                    "height": "50px",
                    "line-height": "50px",
                    "border-width": "1px",
                    "border-style": "dashed",
                    "border-radius": "5px",
                    "text-align": "center",
                    "padding": "0 10px",
                },
                multiple=False,
            ),
            html.Div("... or ..."),
            html.Div(
                [
                    dcc.Input(
                        id=URL_INPUT,
                        type="text",
                        debounce=True,
                        placeholder="Paste URL or file path...",
                        style={"flex": "1"},
                    ),
                    html.Button("Load", id=DATA_LOADER_BUTTON, n_clicks=0),
                ],
                style={
                    "display": "flex",
                    "gap": "8px",
                    "align-items": "center",
                },
            ),
        ],
        style={
            "display": "flex",
            "align-items": "center",
            "gap": "10px",
            "margin": "10px",
        },
    )
