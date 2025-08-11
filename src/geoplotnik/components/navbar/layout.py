import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import Dash, Input, Output, State, callback, clientside_callback, html
from dash_iconify import DashIconify


@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


def render() -> dmc.AppShellNavbar:
    return dmc.AppShellNavbar(
        id="navbar",
        children=[
            "Navbar",
            html.Div(
                [
                    dmc.NavLink(
                        label="With icon",
                        leftSection=get_icon(icon="bi:house-door-fill"),
                    ),
                ]
            ),
        ],
        p="md",
    )
