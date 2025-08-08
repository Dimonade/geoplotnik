"""TAS Diagram UI layout placements."""

from dash import html
from geoplotnik.components.ids import TAS_DIAGRAM
from geoplotnik.components.tas_diagram import axes_dropdown
from geoplotnik.components.tas_diagram import previewer
from geoplotnik.components.tas_diagram import uploader


def render() -> html.Div:
    return html.Div(
        children=[
            uploader.render(),
            previewer.render(),
            axes_dropdown.render(),
            html.Div(id=TAS_DIAGRAM),
        ],
        style={"margin-bottom": "10px"},
    )
