import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from dash import State
from geoplotnik.components.ids import DARK_LIGHT_MODE_TOGGLER
from geoplotnik.components.ids import DATA_UPLOAD_PREVIEW
from geoplotnik.components.ids import TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER
from geoplotnik.components.ids import TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON


def render() -> html.Div:
    """Render the previewer's UI.

    Loading the default dataset once here for the columns and data
    allows remove the CPU spike from the data-store callback.
    """
    return html.Div(
        children=[
            dmc.Button(
                "Open data preview",
                id=TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON,
            ),
            dmc.Collapse(
                id=TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER,
                opened=False,
                children=[
                    dmc.Card(
                        children=[
                            dmc.Stack(
                                [
                                    dmc.Text("Data preview:"),
                                    dag.AgGrid(
                                        id=DATA_UPLOAD_PREVIEW,
                                        dashGridOptions={"pagination": True},
                                    ),
                                ],
                                align="start",
                                gap="sm",
                            ),
                        ],
                    ),
                ],
            ),
        ],
        style={
            "gap": "10px",
            "margin-bottom": "10px",
        },
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


@callback(
    Output(DATA_UPLOAD_PREVIEW, "className"),
    Input(DARK_LIGHT_MODE_TOGGLER, "checked"),
)
def update_data_preview_theme(is_dark_mode: bool) -> str:
    """Update the theme of the data previewer according to the global theme."""
    if is_dark_mode:
        return "ag-theme-alpine-dark"
    return "ag-theme-alpine"
