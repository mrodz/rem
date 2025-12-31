from collections.abc import Callable
from typing import Optional, Self, TypedDict, TypeVar

from .layer import Point

class PointDict(TypedDict):
    lat: str
    lon: str
    label: str

class CSVImporter:
    mapping: PointDict
    weight: float | Callable[[list[str]], float]

    @classmethod
    def default(cls: type[Self]) -> Self: 
        """
        Weight = 1
        
        ## Maps from
        
        | Key   | Value   |
        |------ | ------- |
        | lat   | lat     |
        | lon   | lon     |
        | label | label   |
        """
        ...

    def __init__(self, mapping: PointDict, weight: float | Callable[[list[str]], float] = ...) -> None: ...
    def __call__(self, header: list[str], row: list[str]) -> Point: ...
    
_C = TypeVar("_C", bound=type)

def csv_points(
    file: str,
    transformer: Optional[Callable[[list[str], list[str]], Point]] = ...,
) -> Callable[[_C], _C]: 
    """
    Decorator to implement LayerPointProvider from a CSV file
    
    :param file: A path to a .csv file
    :type file: str
    :param transformer: A function that, given the headers of a CSV file and their corresponding rows, produces a Point
    :type transformer: Optional[Callable[[list[str], list[str]], Point]]
    :return: A decorated class
    :rtype: Callable[[_C], _C]
    """
    ...
