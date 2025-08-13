import dash_mantine_components as dmc
from dash import clientside_callback
from dash import Input
from dash import Output
from dash_iconify import DashIconify
from geoplotnik.components.ids import DARK_LIGHT_MODE_TOGGLER
from geoplotnik.components.ids import HEADER_BURGER

theme_toggle = dmc.Switch(
    offLabel=DashIconify(
        icon="radix-icons:sun", width=15, color=dmc.DEFAULT_THEME["colors"]["yellow"][8]
    ),
    onLabel=DashIconify(
        icon="radix-icons:moon",
        width=15,
        color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
    ),
    id=DARK_LIGHT_MODE_TOGGLER,
    persistence=True,
    color="grey",
)


clientside_callback(
    """ 
    (switchOn) => {
       document.documentElement.setAttribute('data-mantine-color-scheme', switchOn ? 'dark' : 'light');  
       return window.dash_clientside.no_update
    }
    """,
    Output(DARK_LIGHT_MODE_TOGGLER, "id"),
    Input(DARK_LIGHT_MODE_TOGGLER, "checked"),
)


def render() -> dmc.AppShellHeader:
    return dmc.AppShellHeader(
        dmc.Group(
            [
                dmc.Group(
                    [
                        dmc.Burger(
                            id=HEADER_BURGER,
                            size="sm",
                            hiddenFrom="sm",
                            opened=False,
                        ),
                        # dmc.Image(src=geoplotnik_logo, h=40, flex=0),  # TODO: Create a logo.
                        dmc.Title("Geoplotnik", c="blue"),
                    ]
                ),
                theme_toggle,
            ],
            justify="space-between",
            style={"flex": 1},
            h="100%",
            px="md",
        ),
    )
