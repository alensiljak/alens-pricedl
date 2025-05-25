"""
Bean-price-compatible price downloader for Vanguard Australia.

Use:

    uv run bean-price -e "AUD:vanguard_au:HY"
"""

import asyncio
from datetime import datetime
from decimal import Decimal
import re
from typing import Any

from beanprice import source
from loguru import logger
# from pricehist import beanprice
# from pricedl import beanprice

# from pricehist.sources.yahoo import Yahoo
from pricedl.model import SecuritySymbol
from pricedl.quotes.vanguard_au_2023_detail import VanguardAu3Downloader

# Source = beanprice.source(Yahoo())
# Source = beanprice.source(VanguardAu3Downloader())


def _parse_ticker(ticker):
    """Parse the base and quote currencies from the ticker.

    Args:
      ticker: A string, the symbol in XXX-YYY format.
    Returns:
      A pair of (base, quote) currencies.
    """
    match = re.match(r"^(?P<base>\w+):(?P<symbol>\w+)$", ticker)
    if not match:
        raise ValueError('Invalid ticker. Use "BASE-SYMBOL" format.')
    return match.groups()


class Source(source.Source):
    '''
    Vanguard Australia price source
    ticker: VANGUARD:HY
    '''
    def get_latest_price(self, ticker) -> source.SourcePrice | None:
        try:
            base, symbol = _parse_ticker(ticker)

            sec_symbol = SecuritySymbol("VANGUARD", symbol)
            v_price = asyncio.run(VanguardAu3Downloader().download(sec_symbol, base))

            price = v_price.value

            min_time = datetime.min.time()
            time = datetime.combine(v_price.date, min_time)
            # The datetime must be timezone aware.
            time = time.astimezone()

            quote_currency = v_price.currency

            return source.SourcePrice(price, time, quote_currency)
        except Exception as e:
            logger.error(e)
            return None

    def get_historical_price(self, ticker, time):
        # return VanguardAu3Downloader().get_historical_price(ticker, time)
        pass
