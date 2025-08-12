import dash_mantine_components as dmc
from dash import dcc
from dash import html
from geoplotnik.components.ids import TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_X_AXIS_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_Y_AXIS_DROPDOWN


def render() -> html.Div:
    return html.Div(
        children=[
            dmc.Text(
                "X Axis:",
                style={"display": "inline-block", "margin-right": "10px"},
            ),
            dmc.Select(
                id=TAS_DIAGRAM_X_AXIS_DROPDOWN,
                data=[],
                value=None,
                searchable=True,
                clearable=False,
                style={"width": "200px", "display": "inline-block"},
            ),
            dmc.Text(
                "Y Axis:",
                style={
                    "display": "inline-block",
                    "margin-left": "10px",
                    "margin-right": "10px",
                },
            ),
            dmc.Select(
                id=TAS_DIAGRAM_Y_AXIS_DROPDOWN,
                data=[],
                value=None,
                searchable=True,
                clearable=False,
                style={"width": "200px", "display": "inline-block"},
            ),
            dmc.Text(
                "Grouping parameter:",
                style={
                    "display": "inline-block",
                    "margin-left": "10px",
                    "margin-right": "10px",
                },
            ),
            dmc.Select(
                id=TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN,
                data=[],
                value=[],
                searchable=True,
                clearable=False,
                placeholder="Select parameter to group by...",
                style={"width": "200px", "display": "inline-block"},
            ),
        ],
    )
