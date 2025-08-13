import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash import callback
from dash import dcc
from dash import html
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from geoplotnik.components.ids import DARK_LIGHT_MODE_TOGGLER
from geoplotnik.components.ids import DATA_PREVIEW_MOUNTED_MARKER
from geoplotnik.components.ids import DATA_STORE
from geoplotnik.components.ids import DATA_UPLOAD_PREVIEW
from geoplotnik.components.ids import TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER
from geoplotnik.components.ids import TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON

AG_GRID_HEIGHT = "25vh"


def render() -> html.Div:
    """Render the previewer's UI."""
    return html.Div(
        children=[
            dcc.Store(id=DATA_PREVIEW_MOUNTED_MARKER, data=False),
            dmc.Button(
                "Open data preview",
                id=TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON,
            ),
            dmc.Collapse(
                id=TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER,
                opened=False,
                # Mounting the AG Grid only when the collapser is open.
                children=[],
            ),
        ],
        style={
            "gap": "10px",
            "margin-bottom": "10px",
        },
    )


@callback(
    Output(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER, "children"),
    Output(DATA_PREVIEW_MOUNTED_MARKER, "data"),
    Input(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER, "opened"),
    State(DATA_PREVIEW_MOUNTED_MARKER, "data"),
    State(DARK_LIGHT_MODE_TOGGLER, "checked"),
    State(DATA_STORE, "data"),
)
def render_preview_children(opened, mounted, is_dark, data):
    """Render the children of the Collapse only if it is open."""

    # Not open, therefore no mounting.
    if not opened and not mounted:
        return [], mounted

    # Otherwise, mount.
    theme_class = "ag-theme-alpine-dark" if is_dark else "ag-theme-alpine"

    if not data:
        card = dmc.Card(dmc.Text("No data loaded yet."))
    else:
        first_row = data[0]
        columns = [{"field": key} for key in first_row.keys()]
        grid = dag.AgGrid(
            id=DATA_UPLOAD_PREVIEW,
            rowData=data,
            columnDefs=columns,
            className=theme_class,
            dashGridOptions={"pagination": True},
            style={"height": AG_GRID_HEIGHT, "width": "100%"},
        )
        card = dmc.Card(dmc.Stack([grid], align="start", gap="sm"))

    return [card], True


@callback(
    Output(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER, "opened"),
    Output(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON, "children"),
    Input(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER_BUTTON, "n_clicks"),
    State(TAS_DIAGRAM_DATA_PREVIEW_COLLAPSER, "opened"),
)
def toggle_preview(n_clicks, opened):
    if n_clicks is None:
        raise PreventUpdate
    new_state = not opened
    label = "Close data preview" if new_state else "Open data preview"
    return new_state, label
