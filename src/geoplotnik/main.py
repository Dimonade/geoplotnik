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


def main() -> int:
    """Entrypoint to the application."""
    load_dotenv()

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Geoplotnik"
    app.layout = create_layout(app)
    app.run(debug=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
