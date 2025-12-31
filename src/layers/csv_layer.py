import abc
import csv
from pathlib import Path
from typing import Callable, TypedDict, Optional, Iterable
from .layer import Point
from dataclasses import dataclass


class PointDict(TypedDict):
    lat: str
    lon: str
    label: str


class CSVImporter:
    mapping: PointDict
    weight: float | Callable[[list[str]], float]
    __lat_idx: Optional[int] = None
    __lon_idx: Optional[int] = None
    __label_idx: Optional[int] = None
    
    
    def __init__(self, mapping: PointDict, weight: float | Callable[[list[str]], float] = 1.0):
        self.mapping = mapping
        self.weight = weight
        
    
    @classmethod
    def default(cls):
        return cls({ "lat": "lat", "lon": "lon", "label": "label" }, 1)    
    
    
    def __label(self, header: list[str], row: list[str]) -> str:
        if self.__label_idx is not None:
            return row[self.__label_idx]
        
        try:
            self.__label_idx = header.index(self.mapping["label"])
        except ValueError:
            raise TypeError(f"{self.mapping["label"]} is not in the header")
            
        return row[self.__label_idx]
    
    
    def __lat(self, header: list[str], row: list[str]) -> str:
        if self.__lat_idx is not None:
            return row[self.__lat_idx]
        
        try:
            self.__lat_idx = header.index(self.mapping["lat"])
        except ValueError:
            raise TypeError(f"{self.mapping["lat"]} is not in the header")
            
        return row[self.__lat_idx]
    
    
    def __lon(self, header: list[str], row: list[str]) -> str:
        if self.__lon_idx is not None:
            return row[self.__lon_idx]
        
        try:
            self.__lon_idx = header.index(self.mapping["lon"])
        except ValueError:
            raise TypeError(f"{self.mapping["lon"]} is not in the header")
            
        return row[self.__lon_idx]
    
    
    def __call__(self, header: list[str], row: list[str]) -> Point:
        label = self.__label(header, row)
        lat = float(self.__lat(header, row))
        lon = float(self.__lon(header, row))
        
        w = float(self.weight(row) if callable(self.weight) else self.weight)
        
        return Point(lat=lat, lon=lon, w=w, label=label)

        
def csv_points(file: str, transformer: Optional[Callable[[list[str], list[str]], Point]] = None):
    if transformer is None:
        transformer = CSVImporter.default()
    
    p = Path(file)
    
    if not p.suffix.lower() == ".csv":
        raise RuntimeError(f"cannot read from {file}")
    
    points = []
    
    with open(file, "r", newline="", encoding="utf-8") as output:
        r = csv.DictReader(output)
        
        if r.fieldnames is None:
            raise ValueError("CSV has no header row")
        
        fieldnames = [h.strip() for h in r.fieldnames]
        r.fieldnames = fieldnames
        
        for line_no, row in enumerate(r, start=2):
            if row is None:
                continue

            if all((v is None or str(v).strip() == "") for v in row.values()):
                continue
            
            if len(row) != len(fieldnames):
                raise ValueError(
                    f"Row length mismatch at line {line_no}: "
                    f"expected {len(fieldnames)} fields, got {len(row)}"
                )
            
            points.append(transformer(fieldnames, list(row.values())))
    
    
    def result(cls):
        existing = getattr(cls, "point_list", None)
        
        if existing is not None and not getattr(existing, "__isabstractmethod__", False):
            raise TypeError(f"{cls.__name__} already has a concrete point_list")
        
        if any("_p" in base.__dict__ for base in cls.__mro__):
            raise TypeError(f"{cls.__name__} has state _p")
              
        cls._p = points
        
        def point_list(self):
            return self._p
        
        cls.point_list = point_list
        abc.update_abstractmethods(cls)
        
        return cls
    
    
    return result
