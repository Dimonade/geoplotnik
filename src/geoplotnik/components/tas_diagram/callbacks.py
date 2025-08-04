import base64

import pandas as pd
import plotly.express as px
from dash import callback
from dash import dcc
from dash import html
from dash import Input
from dash import Output
from dash import State
from dash.exceptions import PreventUpdate
from geoplotnik.components.ids import DATA_STORE
from geoplotnik.components.ids import DATA_UPLOAD_AREA
from geoplotnik.components.ids import DATA_UPLOAD_PREVIEW
from geoplotnik.components.ids import TAS_DIAGRAM
from geoplotnik.components.ids import TAS_DIAGRAM_LOCATION_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_LOCATION_SELECT_ALL_BUTTON
from geoplotnik.components.ids import TAS_DIAGRAM_X_AXIS_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_Y_AXIS_DROPDOWN
from geoplotnik.data.loaders import load_data


@callback(
    Output(DATA_STORE, "data"),
    Input("url", "pathname"),
    Input(DATA_UPLOAD_AREA, "contents"),
    State(DATA_UPLOAD_AREA, "filename"),
    State(DATA_UPLOAD_AREA, "last_modified"),
)
def update_data_store(url: str, contents: list, names: list, dates: list) -> dict:
    print("Updating data store.")

    # If this is true, we probably have an issue.
    if contents is None and url is None:
        raise PreventUpdate

    if contents is not None:
        print(f"File received: {names}.")
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)

        df = load_data(decoded)
    elif url is not None:
        print("Trying to load default data.")
        df = load_data()
    else:
        print("Cannot load any data.")

    print("Loaded dataframe shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("Sample first row:", df.head(1).to_dict("records"))
    return df.to_dict("records")


@callback(
    Output(DATA_UPLOAD_PREVIEW, "data"),
    Output(DATA_UPLOAD_PREVIEW, "columns"),
    Input(DATA_STORE, "data"),
)
def update_data_preview(
    data: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    if not data:
        raise PreventUpdate
    columns = [{"name": col, "id": col} for col in data[0]]
    return data, columns


@callback(
    Output(TAS_DIAGRAM_LOCATION_DROPDOWN, "options"),
    Output(TAS_DIAGRAM_LOCATION_DROPDOWN, "value"),
    Input(DATA_STORE, "data"),
    Input(TAS_DIAGRAM_LOCATION_SELECT_ALL_BUTTON, "n_clicks"),
)
def update_location_dropdown(data, _: int):
    print("Updating location dropdown.")
    if not data:
        raise PreventUpdate

    locations = sorted(set(row["Location"] for row in data if "Location" in row))
    options = [{"label": loc, "value": loc} for loc in locations]
    print(f"Location:\n{locations}")
    return options, locations


@callback(
    Output(TAS_DIAGRAM_X_AXIS_DROPDOWN, "options"),
    Output(TAS_DIAGRAM_X_AXIS_DROPDOWN, "value"),
    Input(DATA_STORE, "data"),
)
def populate_x_axis_dropdowns(data):
    print("Populating x axis options.")
    if not data:
        raise PreventUpdate
    df = pd.DataFrame(data)

    cols = set(df.columns.tolist())
    options = [{"label": col, "value": col} for col in cols]
    default = options[0]["value"]

    print(f"Axes have the following options:\n{options}.")
    return options, default


@callback(
    Output(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "options"),
    Output(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "value"),
    Input(DATA_STORE, "data"),
)
def populate_y_axis_dropdowns(data):
    print("Populating y axis options.")
    if not data:
        raise PreventUpdate
    df = pd.DataFrame(data)

    cols = set(df.columns.tolist())
    options = [{"label": col, "value": col} for col in cols]
    default = options[0]["value"]

    print(f"Axes have the following options:\n{options}.")
    return options, default


@callback(
    Output(TAS_DIAGRAM, "children"),
    Input(DATA_STORE, "data"),
    Input(TAS_DIAGRAM_X_AXIS_DROPDOWN, "value"),
    Input(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "value"),
    Input(TAS_DIAGRAM_LOCATION_DROPDOWN, "value"),
)
def update_tas_diagram(
    data: list[dict],
    x_axis: str,
    y_axis: str,
    locations: list[str],
) -> html.Div:
    print("Update TAS diagram callback triggered.")
    print("Data keys:", type(data), len(data) if data else None)
    print("x_axis:", x_axis, "y_axis:", y_axis, "locations:", locations)
    print(f"Type of record item: {type(data[0])}")

    if not data or not x_axis or not y_axis:
        return html.Div("No data.", id=TAS_DIAGRAM)

    if locations:
        data = [row for row in data if row.get("Location") in locations]

    if not data:
        return html.Div("No data for selected locations.", id=TAS_DIAGRAM)

    df = pd.DataFrame(data)
    color_col = "Location" if "Location" in df.columns else None

    fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col)
    fig.update_layout(title_text="TAS Diagram", title_x=0.5)
    print("Creating a TAS diagram.")
    return html.Div(dcc.Graph(figure=fig), id=TAS_DIAGRAM)
