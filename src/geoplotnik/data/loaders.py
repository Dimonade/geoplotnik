import io
import os
import re
from enum import StrEnum
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlparse

import pandas as pd
import requests


class TasColumns(StrEnum):
    """Expected to be found columns in a TAS diagram dataset."""

    LOCATION = "Location"
    SAMPLE = "Sample"
    AL2O3 = "Al2O3"
    CAO = "CaO"
    FE2O3T = "Fe2O3T"
    K2O = "K2O"
    MGO = "MgO"
    MNO = "MnO"
    NA2O = "Na2O"
    P2O5 = "P2O5"
    SIO2 = "SiO2"
    TIO2 = "TiO2"
    K2O_PLUS_NA2O = "K2O + Na2O"


def is_compound_in_data(cols: list[str], needle: str) -> list[str] | None:
    """Check if a compound exist in the supplied columns in the dataset."""
    casefold_needle = needle.casefold()

    matches = [col for col in cols if casefold_needle in col.casefold()]

    # If we have multiple matches, check if there is an exact match.
    if len(matches) > 1:
        for m in matches:
            if needle.casefold() == m.casefold():
                print(f"Found exact column match: {m}.")
                return [m]

    return matches if matches else None


def prepare_columns_for_tas(data_in: pd.DataFrame) -> pd.DataFrame:
    """Try to prepare SiO2 and Na2O+K2O columns for default X and Y axes."""
    print("Preparing columns for TAS axes.")
    columns = [c.strip() for c in data_in.columns]
    is_sio2_in = is_compound_in_data(columns, TasColumns.SIO2)
    is_k2o_in = is_compound_in_data(columns, TasColumns.K2O)
    is_na2o_in = is_compound_in_data(columns, TasColumns.NA2O)
    print(f"Found columns: {is_sio2_in}; {is_k2o_in}; {is_na2o_in}.")

    # If columns do not exist, return the data as is.
    if None in (is_sio2_in, is_k2o_in, is_na2o_in):
        print(
            "One of the required columns is missing: "
            f"{is_sio2_in=}, {is_k2o_in=}, {is_na2o_in}."
        )
        return data_in

    assert is_sio2_in is not None
    assert is_k2o_in is not None
    assert is_na2o_in is not None

    # Must have only one column of each.
    if len(is_sio2_in) != 1 or len(is_k2o_in) != 1 or len(is_na2o_in) != 1:
        print("One of the required columns componds appears in multiple places.")
        return data_in

    # If the K2O + Na2O already exists, then it will show for both `is_*_in`'s.
    if len({*(is_k2o_in + is_na2o_in)}) == 1:
        return data_in

    # Otherwise, construct the sum column.
    data_in[TasColumns.K2O_PLUS_NA2O] = data_in[is_k2o_in[0]] + data_in[is_na2o_in[0]]
    return data_in


def load_data(source: Path | str | io.StringIO | bytes | None = None) -> pd.DataFrame:
    """Load tabular data to display."""
    if source is None:
        print("No data source provided.")
        source = os.getenv("DEFAULT_DATA", None)
        if source in (None, "{DEFAULT_DATA}"):
            print("`DEFAULT_DATA` environment variable is not set.")
            print("Loading default data from assets.")
            return prepare_columns_for_tas(
                pd.read_csv("assets/data/tas_diagram/default.csv")
            )

    try:
        if isinstance(source, bytes):
            # Assume bytes means file upload.
            try:
                data = prepare_columns_for_tas(pd.read_excel(io.BytesIO(source)))
            except Exception:
                data = prepare_columns_for_tas(pd.read_csv(io.BytesIO(source)))
        elif isinstance(source, str | Path):
            data = prepare_columns_for_tas(pd.read_csv(source))
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame({"Location": ["Unknown"]})

    return data


def convert_gsheet_url_to_csv(url: str) -> str:
    """Convert the Google sheet link into a tabular-able data source."""
    if "docs.google.com/spreadsheets" not in url:
        return url

    # Extract sheet_id from URL path.
    m = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if not m:
        return url

    sheet_id = m.group(1)

    # Try to get `gid`` from query parameters or fragment.
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    gid = None

    # `gid`` is sometimes in query or fragment.
    if "gid" in query_params:
        gid = query_params["gid"][0]
    else:
        frag = parsed.fragment
        if frag.startswith("gid="):
            gid = frag[4:]

    if gid is None:
        # Default to first sheet.
        gid = "0"

    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&gid={gid}"


def load_data_from_url(url: str) -> pd.DataFrame | None:
    print(f"Fetching URL: `{url}`.")

    # The data is either truly online, ...
    if url.startswith(("http://", "https://")):
        url = convert_gsheet_url_to_csv(
            url
        )  # Is it a strange Google sheet export link?
        resp = requests.get(url, timeout=15, allow_redirects=True)
        resp.raise_for_status()
        return load_data(resp.content)

    # ... or in a local server path, ...
    url_path = Path(url)
    if Path.exists(url_path):
        with Path.open(url_path, "rb") as fh:
            return load_data(fh.read())
    # ... or it is something else, and we will deal with that as the need arises.
    else:
        print(f"An unhandled URL was passed: `{url}`.")
        return None
