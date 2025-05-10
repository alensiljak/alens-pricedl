import asyncio
import click
from loguru import logger
import os
from datetime import datetime
from typing import List, Optional

from .config import PriceDbConfig
from .model import SecuritySymbol
from .price_flat_file import PriceFlatFile, PriceRecord
# from .quotes import get_quote


@click.group()
@click.option("--debug/--no-debug", default=False, help="Enable debug logging")
def cli(debug):
    """PriceDB - Retrieve, store, and export commodity prices in Ledger format."""
    # level = logging.DEBUG if debug else logging.INFO
    # logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    cfg = PriceDbConfig()
    logger.debug(f"Config file: {cfg.config_path}")


# @cli.group()
def config_cmd():
    """Configuration commands."""
    pass


# @config_cmd.command("show")
def config_show():
    """Show current configuration."""
    config = PriceDbConfig()
    click.echo(f"Configuration file: {config.config_path}")
    click.echo(f"Prices path: {config.prices_path}")
    
    # Show all config values
    for key, value in config.config_data.items():
        click.echo(f"{key}: {value}")


# @config_cmd.command("set")
# @click.argument("key")
# @click.argument("value")
# def config_set(key, value):
#     """Set a configuration value."""
#     config = PriceDbConfig()
#     config.set_value(key, value)
#     click.echo(f"Set {key} to {value}")


@cli.command("dl")
@click.option("--symbol", "-s", help="Symbol to download (NAMESPACE:MNEMONIC)")
@click.option("--currency", "-c", help="Currency for the price")
@click.option("--provider", "-p", help="Provider to use for download")
@click.option("--file", "-f", help="Path to CSV file with symbols")
async def download(symbol, currency, provider, file):
    """Download prices for symbols."""
    config = PriceDbConfig()

    # If no file or symbol provided, check config
    if not symbol and not file:
        symbol = config.get_value("symbol")
        file = config.get_value("symbols_file")

        if not symbol and not file:
            click.echo()
