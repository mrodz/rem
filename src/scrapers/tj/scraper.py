from . import LOGGER

from dataclasses import dataclass, fields
import json
import urllib.parse
from bs4 import BeautifulSoup
from typing import Optional, TypedDict, Literal
from cache import CachedReader


SIZE = 631
STATES_LIST_URL = "https://locations.traderjoes.com"
ADDRESS_QUERY = "https://nominatim.openstreetmap.org/search"


# https://schema.org/PostalAddress
PostalAddress = TypedDict(
    "PostalAddress",
    {
        "@context": Literal["https://schema.org"],
        "@type": Literal["PostalAddress"],
        "@id": str,
        "name": str,
        "streetAddress": str,
        "addressLocality": str,
        "addressRegion": str,
        "postalCode": str,
        "addressCountry": Literal["US"],
        "telephone": str,
    },
)


def address_to_lat_lon(cached_reader: CachedReader, address: str) -> Optional[tuple[float, float]]:
    params = { 'q': address, 'format': 'json' }
    query_string = urllib.parse.urlencode(params)
    url = ADDRESS_QUERY + '?' + query_string
    
    response = cached_reader.get(url, headers={'User-Agent': 'trader-joes lat and long finder'})
    
    response_as_json = json.loads(response)
    
    if len(response_as_json) == 0:
        return None
    
    first_result = response_as_json[0]
    
    if not isinstance(first_result, dict):
        raise ValueError('expected object')
    
    lat = first_result["lat"]
    lon = first_result["lon"]
    
    return (lat, lon)
    

@dataclass(frozen=True)
class Shop:
    url: str
    name: str
    street_address: str
    region: str
    postal_code: str
    country: str
    telephone: str
    lat: float
    long: float
    
    
    @classmethod
    def keys(cls):
        return [f.name for f in fields(cls)]
    
    
    def values(self):
        return [getattr(self, f.name) for f in fields(self)]
    
        
    @classmethod
    def from_schema(cls, cached_reader: CachedReader, schema: PostalAddress):
        address = None
        
        # edge cases for addresses that cannot be queried
        # i.e. not up to date, include unnecessary fluff
        # like prefixes to streets, and wrong county
        match schema.get('telephone'):
            case '+1 480-712-6645':
                address = '14770 W McDowell Rd, Goodyear, AZ 85395'
            case '+1 480-367-8920':
                address = '7555 Frank Lloyd Wright, Scottsdale, AZ 85260'
            case '+1 623-546-1640':
                address = '14095 Grand Ave, Surprise, AZ 85374'
            case '+1 510-538-2738':
                address = '22224, Redwood Road, Alameda County, California, 94546, United States'
            case '+1 510-524-7609':
                address = '225, Stannage Avenue, Albany Hill, El Cerrito, Alameda County, California, 94530, United States'
            case '+1 323-856-0689':
                address = '1600, Vine Street, Hollywood, Los Angeles, Los Angeles County, California, 90028, United States'
            case '+1 310-725-9800':
                address = '1800, Rosecrans Avenue, Manhattan Village, Manhattan Beach, Los Angeles County, California, 90266, United States'
            case '+1 949-494-7404':
                address = '8086, Sidra Cove, Crystal Cove, Newport Coast, Newport Beach, Orange County, California, 92657, United States'
            case '+1 818-762-2963':
                address = '6130, Laurel Canyon Boulevard, North Hollywood Neighborhood Council District, Los Angeles, Los Angeles County, California, 91606, United States'
            case '+1 408-264-8120':
                address = "Trader Joe's, 5353, Almaden Expressway, San Jose, Santa Clara County, California, 95118, United States"
            case '+1 650-583-6401':
                address = "Trader Joe's, 301, McLellan Drive, South San Francisco, San Mateo County, California, 94080, United States"
            case '+1 805-434-9562':
                address = "Trader Joe's, 1111, Rossi Road, San Luis Obispo County, California, 93465, United States"
            case '+1 562-698-1642':
                address = "Trader Joe's, 15025, Whittier Boulevard, Friendly Hills, Whittier, Los Angeles County, California, 90603, United States"
            case '+1 561-338-5031':
                address = '855, Southeast 9th Street, Boca Raton, Palm Beach County, Florida, 33432, United States'
            case '+1 727-436-4019':
                address = '33591, West Lake Road, Palm Harbor, Pinellas County, Florida, 34683, United States'
            case '+1 561-656-1067':
                address = '2877, Stribling Way, Wellington, Palm Beach County, Florida, 33414, United States'
            case '+1 470-762-3171':
                address = "Trader Joe's, Halcyon Days Trail, Forsyth County, Georgia, 30005, United States"
            case '+1 208-214-8293':
                address = "303, East Spokane Avenue, Coeur d'Alene, Kootenai County, Idaho, 83814, United States"
            case '+1 574-472-8744':
                address = '1140, Howard Street, Harters Heights, South Bend, Saint Joseph County, Indiana, 46617, United States'
            case '+1 502-895-7872':
                address = "Trader Joe's, 4600 Shelbyville Rd, Louisville, KY 40207"
            case '+1 508-790-3008':
                address = '655 Iyannough Road, Hyannis, MA 02601'
            case '+1 775-267-2486':
                address = '3790, US 395, Carson City, Douglas County, Nevada, 89705, United States'
            case '+1 973-537-3672':
                address = '3056, NJ 10, Denville, Morris County, New Jersey, 07834, United States'
            case '+1 732-462-1539':
                address = "Trader Joe's, Pond Road, Whittier Oaks South, Freehold Township, Monmouth County, New Jersey, 07728, United States"
            case '+1 856-988-3323':
                address = "Trader Joe's, 300, SR 73, Marlton Square, Marlton, Evesham Township, Burlington County, New Jersey, 08053, United States"
            case '+1 201-265-9624':
                address = "Trader Joe's, 404, Sette Drive, Paramus, Bergen County, New Jersey, 07652, United States"
            case '+1 505-883-3662':
                address = "Trader Joe's, 2200, Uptown Loop Road Northeast, Uptown, Albuquerque, Bernalillo County, New Mexico, 87110, United States"
            case '+1 518-383-5015':
                address = "Trader Joe's, Halfmoon Crossing, Town of Halfmoon, Saratoga County, New York, 12065, United States"
            case '+1 212-477-8340':
                address = "Trader Joe's, 400, Grand Street, Lower East Side, Manhattan Community Board 3, Manhattan, New York County, New York, 10002, United States"
            case '+1 716-415-3179':
                address = '5017, Transit Road, Eastern Hills, Buffalo, Erie County, New York, 14221, United States'
            case '+1 541-312-4198':
                address = "Trader Joe's, 63455, McKenzie-Bend Highway, Bend, Deschutes County, Oregon, 97703"
            case '+1 541-485-1744':
                address = "85, Coburg Road, Eugene, Lane County, Oregon, 97401, United States"
            case '+1 843-630-6282':
                address = 'Sayebrook Town Center, Sayebrook, Horry County, South Carolina, 29575, United States'
            case '+1 615-356-1066':
                address = '90, Post Place, Nashville, TN 37205'
            case '+1 281-290-4216':
                # this location does not have an address on Google Maps or the OpenStreetMap project. This Kroger is right across the street
                address = 'Kroger Marketplace, 9703, Barker Cypress Road, Towne Lake Management District, Cypress, Harris County, Texas, 77433, United States'
            case '+1 801-571-0987':
                address = "Trader Joe's, 11477, State Street, Draper, Salt Lake County, Utah, 84020, United States"
            case '+1 385-324-2911':
                address = "Trader Joe's, Rodeo Walk Drive, Wagstaff Acres, Holladay, Salt Lake County, Utah, 84117, United States"
            case '+1 801-224-1453':
                address = "Trader Joe's, 440, Park Avenue, University Place, Orem, Utah County, Utah, 84097, United States"
            case '+1 703-379-5883':
                address = "5847 Leesburg Pike, Bailey's Crossroads, VA 22041"
            case '+1 703-288-0566':
                address = "Trader Joe's, 7514, Leesburg Pike, Falls Church, Fairfax County, Virginia, 22043, United States"
            case '+1 703-689-0865':
                address = "Trader Joe's, 11958, Killingsworth Avenue, Fairfax County, Virginia, 20194, United States"
            case '+1 757-259-2135':
                address = '5000, Settlers Market Boulevard, Virginia, 23188, United States'
            case _:
                address = f"{schema.get('streetAddress').split(',')[0]}, {schema.get('addressLocality')}, {schema.get('addressRegion')} {schema.get('postalCode')}"
        
        bundled = address_to_lat_lon(cached_reader, address)

        if bundled is None:
            raise RuntimeError(f'could not get latitude and longitude from address: {address}')
        
        lat, long = bundled

        return cls(
            url=schema.get('@id'),
            name=schema.get('name'),
            country=schema.get('addressCountry'),
            street_address=schema.get('streetAddress'),
            postal_code=schema.get('postalCode'),
            region=schema.get('addressRegion'),
            telephone=schema.get('telephone'),
            lat=lat,
            long=long,
        )


def get_states(cached_reader: CachedReader) -> list[str]:
    states_html = cached_reader.get(STATES_LIST_URL)
    soup = BeautifulSoup(states_html, 'html.parser')

    state_boxes = soup.select("#contentbegin > div > div > div > div:nth-child(2) > div > div > a")

    result = []

    for state in state_boxes:
        url = state.attrs.get('href')

        if url is None:
            raise ValueError(f"element does not have an href: {state}")
        elif not isinstance(url, str):
            raise ValueError(f"href is not a string")

        result.append(STATES_LIST_URL + url)

    return result


def get_cities(cached_reader: CachedReader, state_url) -> list[str]:
    cities_html = cached_reader.get(state_url)

    soup = BeautifulSoup(cities_html, 'html.parser')

    city_boxes = soup.select("#contentbegin > div > div > div > div:nth-child(2) > div > div > a")

    result = []

    for city in city_boxes:
        url = city.attrs.get('href')

        if url is None:
            raise ValueError(f"element does not have an href: {city}")
        elif not isinstance(url, str):
            raise ValueError(f"href is not a string")

        result.append(STATES_LIST_URL + url)

    return result


def get_locations(cached_reader: CachedReader, city_url):
    locations_html = cached_reader.get(city_url)

    soup = BeautifulSoup(locations_html, 'html.parser')

    locations_json = soup.select("#contentbegin > div > div:nth-child(2) > div > script")

    shops = []

    for location in locations_json:
        location_json = location.encode_contents()
        location_dict = json.loads(location_json)
        shop = Shop.from_schema(cached_reader, location_dict)
        
        shops.append(shop)
        
    return shops
        

def scrape(cached_reader) -> list[Shop]:
    counter = 0
    
    states = get_states(cached_reader)
    
    stores = []
    
    for state in states:
        LOGGER.info(f"{counter/SIZE*100:.2f}% - scraping stores under {state}")
        
        cities = get_cities(cached_reader, state)
        
        for city in cities:
            LOGGER.info(f"{counter/SIZE*100:.2f}% - {city}")
            locations = get_locations(cached_reader, city)
            
            for location in locations:
                stores.append(location)
                counter += 1
                
    return stores
