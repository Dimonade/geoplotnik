"""High level UI layout placements."""

import dash_mantine_components as dmc
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
import geoplotnik.components.header.layout as header_layout
import geoplotnik.components.master.layout as master_layout
import geoplotnik.components.navbar.layout as navbar_layout

_dash_renderer._set_react_version("18.2.0")


def create_layout(app: Dash) -> dmc.MantineProvider:
    """Create the highest level layout for Geoplotnik."""
    return dmc.MantineProvider(
        dmc.AppShell(
            [
                dcc.Location(id="url", refresh=False),
                header_layout.render(),
                dcc.Store(id=DATA_STORE),
                navbar_layout.render(),
                master_layout.render(),
            ],
            header={"height": 60},
            padding="md",
            navbar={
                "width": 300,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
            id="appshell",
        )
    )


"""
dmc.MantineProvider(
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
                    dcc.Location(id="url", refresh=False),
                    dcc.Store(id=DATA_STORE),
                    tas_diagram_layout.render(),
                ],
            ),
        ],
    ),
"""
