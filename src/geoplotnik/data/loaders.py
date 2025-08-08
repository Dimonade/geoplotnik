import io
import os
import re
from enum import Enum
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlparse

import pandas as pd
import requests


class DataSchema(Enum):
    LOCATION = "Location"
    SIO2 = "SiO2"
    TIO2 = "TiO2"
    AL2O3 = "Al2O3"
    FE2O3T = "Fe2O3T"
    MNO = "MnO"
    MGO = "MgO"
    CAO = "CaO"
    NA2O = "Na2O"
    K2O = "K2O"
    P2O5 = "P2O5"


def load_data(source: Path | str | io.StringIO | bytes | None = None) -> pd.DataFrame:
    """Load tabular data to display."""
    if source is None:
        print("No data source provided.")
        source = os.getenv("DEFAULT_DATA", None)
        if source in (None, "{DEFAULT_DATA}"):
            print("`DEFAULT_DATA` environment variable is not set.")
            print("Loading default data from assets.")
            return pd.read_csv("assets/data/tas_diagram/default.csv")

    try:
        if isinstance(source, bytes):
            # Assume bytes means file upload.
            try:
                data = pd.read_excel(io.BytesIO(source))
            except Exception:
                data = pd.read_csv(io.BytesIO(source))
        elif isinstance(source, str | Path):
            data = pd.read_csv(source)
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
