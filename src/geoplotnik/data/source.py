from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from geoplotnik.data.loaders import DataSchema


@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(
        self,
        locations: list[str] | None = None,
    ) -> DataSource:
        if locations is None:
            locations = self.unique_locations

        filtered_data = self._data.query("Location in @locations")
        return DataSource(filtered_data)

    @property
    def row_count(self) -> int:
        return self._data.shape[0]

    @property
    def all_locations(self) -> list[str]:
        return self._data[DataSchema.LOCATION.value].tolist()

    @property
    def unique_locations(self) -> list[str]:
        return sorted(set(self.all_locations), key=str)
