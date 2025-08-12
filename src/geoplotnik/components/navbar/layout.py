import dash_mantine_components as dmc
from dash import callback
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
                label="General plots",
                childrenOffset=28,
                children=[
                    dmc.NavLink(
                        label="Scatter plot",
                        description="Generic scatter plot",
                        href="/general_plots/scatter",
                        active="partial",
                    )
                ],
            ),
            dmc.NavLink(
                label="Rock classification",
                childrenOffset=28,
                children=[
                    dmc.NavLink(
                        label="SiO2 vs Na2O+K2O",
                        description="Use for volcanic rocks.",
                        href="/rock_classification/sio2_vs_na2o_plus_k2o",
                        active="partial",
                    ),
                    dmc.NavLink(
                        label="SiO2 vs K2O",
                        description="Emphasis on andesitic-basaltic composition range.",
                        href="/rock_classification/sio2_vs_k2o",
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
                        href="/series_discriminant_templates/volcanic_rocks",
                    ),
                ],
            ),
        ],
        p="md",
    )
