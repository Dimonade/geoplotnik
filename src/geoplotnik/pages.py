import dash
from geoplotnik.components.home.layout import render as home_render
from geoplotnik.components.tas_diagram.layout import render as tas_diagram_render

def register_pages() -> None:
    dash.register_page("home", path="/", layout=home_render())
    dash.register_page("tas", path="/tas-diagram", layout=tas_diagram_render)