from .layer import Layer, LayerPointProvider
from .csv_layer import csv_points, CSVImporter
from typing import cast, Optional
import math
import folium


HOSPITAL_LAYER_NAME = "Hospitals"
COLUMNS = ["ID","NAME","ADDRESS","CITY","STATE","ZIP","ZIP4","TELEPHONE","TYPE","STATUS","POPULATION","COUNTY","COUNTYFIPS","COUNTRY","LATITUDE","LONGITUDE","NAICS_CODE","NAICS_DESC","SOURCE","SOURCEDATE","VAL_METHOD","VAL_DATE","WEBSITE","STATE_ID","ALT_NAME","ST_FIPS","OWNER","TTL_STAFF","BEDS","TRAUMA","HELIPAD"]


def _beds(row: list[str]) -> Optional[float]:
    beds = float(row[COLUMNS.index("BEDS")])
    return None if beds < 0 else beds


def hospital_weight(row: list[str]) -> float:
    beds = _beds(row)
    
    if beds is None:
        return 0.3
    
    score = math.log1p(max(beds, 0)) ** 1.15
    
    return 0.5 + min(score / 8.0, 1.0) * 1.5

    
HOSPITAL_IMPORTER = CSVImporter({ "label": "NAME", "lat": "LATITUDE", "lon": "LONGITUDE" }, hospital_weight)


@csv_points("data/hospitals.csv", HOSPITAL_IMPORTER)
class HospitalLayerPointProvider(LayerPointProvider):
    def __init__(self) -> None:
        super().__init__()


class HospitalLayer(Layer):
    """
    Layer of hospitals in America (Data ranging 2012-2020)
    """
    points: HospitalLayerPointProvider
    
    
    def __init__(self) -> None:
        super().__init__()
        # point_list is added by a class decorator at runtime; cast to satisfy static typing
        ConcreteTJ = cast(type[HospitalLayerPointProvider], HospitalLayerPointProvider)
        self.points = ConcreteTJ()
        

    def name(self) -> str:
        return HOSPITAL_LAYER_NAME
        
    
    def radius(self) -> int:
        return 40
    
    
    def icon(self) -> folium.Icon:
        return folium.Icon(
            color="blue",
            icon="hospital",
            prefix="fa"
        )
        

    def lat_long_provider(self) -> HospitalLayerPointProvider:
        return self.points
