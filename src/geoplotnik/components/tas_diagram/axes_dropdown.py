from dash import Dash
from dash import dcc
from dash import html
from geoplotnik.components.ids import TAS_DIAGRAM_X_AXIS_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_Y_AXIS_DROPDOWN


def render() -> html.Div:
    return html.Div(
        children=[
            html.Div(
                "X Axis:", style={"display": "inline-block", "margin-right": "10px"}
            ),
            dcc.Dropdown(
                id=TAS_DIAGRAM_X_AXIS_DROPDOWN,
                options=[],
                value=None,
                clearable=False,
                style={"width": "200px", "display": "inline-block"},
            ),
            html.Div(
                "Y Axis:",
                style={
                    "display": "inline-block",
                    "margin-left": "10px",
                    "margin-right": "10px",
                },
            ),
            dcc.Dropdown(
                id=TAS_DIAGRAM_Y_AXIS_DROPDOWN,
                options=[],
                value=None,
                clearable=False,
                style={"width": "200px", "display": "inline-block"},
            ),
        ]
    )
