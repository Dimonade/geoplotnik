import dash_mantine_components as dmc
import dash
from dash import callback
from dash import clientside_callback
from dash import Dash
from dash import Input
from dash import Output
from dash import State
from dash_iconify import DashIconify


def render() -> dmc.AppShellMain:
    return dmc.AppShellMain(
        dmc.Group(
            [
                dash.page_container,
            ]
        )
    )
