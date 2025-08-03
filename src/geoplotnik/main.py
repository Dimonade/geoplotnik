from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from geoplotnik.components.layout import create_layout
from geoplotnik.data.loaders import load_data
from geoplotnik.data.source import DataSource
from geoplotnik.components.tas_diagram import callbacks

def main() -> int:
    """Entrypoint to the application."""
    default_data = DataSource(load_data())

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Geoplotnik"
    app.layout = create_layout(app, default_data)
    app.run(debug=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
