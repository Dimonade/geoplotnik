import dash_mantine_components as dmc
import dash
from dash import callback
from dash import clientside_callback
from dash import Dash
from dash import html
from dash import Input
from dash import Output
from dash import State
from dash_iconify import DashIconify
from geoplotnik.components.ids import APPSHELL
from geoplotnik.components.ids import HEADER_BURGER
from geoplotnik.components.ids import NAVBAR


@callback(
    Output(APPSHELL, "navbar"),
    Input(HEADER_BURGER, "opened"),
    State(APPSHELL, "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


def render() -> dmc.AppShellNavbar:
    return dmc.AppShellNavbar(
        id=NAVBAR,
        children=[
            dmc.NavLink(
                label="Home",
                href="/",
                active="exact",
                leftSection=get_icon(icon="bi:house-door-fill"),
            ),
            dmc.NavLink(
                label="Rock classification",
                childrenOffset=28,
                children=[
                    dmc.NavLink(
                        label="SiO2 vs Na2O+K2O",
                        description="Use for volcanic rocks.",
                        href="/tas-diagram",
                        active="partial",
                    ),
                    dmc.NavLink(
                        label="SiO2 vs K2O",
                        description="Emphasis on andesitic-basaltic composition range.",
                    ),
                ],
            ),
            dmc.NavLink(
                label="Series discriminant templates",
                childrenOffset=28,
                children=[
                    dmc.NavLink(
                        label="Volcanic rocks",
                        description="Ideal for weathered and metamorphosed rocks as this plot uses immobile trace elements.",
                    ),
                ],
            ),
        ],
        p="md",
    )
