from abc import ABC, abstractmethod
from collections import deque
from typing import Iterable, TypedDict, Optional
import folium
from folium.plugins import HeatMap, MarkerCluster
from itertools import chain

class Point(TypedDict):
    lat: float
    lon: float
    w: float
    label: str


class LayerPointProvider(ABC):
    @abstractmethod
    def point_list(self) -> Iterable[Point]:
        ...
        

class Layer(ABC):
    def add_to_map(self, map: folium.Map):
        heat_data = [[p["lat"], p["lon"], p["w"]] for p in self.lat_long_provider().point_list()]
        
        HeatMap(
            heat_data,
            radius=30,        # blob size
            blur=22,          # smoothness
            min_opacity=0.25, # see base map through
            max_zoom=13,
            name=self.name(),
        ).add_to(map)
    
    @abstractmethod
    def lat_long_provider(self) -> LayerPointProvider:
        ...
        
    @abstractmethod
    def name(self) -> str:
        ...
        
    
class Stack:
    layers: deque[Layer]
    __center: Optional[tuple[float, float]]
    
    def __init__(self) -> None:
        self.layers = deque()
        self.__center = None
        
    def add(self, layer: Layer):
        self.__center = None
        self.layers.append(layer)
        
    def center(self) -> tuple[float, float]:
        if self.__center is not None:
            return self.__center
        
        points = list(chain.from_iterable(layer.lat_long_provider().point_list() for layer in self.layers))
        
        self.__center = (sum(p["lat"] for p in points)/len(points),
                         sum(p["lon"] for p in points)/len(points))
        
        return self.__center
                
    def __str__(self) -> str:
        return str([layer.name() for layer in self.layers])
    
    def render(self) -> folium.Map:
        m = folium.Map(
            location=self.center(),
            zoom_start=5,
            tiles="CartoDB positron"
        )
        
        for layer in self.layers:
            layer.add_to_map(m)
            
        return m
    
