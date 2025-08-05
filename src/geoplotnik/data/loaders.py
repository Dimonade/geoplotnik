import pandas as pd
from enum import Enum
import os
import io
from pathlib import Path


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
            data = pd.read_csv(
                source,
                usecols=[m.value for m in DataSchema.__members__.values()],
            )
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame({"Location": ["Unknown"]})

    data["Location"] = data["Location"].replace("", pd.NA).fillna("Unknown")
    return data
