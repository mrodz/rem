import requests
import shelve

def get_data(cache_path, key, computed_value = lambda: None, *, recompute = False):
    with shelve.open(cache_path) as db:
        if recompute or not key in db:
            value = computed_value()

            if not isinstance(value, str):
                raise ValueError("value was not a string")

            db[key] = value

            return value
        else:
            value = db[key]
            return value


DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

class CachedReader:
    cache_path: str
    
    def __init__(self, cache_path: str) -> None:
        self.cache_path = cache_path
    
    
    def get_uncached(self, url, headers):
        response = requests.get(url, headers=headers)
        return response.text


    def get(self, url, headers=DEFAULT_HEADERS, *, recompute = False):
        return get_data(self.cache_path, url, computed_value = lambda: self.get_uncached(url, headers), recompute=recompute)
