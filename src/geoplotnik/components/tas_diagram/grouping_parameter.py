from dash import dcc
from dash import html
from geoplotnik.components.ids import TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN


def render() -> html.Div:
    return html.Div(
        children=[
            html.H6("Grouping parameter"),
            dcc.Dropdown(
                id=TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN,
                options=[],
                value=[],
                multi=False,
                placeholder="Select parameter to group by...",
            ),
        ],
    )
