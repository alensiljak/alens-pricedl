'''
    A flat file for prices.
    Ledger price file.
'''
import csv
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .model import Price


@dataclass
class PriceRecord:
    """
    Record row in the prices file.
    """

    symbol: str
    currency: str
    date: datetime
    value: float
    time: Optional[datetime] = None
    source: str = ""

    @classmethod
    def from_price(cls, price: Price):
        """
        Create a PriceRecord from a Price object.
        """
        return cls(
            symbol=str(price.symbol),
            currency=price.currency,
            date=price.date,
            value=price.value,
            time=price.time,
            source=price.source,
        )


class PriceFlatFile:
    """
    Flat file implementation of the PriceDatabase.
    """
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.prices: Dict[str, PriceRecord] = {}
        self._load()

    def _load(self):
        """Load prices from the flat file."""
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) < 5:
                    continue

                symbol = row[0]
                currency = row[1]
                date_str = row[2]
                time_str = row[3] if row[3] else None
                value = float(row[4])
                source = row[5] if len(row) > 5 else ""

                date = datetime.strptime(date_str, "%Y-%m-%d")
                time = datetime.strptime(time_str, "%H:%M:%S") if time_str else None

                self.prices[symbol] = PriceRecord(
                    symbol=symbol,
                    currency=currency,
                    date=date,
                    time=time,
                    value=value,
                    source=source,
                )

    def save(self):
        """Save prices to the flat file."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Currency", "Date", "Time", "Value", "Source"])

            # Sort by date/time + symbol
            sorted_prices = sorted(
                self.prices.values(),
                key=lambda p: (p.date, p.time or datetime.min, p.symbol),
            )

            for price in sorted_prices:
                writer.writerow(
                    [
                        price.symbol,
                        price.currency,
                        price.date.strftime("%Y-%m-%d"),
                        price.time.strftime("%H:%M:%S") if price.time else "",
                        price.value,
                        price.source,
                    ]
                )

    def add_price(self, price: PriceRecord):
        """Add a price record to the collection."""
        self.prices[price.symbol] = price

    def export_ledger(self, output_path: str):
        """Export prices in Ledger format."""
        with open(output_path, "w", encoding='utf-8') as f:
            # Sort by date/time + symbol
            sorted_prices = sorted(
                self.prices.values(),
                key=lambda p: (p.date, p.time or datetime.min, p.symbol),
            )

            for price in sorted_prices:
                date_str = price.date.strftime("%Y-%m-%d")
                time_str = f" {price.time.strftime('%H:%M:%S')}" if price.time else ""
                f.write(
                    f"P {date_str}{time_str} {price.symbol} {price.value} {price.currency}\n"
                )
