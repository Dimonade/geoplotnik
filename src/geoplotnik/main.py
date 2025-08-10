"""Geoplotnik.

Plot your favourite geological diagrams.
The data can be uploaded from a local flie or through a link.
"""

from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from geoplotnik.components.layout import create_layout

# Callbacks are not used directly, but must be imported.
from geoplotnik.components.tas_diagram import callbacks  # noqa: F401

from dotenv import load_dotenv


def create_app():
    """Create a Dash app to serve to the user."""
    load_dotenv()

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Geoplotnik"
    app.layout = create_layout(app)
    return app


if __name__ == "__main__":
    raise SystemExit(create_app().run(debug=True))
