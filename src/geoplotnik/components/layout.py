from dash import Dash
from dash import html
from dash import dcc
import geoplotnik.components.tas_diagram.layout as tas_diagram_layout
from geoplotnik.data.source import DataSource


def create_layout(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className="add-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="tas-diagram-container",
                children=[
                    dcc.Location(id="url", refresh=False),
                    dcc.Store(id="data-store"),# , data=source._data.to_dict("records")),
                    tas_diagram_layout.render(),
                ],
            ),
        ],
    )
