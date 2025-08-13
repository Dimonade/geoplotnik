"""Geoplotnik.

Plot your favourite geological diagrams.
The data can be uploaded from a local flie or through a link.
"""

from dash import Dash
from dotenv import load_dotenv
from geoplotnik.components.layout import create_layout
from geoplotnik.components.tas_diagram import callbacks  # noqa: F401
from geoplotnik.pages import register_pages
# Callbacks are not used directly, but must be imported to be registered.


def create_app() -> Dash:
    """Create a Dash app to serve to the user."""
    load_dotenv()

    app = Dash(
        __name__,
        use_pages=True,
        pages_folder="",
        suppress_callback_exceptions=True,
    )
    register_pages()
    app.title = "Geoplotnik"
    app.layout = create_layout(app)
    return app


if __name__ == "__main__":
    raise SystemExit(create_app().run(debug=True))
