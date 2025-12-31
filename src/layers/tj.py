from .layer import Layer, LayerPointProvider
from .csv_layer import csv_points, CSVImporter
from typing import cast


TJ_IMPORTER = CSVImporter({ "label": "name", "lat": "lat", "lon": "long" })
TJ_LAYER_NAME = "Trader Joe's Layer"

@csv_points("data/tj.csv", TJ_IMPORTER)
class TJLayerPointProvider(LayerPointProvider):
    def __init__(self) -> None:
        super().__init__()


class TJLayer(Layer):
    """
    Layer of every Trader Joe's in America (as of 12/31/2025)
    """
    points: TJLayerPointProvider
    
    def __init__(self) -> None:
        super().__init__()
        # point_list is added by a class decorator at runtime; cast to satisfy static typing
        ConcreteTJ = cast(type[TJLayerPointProvider], TJLayerPointProvider)
        self.points = ConcreteTJ()
        

    def name(self) -> str:
        return TJ_LAYER_NAME
        

    def lat_long_provider(self) -> TJLayerPointProvider:
        return self.points
