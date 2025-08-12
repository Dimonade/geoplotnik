"""High level UI layout placements."""

import dash_mantine_components as dmc
import geoplotnik.components.header.layout as header_layout
import geoplotnik.components.master.layout as master_layout
import geoplotnik.components.navbar.layout as navbar_layout
from dash import _dash_renderer
from dash import Dash
from dash import dcc
from geoplotnik.components.ids import APPSHELL
from geoplotnik.components.ids import DATA_STORE_URL_TRIGGER
from geoplotnik.components.ids import DATA_STORE

_dash_renderer._set_react_version("18.2.0")


def create_layout(app: Dash) -> dmc.MantineProvider:
    """Create the highest level layout for Geoplotnik."""
    return dmc.MantineProvider(
        dmc.AppShell(
            id=APPSHELL,
            children=[
                dcc.Store(id=DATA_STORE),
                header_layout.render(),
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
        )
    )
