"""
Vanguard AU price downloader using the detail data.
https://www.vanguard.com.au/personal/api/products/personal/fund/8105/detail

Valid as of 2023-05.
As of 2023-10, the fund codes have changed.

The fund page is at
https://www.vanguard.com.au/personal/invest-with-us/fund?productType=managed+fund&portId=8105&tab=prices-and-distributions
but the prices are retrieved as JSON from
https://www.vanguard.com.au/personal/api/products/personal/fund/8105/prices?limit=-1
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, getcontext
from typing import Dict, Tuple

import aiohttp

# Set precision for Decimal, if needed, though for simple storage and retrieval it might not be strictly necessary
# getcontext().prec = 28 # Default is 28, usually sufficient

@dataclass
class SecuritySymbol:
    '''A security symbol'''
    namespace: str
    symbol: str

    def __init__(self, full_symbol: str):
        if ":" not in full_symbol:
            raise ValueError("Symbol must be in 'NAMESPACE:SYMBOL' format")
        self.namespace, self.symbol = full_symbol.split(":", 1)

    def __str__(self) -> str:
        return f"{self.namespace}:{self.symbol}"

@dataclass
class Price:
    '''The price for a commodity'''
    date: str = ""
    value: int = 0  # Mantissa
    denom: int = 1  # Denominator (e.g., 100 for 2 decimal places, 1000 for 3)
    currency: str = ""

class VanguardAu3Downloader:
    '''Downloader for Vanguard mutual funds prices'''
    def __init__(self):
        self.funds_map: Dict[str, str] = {
            # "VANGUARD:BOND": "8123",
            # "VANGUARD:HINT": "8146",
            "VANGUARD:PROP": "8105",  # VAN0004AU
            "VANGUARD:HY": "8106",  # VAN0104AU
        }

    def get_url(self, symbol: SecuritySymbol) -> str:
        '''Creates the URL for the fund'''
        sec_symbol_str = str(symbol)
        fund_id = self.funds_map.get(sec_symbol_str)
        if fund_id is None:
            raise ValueError(f"Fund ID not found for symbol: {sec_symbol_str}")

        result = f"https://www.vanguard.com.au/personal/api/products/personal/fund/{fund_id}/detail?limit=-1"
        # print(f"DEBUG: url: {result}") # Corresponds to log::debug!
        return result

    async def _dl_price(self, symbol: SecuritySymbol) -> Tuple[str, str, str]:
        """
        Returns the latest retail fund price.
        (date_str, price_str, currency_str)
        """
        url = self.get_url(symbol)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
                content = await response.text()

        content_json = json.loads(content)
        data = content_json["data"][0]
        
        prices = data["navPrices"]
        if not prices:
            raise ValueError(f"No price data found for symbol {symbol} at {url}")
            
        latest = prices[0] # Assuming the first one is the latest

        date_str = latest["asOfDate"] # No need to replace quotes, json.loads handles it
        price_str = str(latest["price"]) # Ensure it's a string for Decimal conversion
        currency_str = latest["currencyCode"] # No need to replace quotes

        return date_str, price_str, currency_str

    def _parse_price(self, date_str: str, price_str: str, currency_str: str) -> Price:
        p = Price()

        # Parse date
        dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
        p.date = dt_obj.strftime("%Y-%m-%d")

        # Parse decimal value
        value_decimal = Decimal(price_str)
        
        # Deconstruct Decimal into mantissa and exponent for storage
        # sign, digits, exponent = value_decimal.as_tuple()
        # if sign: # Handle negative numbers if necessary, though prices are usually positive
        #     p.value = -int("".join(map(str, digits)))
        # else:
        #     p.value = int("".join(map(str, digits)))

        # A more direct way to get mantissa for positive numbers
        # If price can be "123.45", scale is 2, exponent is -2
        # Mantissa is 12345
        # Denom is 10^2 = 100
        
        # value_decimal.scaleb(abs(value_decimal.as_tuple().exponent)) gives the integer part
        # For "1.234", as_tuple() -> (0, (1,2,3,4), -3)
        # Mantissa is 1234. Denom is 10^3 = 1000
        
        sign, digits, exponent = value_decimal.as_tuple()
        
        num_str = "".join(map(str,digits))
        p.value = int(num_str)
        if sign:
            p.value = -p.value

        if exponent < 0:
            p.denom = 10**abs(exponent)
        else: # if exponent is 0 or positive (e.g. Decimal('123E+2'))
            p.value *= (10**exponent)
            p.denom = 1


        p.currency = currency_str

        return p

    async def download(self, security_symbol: SecuritySymbol, currency: str) -> Price:
        # The `currency` parameter is not used in the Rust version's dl_price logic,
        # as the API returns the currency. We'll keep it for interface consistency if needed.
        if security_symbol.namespace.upper() != "VANGUARD":
            raise ValueError("Only Vanguard symbols are handled by this downloader!")

        date_str, price_str, currency_api = await self._dl_price(security_symbol)

        # Optionally, you could validate currency_api against the input `currency` if required.
        # For now, we use the currency from the API.

        price_obj = self._parse_price(date_str, price_str, currency_api)
        return price_obj
