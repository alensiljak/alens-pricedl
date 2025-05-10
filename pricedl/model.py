from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class SecuritySymbol:
    namespace: str
    mnemonic: str

    def __str__(self):
        return f"{self.namespace}:{self.mnemonic}"

    @classmethod
    def from_string(cls, symbol_str: str):
        parts = symbol_str.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid symbol format: {symbol_str}")
        return cls(parts[0], parts[1])


@dataclass
class Price:
    symbol: SecuritySymbol
    currency: str
    date: datetime
    value: float
    time: Optional[datetime] = None
    source: str = ""
