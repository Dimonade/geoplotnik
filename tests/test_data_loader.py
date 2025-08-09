from geoplotnik.data.loaders import is_compound_in_data
from geoplotnik.data.loaders import TasColumns

import pandas as pd
import pytest


@pytest.mark.parametrize(
    ("cols", "needle", "expected"),
    [
        # Exact match.
        (["K2O"], TasColumns.K2O, ["K2O"]),
        # Case-insensitive match.
        (["na2o_ppm"], TasColumns.NA2O, ["na2o_ppm"]),
        (["Na2O_PPM"], TasColumns.NA2O, ["Na2O_PPM"]),
        # No match.
        (["CaO", "MgO"], TasColumns.NA2O, None),
        # Multiple matches.
        (["Na2O", "Total_Na2O"], TasColumns.NA2O, ["Na2O", "Total_Na2O"]),
        # Partial match but unrelated compound.
        (["Na2O3"], TasColumns.NA2O, ["Na2O3"]),
        # Special chars and spaces.
        (["Na2O (ppm)"], TasColumns.NA2O, ["Na2O (ppm)"]),
        ([" Na2O"], TasColumns.NA2O, [" Na2O"]),
        # Substring inside longer string.
        (["SomeNa2OValue"], TasColumns.NA2O, ["SomeNa2OValue"]),
    ],
)
def test_compound_found_in_columns(
    cols: list[str],
    needle: str,
    expected: list[str] | None,
):
    df = pd.DataFrame(columns=cols)
    assert is_compound_in_data(df.columns, needle) == expected
