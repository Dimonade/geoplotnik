"""Definitions of the borders of different rock kinds on the TAS diagram."""

from dataclasses import dataclass
from enum import Enum

import plotly.graph_objects as go


@dataclass
class TasBorder:
    name: str
    xs: list[float]
    ys: list[float]
    colour: str = "black"
    visible: bool = True

    def to_scatter(self) -> go.Scatter:
        return go.Scatter(
            x=self.xs,
            y=self.ys,
            mode="lines",
            name=self.name,
            visible=self.visible,
            showlegend=False,
            line={"color": self.colour},
        )

    def is_closed_polygon(self) -> bool:
        """Check whether this is a closed polygon or an open polygon."""
        return self.xs[0] == self.xs[-1] and self.ys[0] == self.ys[-1]

    def clean_duplicates(self) -> tuple[list[float], list[float]]:
        if self.is_closed_polygon():
            return self.xs[:-1], self.ys[:-1]
        else:
            return self.xs, self.ys

    def to_label(self) -> go.Scatter:
        xs, ys = self.clean_duplicates()

        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)

        return go.Scatter(
            x=[cx],
            y=[cy],
            text=[self.name],
            mode="text",
            showlegend=False,
            visible=self.visible,
            textfont={"color": "rgba(0, 0, 0, 0.3)", "size": 10},
            hoverinfo="skip",
        )


# TODO: Not all borders are specified exactly. They are commented out.
class Rocks(Enum):
    """Collection of border coordinates of the different rocks in a TAS diagram."""

    Andesite = TasBorder(name="Andesite", xs=[57, 57, 63, 63], ys=[0, 5.9, 7, 0])
    Basalt = TasBorder(name="Basalt", xs=[45, 45, 52, 52], ys=[0, 5, 5, 0])
    BasalticAndesite = TasBorder(
        name="Basaltic Andesite", xs=[52, 52, 57, 57], ys=[0, 5, 5.9, 0]
    )
    BasalticTrachyandesite = TasBorder(
        name="Basaltic Trachyandesite",
        xs=[52, 49.4, 53, 57, 52],
        ys=[5, 7.3, 9.3, 5.9, 5],
    )
    # Basanite = TasBorder(name="Basanite", xs=[], ys=[])
    Dacite = TasBorder(name="Dacite", xs=[63, 63, 69, 77], ys=[0, 7, 8, 0])
    # Foidite = TasBorder(name="Foidite", xs=[], ys=[])
    Picrobasalt = TasBorder(name="Picrobasalt", xs=[41, 41, 45, 45], ys=[0, 3, 3, 0])
    # Phonolite = TasBorder(name="Phonolite", xs=[], ys=[])
    Phonotephrite = TasBorder(
        name="Phonotephrite",
        xs=[49.4, 45, 48.4, 53, 49.4],
        ys=[7.3, 9.4, 11.5, 9.3, 7.3],
    )
    Rhyolite = TasBorder(name="Rhyolite", xs=[77, 69, 69], ys=[0, 8, 13])
    # Tephrite = TasBorder(name="Tephrite", xs=[], ys=[])
    Trachyandesite = TasBorder(
        name="Trachyandesite", xs=[57, 53, 57.6, 63, 57], ys=[5.9, 9.3, 11.7, 7, 5.9]
    )
    Trachybasalt = TasBorder(
        name="Trachybasalt", xs=[45, 49.4, 52, 45], ys=[5, 7.3, 5, 5]
    )
    # Trachyte = TasBorder(name="Trachyte", xs=[], ys=[])
    # Trachydacite = TasBorder(name="Trachydacite", xs=[], ys=[])
    Tephriphonolite = TasBorder(
        name="Tephriphonolite",
        xs=[53, 48.4, 52.5, 57.6, 53],
        ys=[9.3, 11.5, 14, 11.7, 9.3],
    )

    @classmethod
    def to_overlay_traces(cls) -> list[go.Scatter]:
        """Convert the rock kinds into an overlay collection."""

        return [(member.value.to_scatter(), member.value.to_label()) for member in cls]
