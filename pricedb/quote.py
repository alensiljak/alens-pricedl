"""
Quote implementation in Python.
Fetching prices.

Based on [Price Database](https://gitlab.com/alensiljak/price-database),
Python library.
"""
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from .model import Price, SecuritySymbol


class Downloader(ABC):
    @abstractmethod
    async def download(self, security_symbol: SecuritySymbol, currency: str) -> Price:
        """Download price for the given security symbol and currency."""
        pass


class Quote:
    def __init__(self):
        self.symbol: Optional[str] = None
        self.exchange: Optional[str] = None
        self.source: Optional[str] = None
        self.currency: Optional[str] = None

    async def fetch(self, exchange: str, symbols: List[str]) -> List[Price]:
        """Fetch prices for the given symbols."""
        result = []

        for symbol in symbols:
            # logging.debug(f"Downloading price for {symbol}")
            sec_sym = SecuritySymbol(exchange, symbol)

            price = await self.download(sec_sym)
            if price:
                result.append(price)

        return result

    async def download(self, security_symbol: SecuritySymbol) -> Optional[Price]:
        """Download price for the given security symbol."""
        if self.currency is not None:
            currency_val = self.currency
            if currency_val != currency_val.upper():
                raise ValueError("currency must be uppercase!")

        downloader = self.get_downloader()
        currency = self.currency

        logging.debug(
            f"Calling download with symbol {security_symbol} and currency {currency}"
        )

        try:
            price = await downloader.download(security_symbol, currency)
            # Set the symbol here.
            price.symbol = str(security_symbol)
            return price
        except Exception as error:
            raise Exception(f"Error downloading price: {error}")

    def get_downloader(self) -> Downloader:
        """Get the appropriate downloader based on the source."""
        from .quote.fixerio import Fixerio
        from .quote.vanguard_au_2023_detail import VanguardAu3Downloader
        from .quote.yahoo_finance_downloader import YahooFinanceDownloader

        source = self.source.lower() if self.source else None
        
        if source == "yahoo_finance":
            logging.debug("using yahoo finance")
            return YahooFinanceDownloader()
        elif source == "fixerio":
            logging.debug("using fixerio")
            return Fixerio()
        elif source == "vanguard_au":
            logging.debug("using vanguard")
            return VanguardAu3Downloader()
        else:
            raise ValueError(f"unknown downloader: {source}")

    def set_currency(self, currency: str):
        """Set the currency for price fetching."""
        self.currency = currency.upper()

    def set_source(self, source: str):
        """Set the source for price fetching."""
        self.source = source
