"""TAS Diagram UI layout placements."""

from dash import html
from geoplotnik.components.ids import TAS_DIAGRAM
from geoplotnik.components.tas_diagram import axes_dropdown
from geoplotnik.components.tas_diagram import grouping_parameter
from geoplotnik.components.tas_diagram import uploader
from geoplotnik.components.tas_diagram import previewer


def render() -> html.Div:
    return html.Div(
        children=[
            uploader.render(),
            previewer.render(),
            axes_dropdown.render(),
            grouping_parameter.render(),
            html.Div(id=TAS_DIAGRAM),
        ],
        style={"margin-bottom": "10px"},
    )
