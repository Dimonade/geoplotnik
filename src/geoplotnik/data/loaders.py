import pandas as pd
from enum import Enum
import os
import io
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


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
        source = os.getenv("DEFAULT_DATA", None)
        if source is None:
            return pd.DataFrame({"Location": ["Unknown"]})

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


def load_data_(source: Path | str | io.StringIO | None = None) -> pd.DataFrame:
    """Load tabular data to display."""
    if source is None:
        try:
            source = os.getenv("DEFAULT_DATA")
        except Exception as e:
            print(e)

    assert source is not None
    data = pd.read_csv(
        source,
        usecols=[m.value for m in DataSchema.__members__.values()],
        dtype={
            DataSchema.LOCATION: str,
            DataSchema.MGO: float,
            DataSchema.SIO2: float,
            DataSchema.TIO2: float,
        },
    )
    data["Location"] = data["Location"].replace("", pd.NA).fillna("Unknown")
    return data
