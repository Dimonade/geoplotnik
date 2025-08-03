from dash import dcc
from dash import html
from geoplotnik.components.ids import TAS_DIAGRAM_LOCATION_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_LOCATION_SELECT_ALL_BUTTON


def render() -> html.Div:
    return html.Div(
        children=[
            html.H6("Location filter"),
            dcc.Dropdown(
                id=TAS_DIAGRAM_LOCATION_DROPDOWN,
                options=[],
                value=[],
                multi=True,
                placeholder="Select locations to filter by...",
            ),
            html.Button(
                id=TAS_DIAGRAM_LOCATION_SELECT_ALL_BUTTON,
                className="dropdown-button",
                children=["Select all"],
                n_clicks=0,
            ),
        ],
    )
