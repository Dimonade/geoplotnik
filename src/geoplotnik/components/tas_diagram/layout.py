"""TAS Diagram UI layout placements."""

from dash import callback
from dash import html
from dash import Output
from dash import Input
from dash import State
import dash_bootstrap_components as dbc
from geoplotnik.components.ids import TAS_DIAGRAM
from geoplotnik.components.tas_diagram import axes_dropdown
from geoplotnik.components.tas_diagram import previewer
from geoplotnik.components.tas_diagram import uploader

TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON = "tas-diagram-data-preview-collapser-button"
TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER = "tas-diagram-data-preview-collapser"


def render() -> html.Div:
    return html.Div(
        children=[
            uploader.render(),
            html.Div(
                children=[
                    dbc.Button(
                        "Open data preview",
                        id=TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON,
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            previewer.render(),
                        ),
                        id=TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER,
                        is_open=False,
                    ),
                ]
            ),
            axes_dropdown.render(),
            html.Div(id=TAS_DIAGRAM),
        ],
        style={"margin-bottom": "10px"},
    )


@callback(
    Output(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON, "children"),
    Output(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER, "is_open"),
    Input(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON, "n_clicks"),
    State(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER, "is_open"),
)
def toggle_data_previewer_collapser(n_clicks: int, is_open: bool) -> tuple[str, bool]:
    """Toggle the data previewer collapse state."""
    # Upon app initialization, `n_clicks` is triggered, keep collapser collapsed.
    if n_clicks is None:
        return "Open data preview", False

    print("Toggling the TAS diagram data previewer.")
    if is_open:
        return "Open data preview", False
    return "Close data preview", True
