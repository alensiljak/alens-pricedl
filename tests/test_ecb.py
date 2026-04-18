"""
ECB Quotes
"""

from pathlib import Path
from alens.pricedl.model import SecuritySymbol
from alens.pricedl.quotes.ecb import EcbDownloader


def test_aud_dl():
    """
    Test downloading AUD exchange rate.
    """
    currency = "AUD"
    dl = EcbDownloader()
    symbol = SecuritySymbol("CURRENCY", currency)
    result = dl.download(symbol, "EUR")

    assert result is not None
    assert result.value > 0
    assert result.value < 3
    assert result.currency == "EUR"
    assert result.symbol.mnemonic == currency
    assert result.symbol.namespace == "CURRENCY"


def test_dl():
    """
    test download
    """
    dl = EcbDownloader()
    symbol = SecuritySymbol("CURRENCY", "GBP")
    result = dl.download(symbol, "EUR")

    assert result is not None
    assert result.value > 0
    assert result.value < 3
    assert result.currency == "EUR"
    assert result.symbol.mnemonic == "GBP"
    assert result.symbol.namespace == "CURRENCY"


def test_temp_dir():
    """
    test temp dir
    """
    dl = EcbDownloader()

    actual = dl.get_cache_path()
    file_path = Path(actual)
    parent_dir = Path(file_path.parent)

    assert parent_dir is not None
    assert parent_dir.exists()
    assert parent_dir.is_dir()
