from abc import ABC, abstractmethod
from typing import Iterable, TypedDict
import folium

class Point(TypedDict):
    """
    Docstring for Point
    
    :var lat: Latitude in decimal degrees
    :vartype lat: float
    :var lon: Longitude in decimal degrees
    :vartype lon: float
    :var w: Weight associated with the point
    :vartype w: float
    :var label: Human-readable label for the point
    :vartype label: str
    """


class LayerPointProvider(ABC):
    """
    Abstract provider of geographic points.

    Implementations are responsible for supplying a collection of
    `Point` objects. Providers may load points from CSV files, APIs,
    databases, or other sources.
    """

    @abstractmethod
    def point_list(self) -> Iterable[Point]:
        """
        Return an iterable of geographic points.

        Implementations may return a list, generator, or other iterable.
        """
        ...


class Layer(ABC):
    """
    Abstract geographic layer.

    A layer exposes its geographic data indirectly via a
    `LayerPointProvider`.
    """

    def set_enabled(self, enabled: bool): ...
    """
    Set whether this layer is enabled
    """
    
    def is_enabled(self) -> bool: ...
    """
    Get whether this layer is enabled
    """

    @abstractmethod
    def lat_long_provider(self) -> LayerPointProvider:
        """
        Return the point provider associated with this layer.
        """
        ...
    
    @abstractmethod
    def name(self) -> str:
        """
        Return the name of this layer.
        """
        ...
    
    @abstractmethod
    def radius(self) -> int:
        """
        Return the radius of the heat map bubbles this layer produces
        """
        ...
        
    @abstractmethod
    def icon(self) -> folium.Icon:
        """
        Icon for the markers produced by this layer
        """
        ...
        
    
class Stack:
    """
    Docstring for Stack
    """
    
    def __init__(self) -> None: ...
    def add(self, layer: Layer): ...
    def center(self) -> tuple[float, float]: ...
    def __str__(self) -> str: ...
    def render(self) -> folium.Map: ...