import dash_ag_grid as dag
import dash_mantine_components as dmc
from dash import callback
from dash import html
from dash import Input
from dash import Output
from geoplotnik.components.ids import DARK_LIGHT_MODE_TOGGLER
from geoplotnik.components.ids import DATA_UPLOAD_PREVIEW
from geoplotnik.data.loaders import load_data


def render() -> html.Div:
    """Render the previewer's UI.

    Loading the default dataset once here for the columns and data
    allows remove the CPU spike from the data-store callback.
    """
    default_data = load_data()
    columns = [{"field": col} for col in default_data]
    rows = default_data.to_dict("records")

    return html.Div(
        children=[
            dmc.Text("Data preview:"),
            dag.AgGrid(
                id=DATA_UPLOAD_PREVIEW,
                rowData=rows,
                columnDefs=columns,
                dashGridOptions={"pagination": True},
            ),
        ]
    )


@callback(
    Output(DATA_UPLOAD_PREVIEW, "className"),
    Input(DARK_LIGHT_MODE_TOGGLER, "checked"),
)
def update_data_preview_theme(is_dark_mode: bool) -> str:
    """Update the theme of the data previewer according to the global theme."""
    if is_dark_mode:
        return "ag-theme-alpine-dark"
    return "ag-theme-alpine"
