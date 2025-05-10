import aiohttp
import logging
from datetime import datetime
from typing import Optional

from ..model import Price, SecuritySymbol
from . import QuoteProvider


class YahooFinanceDownloader(QuoteProvider):
    async def get_price(self, symbol: SecuritySymbol, currency: str) -> Optional[Price]:
        """Get price from Yahoo Finance."""
        logging.info(f"Downloading price for {symbol} from Yahoo Finance")
        
        # Yahoo Finance uses different format
        yahoo_symbol = symbol.mnemonic
        
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logging.error(f"Failed to get price: {response.status}")
                    return None
                
                data = await response.json()
                
                try:
                    result = data["chart"]["result"][0]
                    quote = result["indicators"]["quote"][0]
                    
                    # Get the latest price
                    close_prices = quote.get("close", [])
                    if not close_prices or close_prices[-1] is None:
                        return None
                    
                    price_value = close_prices[-1]
                    timestamp = result["timestamp"][-1]
                    
                    # Convert timestamp to datetime
                    dt = datetime.fromtimestamp(timestamp)
                    
                    return Price(
                        symbol=symbol,
                        currency=currency,
                        date=dt.date(),
                        time=dt,
                        value=price_value,
                        source="Yahoo Finance"
                    )
                except (KeyError, IndexError) as e:
                    logging.error(f"Error parsing Yahoo Finance response: {e}")
                    return None
