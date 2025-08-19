from __future__ import annotations

from dataclasses import dataclass
import io
import re
import requests
import traceback
from enum import StrEnum
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlparse

import pandas as pd


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


class TableSource(StrEnum):
    ExcelXlsx = "Excel/xlsx"
    ExcelXls = "Excel/xls"
    Csv = "Csv"
    Txt = "Txt"


class ValueDelimiter(StrEnum):
    Comma = ","
    Dot = "."
    Semicolon = ";"


class ThousandSeparator(StrEnum):
    Comma = ","
    Dot = "."


class DecimalSeparator(StrEnum):
    Comma = ","
    Dot = "."


class Encoding(StrEnum):
    """Available encodings.

    TODO: Better would be to iterate over codecs and encodings to create
    a complete list of encodings, but for the sake of this prototype
    it is OK.
    """

    Utf8 = "utf-8"
    Utf16 = "utf-16"
    UnicodeEscape = "unicode_escape"
    Koi8r = "koi8-r"


class Engine(StrEnum):
    Xlrd = "xlrd"
    Openpyxl = "openpyxl"
    Pyxlsb = "pyxlsb"
    Odf = "odf"  # TODO: Make sure this dependency is installed.
    Calamine = "calamine"  # TODO: Make sure this dependency is installed.


def guess_table_source(suffix: str) -> TableSource | None:
    """Guess and assume the table format from the file suffix."""
    print("Table format not supplied, guessing from suffix.")
    if suffix == "xlsx":
        return TableSource.ExcelXlsx
    if suffix == "xls":
        return TableSource.ExcelXls
    if suffix == "csv":
        return TableSource.Csv
    if suffix == "txt":
        return TableSource.Txt

    print(f"Unhandled table format suffix: `{suffix}`.`")
    return None


@dataclass
class SanitizedPandasArgs:
    encoding: str
    value_delimiter: str
    thousands_separator: str | None
    decimal_separator: str
    engine: str | None


def sanitize_pandas_arguments(
    encoding: Encoding | str,
    value_delimiter: ValueDelimiter | str,
    thousands_separator: ThousandSeparator | str | None,
    decimal_separator: DecimalSeparator | str,
    engine: Engine | str | None,
) -> SanitizedPandasArgs:
    if isinstance(encoding, Encoding):
        encoding = encoding.value
    if isinstance(value_delimiter, ValueDelimiter):
        value_delimiter = value_delimiter.value
    if isinstance(thousands_separator, ThousandSeparator):
        thousands_separator = thousands_separator.value
    if isinstance(decimal_separator, DecimalSeparator):
        decimal_separator = decimal_separator.value
    if isinstance(engine, Engine):
        engine = engine.value
    return SanitizedPandasArgs(
        encoding,
        value_delimiter,
        thousands_separator,
        decimal_separator,
        engine,
    )


def load_table(
    source: Path | str | io.StringIO | bytes,
    *,
    table_source: TableSource | None = None,
    encoding: Encoding | str = Encoding.Utf8,
    value_delimiter: ValueDelimiter | str = ValueDelimiter.Comma,
    thousands_separator: ThousandSeparator | str | None = None,
    decimal_separator: DecimalSeparator | str = DecimalSeparator.Dot,
    engine: Engine | str | None = None,
) -> pd.DataFrame | None:
    """Load tabular data to display."""
    sanitized_args = sanitize_pandas_arguments(
        encoding,
        value_delimiter,
        thousands_separator,
        decimal_separator,
        engine,
    )

    # Loading a file from a path source.
    if isinstance(source, (str, Path)):
        print("Assuming data is a sort of path.")
        path = Path(source)
        suffix = path.suffix

        # We deduce the format ourselves, from the suffix.
        if table_source is None:
            table_source = guess_table_source(suffix)
            # If we cannot guess, return to handler.
            if table_source is None:
                return None
            print(f"Guessed: `{table_source}`.")
        else:
            print(f"Table format supplied: `{table_source}`.")

        # By now we should have a file format, either guessed or forced.

        if table_source in (TableSource.ExcelXlsx, TableSource.ExcelXls):
            print("Loading `read_excel`.")
            return pd.read_excel(
                path,
                thousands=sanitized_args.thousands_separator,
                decimal=sanitized_args.decimal_separator,
                engine=sanitized_args.engine,
            )

        if table_source == TableSource.Csv:
            print("Loading `read_csv`.")
            return pd.read_csv(
                path,
                encoding=sanitized_args.encoding,
                delimiter=sanitized_args.value_delimiter,
                thousands=sanitized_args.thousands_separator,
                decimal=sanitized_args.decimal_separator,
                engine=sanitized_args.engine,
            )

    # Assume source is bytes.
    print("Assuming loaded data is bytes.")
    try:
        if isinstance(source, bytes):
            # Assume bytes means file upload.
            try:
                print("Loading `read_excel`.")
                return pd.read_excel(
                    io.BytesIO(source),
                    thousands=sanitized_args.thousands_separator,
                    decimal=sanitized_args.decimal_separator,
                    engine=sanitized_args.engine,
                )
            except Exception:
                print("Loading `read_csv`.")
                return pd.read_csv(
                    io.BytesIO(source),
                    encoding=sanitized_args.encoding,
                    delimiter=sanitized_args.value_delimiter,
                    thousands=sanitized_args.thousands_separator,
                    decimal=sanitized_args.decimal_separator,
                    engine=sanitized_args.engine,
                )
        elif isinstance(source, str | Path):
            print("Loading `read_csv`.")
            return pd.read_csv(
                source,
                encoding=sanitized_args.encoding,
                delimiter=sanitized_args.value_delimiter,
                thousands=sanitized_args.thousands_separator,
                decimal=sanitized_args.decimal_separator,
                engine=sanitized_args.engine,
            )
    except Exception as e:
        print(f"Error loading data: {e}")
        print(traceback.format_exc())
        return None
    return None


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
    """Load data from a URL, such as Google Sheets."""
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
