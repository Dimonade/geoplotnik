from dash import html, dash_table
from geoplotnik.components.ids import DATA_UPLOAD_PREVIEW

def render() -> html.Div:
    """Render the previewer's UI."""
    return html.Div(
        [
            html.H5("Data preview"),
            dash_table.DataTable(
                id=DATA_UPLOAD_PREVIEW,
                page_size=8,
            ),
        ]
    )