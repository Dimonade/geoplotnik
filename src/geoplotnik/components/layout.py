"""High level UI layout placements."""

import dash_mantine_components as dmc
import geoplotnik.components.tas_diagram.layout as tas_diagram_layout
from dash import _dash_renderer
from dash import clientside_callback
from dash import Dash
from dash import dcc
from dash import html
from dash import Input
from dash import Output
from dash_iconify import DashIconify
from geoplotnik.components.ids import DARK_LIGHT_MODE_TOGGLER
from geoplotnik.components.ids import DATA_STORE
from geoplotnik.components.ids import TAS_DIAGRAM_CONTAINER

_dash_renderer._set_react_version("18.2.0")

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


def create_layout(app: Dash) -> dmc.MantineProvider:
    """Create the highest level layout for Geoplotnik."""
    return dmc.MantineProvider(
        children=[
            dmc.Center(
                dmc.Title(
                    app.title,
                    order=1,
                ),
            ),
            dmc.Divider(),
            html.Div(
                className=TAS_DIAGRAM_CONTAINER,
                children=[
                    theme_toggle,
                    dcc.Location(id="url", refresh=False),
                    dcc.Store(id=DATA_STORE),
                    tas_diagram_layout.render(),
                ],
            ),
        ],
    )
