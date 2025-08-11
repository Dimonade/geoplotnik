import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, Input, Output, State, callback, clientside_callback
import geoplotnik.components.tas_diagram.layout as tas_diagram_layout


def render() -> dmc.AppShellMain:
    return dmc.AppShellMain(
        dmc.Group(
            [
                tas_diagram_layout.render(),
            ]
        )
    )
