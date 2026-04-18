'''
Price downloader for ECB data (currencies).
'''

import datetime
import json
import os
import tempfile
from decimal import ROUND_HALF_UP, Decimal
import xml.etree.ElementTree as ET

import requests
from loguru import logger

from alens.pricedl.model import Price
from alens.pricedl.quote import Downloader

ECB_URL = "https://www.ecb.europa.eu/stats/eurofx/eurofxref/eurofxref-daily.xml"
ECB_NS = "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"


class EcbDownloader(Downloader):
    '''
    Downloader for ECB data (currencies).
    '''

    def download(self, security_symbol, currency):
        '''
        Download the price for the given symbol.
        '''
        currency = currency.upper()
        if not currency == 'EUR':
            raise ValueError("Only EUR is supported")
        symbol = security_symbol.mnemonic.upper()
        logger.debug(f"Downloading price for {symbol} in {currency}")

        if self.daily_cache_exists():
            logger.debug(f"Using cached daily rates: {self.get_cache_path()}")
            data = self.read_daily_cache()
        else:
            data = self.fetch_daily_rates()
            self.write_daily_cache(data)

        date = datetime.date.fromisoformat(data["date"])
        rate = data["rates"][symbol]
        # Rates are EUR/currency, so invert to get currency/EUR
        inv_rate = Decimal(1 / rate).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

        return Price(symbol=security_symbol, date=date, value=inv_rate,
                     currency=currency, source="ECB")

    def fetch_daily_rates(self) -> dict:
        '''Fetch and parse ECB daily rates XML.'''
        response = requests.get(ECB_URL, timeout=30)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        # The outer Cube contains a Cube with time=, which contains Cube currency= rate= children
        outer = root.find(f"{{{ECB_NS}}}Cube")
        daily = outer.find(f"{{{ECB_NS}}}Cube")
        date = daily.attrib["time"]
        rates = {c.attrib["currency"]: float(c.attrib["rate"]) for c in daily}

        return {"date": date, "rates": rates}

    def get_cache_path(self) -> str:
        temp_dir = tempfile.gettempdir()
        filename = datetime.date.today().isoformat()
        return os.path.join(temp_dir, f"{filename}-ecb.json")

    def daily_cache_exists(self) -> bool:
        return os.path.exists(self.get_cache_path())

    def write_daily_cache(self, data: dict):
        with open(self.get_cache_path(), "w", encoding="utf-8") as f:
            json.dump(data, f)

    def read_daily_cache(self) -> dict:
        with open(self.get_cache_path(), encoding="utf-8") as f:
            return json.load(f)
