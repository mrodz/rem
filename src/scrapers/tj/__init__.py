from definitions import application_logger

LOGGER = application_logger("TJ Scraper")

import csv
import logging
import scrapers.tj.scraper as scraper
from pathlib import Path
from cache import CachedReader

def _write_to_csv(path: str, stores: list[scraper.Shop]):
    p = Path(path)
    
    if not p.suffix.lower() == ".csv":
        raise RuntimeError(f"cannot write to {path}")
    
    with open(path, "w", newline="", encoding="utf-8") as output:
        wr = csv.writer(output, quoting=csv.QUOTE_ALL)
        
        wr.writerow(scraper.Shop.keys())
        wr.writerows([store.values() for store in stores])
    

def scrape(cached_reader: CachedReader, path: str):
    logging.basicConfig(level=logging.INFO)

    stores = scraper.scrape(cached_reader)
    _write_to_csv(path, stores)
    
    LOGGER.info("done")