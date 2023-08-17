# working..
# ref: https://github.com/pydantic/pydantic-extra-types/blob/main/pydantic_extra_types/coordinate.py

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_core._pydantic_core import ArgsKwargs


class Longitude(float):
    min: ClassVar[float] = -180
    max: ClassVar[float] = 180

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: type[Any], _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.float_schema(ge=cls.min, le=cls.max)


class Latitude(float):
    min: ClassVar[float] = -90
    max: ClassVar[float] = 90

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: type[Any], _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.float_schema(ge=cls.min, le=cls.max)


class Coordinate(BaseModel):
    longitude: Longitude
    latitude: Latitude

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: type[Any], _handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        ...

    @classmethod
    def _parse_tuple(cls, value: Any, handler: core_schema.ValidatorFunctionWrapHandler) -> Any:
        if not isinstance(value, tuple):
            return value
        return ArgsKwargs(args=handler(value))

    def __str__(self) -> str:
        return f"{self.longitude},{self.latitude}"


class _GeoJSON(BaseModel):
    type: Literal[
        "Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon", "GeometryCollection"
    ]


class Point(_GeoJSON):
    coordinates: list


class LineString(_GeoJSON):
    coordinates: list


class Polygon(_GeoJSON):
    coordinates: list


class MultiPoint(_GeoJSON):
    coordinates: list


class MultiLineString(_GeoJSON):
    coordinates: list


class MultiPolygon(_GeoJSON):
    coordinates: list


class GeometryCollection(_GeoJSON):
    geometries: list
