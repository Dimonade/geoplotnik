"""Geoplotnik.

Plot your favourite geological diagrams.
The data can be uploaded from a local flie or through a link.
"""

from dash import Dash
from dash import html
from dotenv import load_dotenv
from geoplotnik.components.layout import create_layout
from geoplotnik.pages import register_pages

def create_app() -> Dash:
    """Create a Dash app to serve to the user."""
    load_dotenv()

    app = Dash(__name__, use_pages=True, pages_folder="")
    register_pages()
    app.title = "Geoplotnik"
    app.layout = create_layout(app)
    return app


if __name__ == "__main__":
    raise SystemExit(create_app().run(debug=True))
