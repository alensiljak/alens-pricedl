"""
Test price file handling
"""

from decimal import Decimal
from pathlib import Path

from pricedl.price_flat_file import PriceFlatFile


def test_reading():
    """
    Test reading a price file
    """
    file_path = Path("tests/prices.txt")
    price_file = PriceFlatFile.load(file_path)

    assert len(price_file.prices) == 4
    assert price_file.prices["VEUR_AS"].value == Decimal("1.5")
    assert price_file.prices["VEUR_AS"].currency == "EUR"
    assert price_file.prices["VEUR_AS"].datetime.strftime("%Y-%m-%d") == "2023-04-15"
    assert price_file.prices["VEUR_AS"].datetime.strftime("%H:%M:%S") == "12:00:00"
    assert price_file.prices["VEUR_AS"].symbol == "VEUR_AS"
