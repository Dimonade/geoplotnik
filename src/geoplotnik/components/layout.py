"""High level UI layout placements."""

from dash import Dash
from dash import html
from dash import dcc
from geoplotnik.components.ids import DATA_STORE, TAS_DIAGRAM_CONTAINER
import geoplotnik.components.tas_diagram.layout as tas_diagram_layout


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="add-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className=TAS_DIAGRAM_CONTAINER,
                children=[
                    dcc.Location(id="url", refresh=False),
                    dcc.Store(id=DATA_STORE),
                    tas_diagram_layout.render(),
                ],
            ),
        ],
    )
