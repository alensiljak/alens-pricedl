from abc import ABC, abstractmethod
from typing import List, Optional
import asyncio
import logging
from datetime import datetime

from .model import Price, SecuritySymbol


class QuoteProvider(ABC):
    @abstractmethod
    async def get_price(self, symbol: SecuritySymbol, currency: str) -> Optional[Price]:
        pass


async def get_quote(symbol: str, currency: str, provider: str = "") -> Optional[Price]:
    """Get a price quote for the given symbol."""
    from pricedb.quotes.fixerio import Fixerio
    from pricedb.quotes.vanguard_au_2023_detail import VanguardAu3Downloader
    from pricedb.quotes.yahoo_finance_downloader import YahooFinanceDownloader
    
    logging.debug(f"Getting quote for {symbol} in {currency} using {provider}")
    
    security_symbol = SecuritySymbol.from_string(symbol)
    
    # Select provider based on input or symbol namespace
    if provider:
        provider_name = provider.lower()
    else:
        provider_name = security_symbol.namespace.lower()
    
    # Map provider name to provider class
    providers = {
        "fixerio": Fixerio(),
        "vanguard_au": VanguardAu3Downloader(),
        "yahoo": YahooFinanceDownloader(),
    }
    
    quote_provider = providers.get(provider_name)
    if not quote_provider:
        logging.error(f"No provider found for {provider_name}")
        return None
    
    try:
        price = await quote_provider.get_price(security_symbol, currency)
        return price
    except Exception as e:
        logging.error(f"Error fetching price: {e}")
        return None
