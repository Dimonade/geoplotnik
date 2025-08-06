import base64
from typing import Any

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
from geoplotnik.components.ids import TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_GROUPING_PARAMETER_SELECT_ALL_BUTTON
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
    Output(TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN, "options"),
    Output(TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN, "value"),
    Output(TAS_DIAGRAM_X_AXIS_DROPDOWN, "options"),
    Output(TAS_DIAGRAM_X_AXIS_DROPDOWN, "value"),
    Output(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "options"),
    Output(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "value"),
    Input(DATA_STORE, "data"),
    Input(TAS_DIAGRAM_GROUPING_PARAMETER_SELECT_ALL_BUTTON, "n_clicks"),
)
def update_grouping_parameter_dropdown(
    data: list[dict[str, Any]], _: int
) -> tuple[
    list[dict[str, str]], str, list[dict[str, str]], str, list[dict[str, str]], str
]:
    print("Updating x axis, y axis and grouping parameter dropdown with data columns.")
    if not data:
        raise PreventUpdate

    cols = sorted(set(data[0].keys()))
    opts = [{"label": col, "value": col} for col in cols]
    print(f"Columns to group by:\n{cols}")
    return (
        opts,
        opts[0]["value"],
        opts,
        opts[1]["value"],
        opts,
        opts[2]["value"],
    )


@callback(
    Output(TAS_DIAGRAM, "children"),
    Input(DATA_STORE, "data"),
    Input(TAS_DIAGRAM_X_AXIS_DROPDOWN, "value"),
    Input(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "value"),
    Input(TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN, "value"),
)
def update_tas_diagram(
    data: list[dict],
    x_axis: str,
    y_axis: str,
    grouping_parameter: str,
) -> html.Div:
    print("Update TAS diagram callback triggered.")
    print("Data keys:", type(data), len(data) if data else None)
    print(
        "x_axis:", x_axis, "y_axis:", y_axis, "grouping_parameter:", grouping_parameter
    )

    if not data or not x_axis or not y_axis:
        return html.Div("No data.", id=TAS_DIAGRAM)

    if not data:
        return html.Div("No data for selected locations.", id=TAS_DIAGRAM)

    df = pd.DataFrame(data)

    df[x_axis] = pd.to_numeric(df[x_axis], errors="coerce")
    df[y_axis] = pd.to_numeric(df[y_axis], errors="coerce")

    df = df.dropna(subset=[x_axis, y_axis])

    if len(df) == 0:
        raise PreventUpdate

    print(f"Types in x_axis: {set([type(x) for x in df[x_axis]])}")
    print(f"TYpes in y axis: {set([type(y) for y in df[y_axis]])}")

    group_colour = grouping_parameter if grouping_parameter in df.columns else None
    print(f"Colour groups: {group_colour}")

    fig = px.scatter(df, x=x_axis, y=y_axis, color=group_colour)
    fig.update_layout(title_text="TAS Diagram", title_x=0.5)
    print("Creating a TAS diagram.")
    return html.Div(dcc.Graph(figure=fig), id=TAS_DIAGRAM)
