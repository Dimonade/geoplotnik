"""TAS Diagram UI layout placements."""

import dash_mantine_components as dmc
import dash
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import State
from geoplotnik.components.ids import TAS_DIAGRAM
from geoplotnik.components.ids import TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER
from geoplotnik.components.ids import TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON
from geoplotnik.components.tas_diagram import axes_dropdown
from geoplotnik.components.tas_diagram import previewer
from geoplotnik.components.tas_diagram import uploader

def render() -> html.Div:
    from geoplotnik.components.tas_diagram import callbacks  # noqa: F401
    # Callbacks are not used directly, but must be imported to be registered.

    return html.Div(
        children=[
            uploader.render(),
            html.Div(
                children=[
                    dmc.Button(
                        "Open data preview",
                        id=TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON,
                    ),
                    dmc.Collapse(
                        dmc.Card(
                            previewer.render(),
                        ),
                        id=TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER,
                        opened=False,
                    ),
                ],
                style={
                    "gap": "10px",
                    "margin-bottom": "10px",
                },
            ),
            axes_dropdown.render(),
            html.Div(id=TAS_DIAGRAM),
        ],
    )


@callback(
    Output(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON, "children"),
    Output(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER, "opened"),
    Input(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON, "n_clicks"),
    State(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER, "opened"),
)
def toggle_data_previewer_collapser(n_clicks: int, opened: bool) -> tuple[str, bool]:
    """Toggle the data previewer collapse state."""
    # Upon app initialization, `n_clicks` is triggered, keep collapser collapsed.
    if n_clicks is None:
        return "Open data preview", False

    print("Toggling the TAS diagram data previewer.")
    if opened:
        return "Open data preview", False
    return "Close data preview", True
