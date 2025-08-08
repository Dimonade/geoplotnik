from dash import dcc
from dash import html
from geoplotnik.components.ids import TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_X_AXIS_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_Y_AXIS_DROPDOWN


def render() -> html.Div:
    return html.Div(
        children=[
            html.Div(
                "X Axis:",
                style={"display": "inline-block", "margin-right": "10px"},
            ),
            dcc.Dropdown(
                id=TAS_DIAGRAM_X_AXIS_DROPDOWN,
                options=[],
                value=None,
                multi=False,
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
                multi=False,
                clearable=False,
                style={"width": "200px", "display": "inline-block"},
            ),
            html.Div(
                "Grouping parameter:",
                style={
                    "display": "inline-block",
                    "margin-left": "10px",
                    "margin-right": "10px",
                },
            ),
            dcc.Dropdown(
                id=TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN,
                options=[],
                value=[],
                multi=False,
                clearable=False,
                placeholder="Select parameter to group by...",
                style={"width": "200px", "display": "inline-block"},
            ),
        ],
    )
