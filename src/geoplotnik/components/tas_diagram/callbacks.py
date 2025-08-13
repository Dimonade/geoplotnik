"""Definitions of callbacks that make the TAS diagram interactive."""

import base64
from typing import Any

import pandas as pd
import plotly.express as px
from dash import callback
from dash import ctx
from dash import dcc
from dash import html
from dash import Input
from dash import Output
from dash.exceptions import PreventUpdate
from geoplotnik.components.ids import DARK_LIGHT_MODE_TOGGLER
from geoplotnik.components.ids import DATA_LOADER_BUTTON
from geoplotnik.components.ids import DATA_STORE
from geoplotnik.components.ids import DATA_UPLOAD_AREA
from geoplotnik.components.ids import DATA_UPLOAD_PREVIEW
from geoplotnik.components.ids import TAS_DIAGRAM
from geoplotnik.components.ids import TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_X_AXIS_DROPDOWN
from geoplotnik.components.ids import TAS_DIAGRAM_Y_AXIS_DROPDOWN
from geoplotnik.components.ids import URL_INPUT
from geoplotnik.components.tas_diagram.rocks import Rocks
from geoplotnik.data.loaders import load_data
from geoplotnik.data.loaders import load_data_from_url
from geoplotnik.data.loaders import TasColumns


def make_empty_scatter():
    """Create an initial empty plot."""
    fig = px.scatter(pd.DataFrame({"x": [], "y": []}), x="x", y="y")
    fig.update_layout(
        xaxis={"visible": True, "range": [0, 1]},
        yaxis={"visible": True, "range": [0, 1]},
        annotations=[
            {
                "text": "Upload data to see the plot",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 16},
            }
        ],
    )
    return fig


@callback(
    Output(DATA_STORE, "data"),
    Output(URL_INPUT, "value"),
    Output(DATA_UPLOAD_AREA, "contents"),
    Input(URL_INPUT, "value"),
    Input(DATA_UPLOAD_AREA, "contents"),
    Input(DATA_LOADER_BUTTON, "n_clicks"),
)
def update_data_store(
    url_value: str,
    upload_contents: list[Any],
    _: int,  # I just want the update signal, the n_clicks is not important.
) -> tuple[list[dict[str, Any]], str | None, str | None]:
    """Update the data store with user supplied data."""
    print("Updating data store.")
    triggered = ctx.triggered_id
    if triggered is None:
        print("No trigger - no update.")
        raise PreventUpdate

    url_out = url_value
    upload_out = upload_contents

    try:
        # Drap and drop from local user storage is triggered.
        if triggered == DATA_UPLOAD_AREA and upload_contents:
            c = (
                upload_contents[0]
                if isinstance(upload_contents, list)
                else upload_contents
            )
            if not isinstance(c, str) or "," not in c:
                msg = "Upload data contents are malformed."
                raise ValueError(msg)
            content_type, content_string = c.split(",", 1)
            decoded = base64.b64decode(content_string)
            df = load_data(decoded)

            upload_out = upload_contents
            return df.to_dict("records"), "", upload_out

        # URL loading is triggered.
        if triggered == DATA_LOADER_BUTTON:
            if not url_value:
                print("Load URL button was triggered but no URL supplied - no update.")
                raise PreventUpdate

            df = load_data_from_url(url_value)
            if df is None:
                print("No data from url with button trigger - no update.")
                raise PreventUpdate

            url_out = url_value
            return df.to_dict("records"), url_out, ""

        # Return is pressed inside of the URL input.
        if triggered == URL_INPUT:
            if not url_value:
                print(
                    "Return inside URL input was triggered but no URL was supplied - no update."
                )
            df = load_data_from_url(url_value)
            if df is None:
                print("No data from url trigger - no update.")
                raise PreventUpdate

        # In any other case, prevent update.
        print("No useful input for data loading - no update.")
        raise PreventUpdate

    # Since many things can go wrong, at the moment, blanket catch all exceptions,
    # and deal with then on a per case basis, as the cases come by.
    except Exception:
        print("update_data_store: failed to load data.")
        raise PreventUpdate


def try_set_default_axis_value(
    options: list[dict[str, str]], needle: str
) -> str | None:
    """Try to set the default values for the X and Y axes according to a TAS diagram."""
    for option in options:
        if option["value"].casefold() == needle.casefold():
            return option["value"]
    return None


def try_set_default_grouping_parameter(
    options: list[dict[str, str]], needles: list[str]
) -> str | None:
    """Try to set the default grouping parameter to a logical categorical group."""
    opts = [o["value"] for o in options]
    # Return the first match, don't try to be too smart about it.
    for needle in needles:
        for op in opts:
            if needle.casefold() in op.casefold():
                return op
    return None


def sanitize_grouping_parameter(
    df: pd.DataFrame,
    grouping_parameter: str | None,
    fill_label: str = "Ungrouped",
    *,
    drop_na: bool = False,
) -> tuple[pd.DataFrame, str | None]:
    """Ensure grouping column is present and clean NA values."""
    if grouping_parameter and grouping_parameter in df.columns:
        if drop_na:
            df = df.dropna(subset=[grouping_parameter])
        else:
            df[grouping_parameter] = df[grouping_parameter].fillna(fill_label)
        return df, grouping_parameter
    return df, None


@callback(
    Output(TAS_DIAGRAM_X_AXIS_DROPDOWN, "data"),
    Output(TAS_DIAGRAM_X_AXIS_DROPDOWN, "value"),
    Output(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "data"),
    Output(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "value"),
    Output(TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN, "data"),
    Output(TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN, "value"),
    Input(DATA_STORE, "data"),
)
def update_tas_diagram_dropdowns(
    data: list[dict[str, Any]],
) -> tuple[
    list[dict[str, str]],
    str | None,
    list[dict[str, str]],
    str | None,
    list[dict[str, str]],
    str | None,
]:
    """Update the TAS diagram's axes and grouping parameters dropdowns' values."""
    print("Updating x axis, y axis and grouping parameter dropdown with data columns.")
    if not data:
        raise PreventUpdate

    cols = sorted(set(data[0].keys()))
    opts = [{"label": col, "value": col} for col in cols]

    default_x_axis = try_set_default_axis_value(opts, TasColumns.SIO2)
    default_y_axis = try_set_default_axis_value(opts, TasColumns.K2O_PLUS_NA2O)
    default_grouping_parameter = try_set_default_grouping_parameter(
        opts, [TasColumns.LOCATION, TasColumns.SAMPLE]
    )
    return (
        opts,
        default_x_axis,
        opts,
        default_y_axis,
        opts,
        default_grouping_parameter,
    )


@callback(
    Output(TAS_DIAGRAM, "children"),
    Input(DATA_STORE, "data"),
    Input(TAS_DIAGRAM_X_AXIS_DROPDOWN, "value"),
    Input(TAS_DIAGRAM_Y_AXIS_DROPDOWN, "value"),
    Input(TAS_DIAGRAM_GROUPING_PARAMETER_DROPDOWN, "value"),
    Input(DARK_LIGHT_MODE_TOGGLER, "checked"),
)
def update_tas_diagram(
    data: list[dict[str, Any]],
    x_axis: str,
    y_axis: str,
    grouping_parameter: str,
    is_dark_mode: bool,
) -> html.Div:
    """Update the TAS diagram with the newest data store values."""
    print("Update TAS diagram callback triggered.")
    print(f"{x_axis=}, {y_axis=}, {grouping_parameter=}.")

    if not data or not x_axis or not y_axis:
        print("Did not get any data, plotting empty plot.")
        fig = make_empty_scatter()
        return html.Div(
            dcc.Graph(figure=fig, style={"width": "100%", "height": "80vh"}),
            id=TAS_DIAGRAM,
            style={"width": "100%", "height": "80vh"},
        )

    if not data:
        return html.Div("No data for selected locations.", id=TAS_DIAGRAM)

    df = load_data_from_store(data)
    df = convert_to_numeric_axes(df, x_axis, y_axis)

    if len(df) == 0:
        raise PreventUpdate

    df, group = sanitize_grouping_parameter(df, grouping_parameter, drop_na=False)

    fig = px.scatter(df, x=x_axis, y=y_axis, color=group, symbol=group)
    fig.update_layout(
        title_text="Scatter Plot",
        title_x=0.5,
        xaxis={"gridcolor": "black"},
        yaxis={"gridcolor": "black"},
    )
    axes_configuration = {
        "gridcolor": "black",
        "zeroline": True,
        "zerolinewidth": 5,
        "zerolinecolor": "LightPink",
    }
    fig.update_xaxes(axes_configuration)
    fig.update_yaxes(axes_configuration)
    if is_dark_mode:
        fig.update_layout(template="plotly_dark")
    else:
        fig.update_layout(template="plotly_white")
    fig = create_tas_overlay(fig)
    print("Creating a TAS diagram.")
    return html.Div(
        dcc.Graph(figure=fig, style={"width": "100%", "height": "80vh"}),
        id=TAS_DIAGRAM,
        style={"width": "100%", "height": "80vh"},
    )


def load_data_from_store(data_in: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert serialized data from data store into a `DataFrame`."""
    return pd.DataFrame(data_in)


def convert_to_numeric_axes(df: pd.DataFrame, x_axis: str, y_axis: str) -> pd.DataFrame:
    """Convert the X and Y axes to numerics, coerce the errors and drop NA values."""
    df[x_axis] = pd.to_numeric(df[x_axis], errors="coerce")
    df[y_axis] = pd.to_numeric(df[y_axis], errors="coerce")

    df = df.dropna(subset=[x_axis, y_axis])
    return df


def create_tas_overlay(fig: Any) -> Any:
    for traces in Rocks.to_overlay_traces():
        poly, label = traces
        fig.add_trace(poly.update(visible="legendonly"))
        fig.add_trace(label.update(visible="legendonly"))

    # Each rock contributes 2 overlays: the polygon and the label.
    num_overlay_traces = len(Rocks) * 2

    fig.update_layout(
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "buttons": [
                    {
                        "label": "Toggle overlay",
                        "method": "update",
                        "args2": [
                            {"visible": [True] * len(fig.data)},
                            {
                                "title": {
                                    "text": "TAS Diagram<br>values in [wt%]",
                                    "x": 0.5,
                                },
                            },
                        ],
                        "args": [
                            {
                                "visible": [True] * (len(fig.data) - num_overlay_traces)
                                + [False] * num_overlay_traces,
                            },
                            {
                                "title": {
                                    "text": "Scatter Plot",
                                    "x": 0.5,
                                },
                            },
                        ],
                    },
                ],
                "showactive": True,
                "x": 0.0,
                "y": -0.15,
                "xanchor": "left",
                "yanchor": "top",
            },
        ],
        margin={"t": 120},
    )
    return fig
