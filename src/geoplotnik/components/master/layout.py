import dash
import dash_mantine_components as dmc
from dash import callback
from dash import clientside_callback
from dash import Dash
from dash import Input
from dash import Output
from dash import State
from dash_iconify import DashIconify


def render() -> dmc.AppShellMain:
    return dmc.AppShellMain(
        dash.page_container,
    )
