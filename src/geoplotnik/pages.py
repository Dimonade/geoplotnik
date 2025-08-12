import dash
from dash import html
from geoplotnik.components.home.layout import render as home_render
from geoplotnik.components.tas_diagram.layout import render as tas_diagram_render


def register_pages() -> None:
    """Register the currently available pages in `Geoplotnik`."""
    dash.register_page("home", path="/", layout=home_render)
    dash.register_page(
        "Scatter plot",
        path="/general_plots/scatter",
        layout=html.Div(html.H1("Placeholder for scatter plots.")),
    )
    dash.register_page(
        "SiO2 vs Na2O + K2O",
        path="/rock_classification/sio2_vs_na2o_plus_k2o",
        layout=tas_diagram_render,
    )
    dash.register_page(
        "SiO2 vs K2O",
        path="/rock_classification/sio2_vs_k2o",
        layout=html.Div(html.H1("Placeholder for SiO2 vs K2O plots.")),
    )
    dash.register_page(
        "Volcanic rocks",
        path="/series_discriminant_templates/volcanic_rocks",
        layout=html.Div(html.H1("Placeholder for Volcanic rock plots.")),
    )
