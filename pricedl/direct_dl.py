"""
The price downloader that downloads the prices directly into the list.
"""

from pathlib import Path
from loguru import logger
from pricedl.config import PriceDbConfig
from .model import SecurityFilter


def get_securities(symbols_path: str, filter: SecurityFilter):
    """
    Load symbols list, applying the filters.
    """
    pass


def get_paths():
    """
    Get the paths to the symbols and prices files.
    """
    config = PriceDbConfig()
    symbols_path = Path(config.symbols_path) if config.symbols_path else None
    prices_path = Path(config.prices_path) if config.prices_path else None

    if not symbols_path.exists:
        raise FileNotFoundError(f"Symbols file not found: {symbols_path}")
    if not prices_path.exists:
        raise FileNotFoundError(f"Prices file not found: {prices_path}")

    return symbols_path, prices_path


def dl_quote(security_filter: SecurityFilter):
    """
    Download directly into the price file in ledger format.
    Maintains the latest prices in the price file by updating the prices for
    existing symbols and adding any new ones.
    """
    symbols_path, prices_path = get_paths()
    logger.debug(f"Symbols path: {symbols_path}")
    logger.debug(f"Prices path: {prices_path}")

    # load the symbols table for mapping
    securities = get_securities(symbols_path, security_filter)


def load_symbols(symbols_path: Path):
    """
    Loads the symbols from the symbols file.
    """
