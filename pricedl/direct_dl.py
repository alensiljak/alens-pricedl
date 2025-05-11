"""
The price downloader that downloads the prices directly into the list.
"""

from pathlib import Path
from typing import Tuple
import csv
from loguru import logger
from pricedl.config import PriceDbConfig
from .model import SecurityFilter, SymbolMetadata


def get_securities(symbols_path: Path, filter: SecurityFilter):
    """
    Load symbols list, applying the filters.
    """
    symbols_list = load_symbols(symbols_path)
    logger.debug(f"Loaded {len(symbols_list)} symbols from {symbols_path}")


def get_paths() -> Tuple[Path, Path]:
    """
    Get the paths to the symbols and prices files.
    """
    config = PriceDbConfig()

    if config.symbols_path is None:
        raise ValueError("Symbols path not set in config")
    if config.prices_path is None:
        raise ValueError("Prices path not set in config")

    symbols_path = Path(config.symbols_path)
    prices_path = Path(config.prices_path)

    if not symbols_path.exists():
        raise FileNotFoundError(f"Symbols file not found: {symbols_path}")
    if not prices_path.exists():
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
    # symbols_list = []

    with open(symbols_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        symbols_list = [SymbolMetadata(**row) for row in reader]
        # for row in reader:
        #     symbols_list.append(row)

    logger.debug(f"Loaded {len(symbols_list)} symbols from {symbols_path}")
    return symbols_list
