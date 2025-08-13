import dash_mantine_components as dmc
from dash import ALL
from dash import callback
from dash import ctx
from dash import Input
from dash import Output
from dash import State
from dash_iconify import DashIconify
from geoplotnik.components.ids import APPSHELL
from geoplotnik.components.ids import HEADER_BURGER
from geoplotnik.components.ids import NAVBAR


@callback(
    Output(APPSHELL, "navbar"),
    Output(HEADER_BURGER, "opened"),
    Input(HEADER_BURGER, "opened"),
    Input({"type": "navlink", "path": ALL, "leaf": ALL}, "n_clicks"),
    State(APPSHELL, "navbar"),
)
def handle_navbar_toggle(burger_opened, all_clicks, navbar):
    triggered = ctx.triggered_id

    # If burger clicked.
    if triggered == HEADER_BURGER:
        # Toggle navbar based on burger_opened.
        navbar["collapsed"] = {"mobile": not burger_opened}
        return navbar, burger_opened

    # If a leaf navlink selected.
    if isinstance(triggered, dict) and triggered.get("type") == "navlink":
        if triggered.get("leaf", False):
            navbar["collapsed"] = {"mobile": True}
            return navbar, False

    return navbar, burger_opened


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


def render() -> dmc.AppShellNavbar:
    return dmc.AppShellNavbar(
        id=NAVBAR,
        children=[
            dmc.NavLink(
                id={"type": "navlink", "path": "home", "leaf": True},
                label="Home",
                href="/",
                active="exact",
                leftSection=get_icon(icon="bi:house-door-fill"),
            ),
            dmc.NavLink(
                id={"type": "navlink", "path": "general", "leaf": False},
                label="General plots",
                childrenOffset=28,
                children=[
                    dmc.NavLink(
                        id={"type": "navlink", "path": "general/scatter", "leaf": True},
                        label="Scatter plot",
                        leftSection=get_icon(
                            icon="material-symbols:engineering-outline",
                        ),
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
                        leftSection=get_icon(
                            icon="material-symbols:engineering-outline",
                        ),
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
                        leftSection=get_icon(
                            icon="material-symbols:engineering-outline"
                        ),
                    ),
                ],
            ),
        ],
        p="md",
    )
