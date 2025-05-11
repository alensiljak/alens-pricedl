from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from decimal import Decimal, InvalidOperation


@dataclass
class SecurityFilter:
    '''
    CLI filter for the securities for which to download the prices
    '''
    currency: None
    agent: None
    exchange: None
    symbol: None


@dataclass
class SecuritySymbol:
    '''
    Security symbol, containing the exchange.
    '''
    namespace: str
    mnemonic: str

    def __str__(self):
        return f"{self.namespace}:{self.mnemonic}"

    @classmethod
    def from_str(cls, symbol_str: str):
        '''
        Create a SecuritySymbol from a str. i.e. "NASDAQ:OPI"
        '''
        parts = symbol_str.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid symbol format: {symbol_str}")
        return cls(parts[0], parts[1])


@dataclass
class Price:
    '''
    The downloaded price for a security
    '''
    symbol: SecuritySymbol
    date: datetime
    time: Optional[datetime] = None
    value: float
    currency: str
    source: str = ""
    value_int_part: int  # The integer part of the value (mantissa)
    denom_as_scale: int  # The scale (number of decimal places)

    def to_decimal(self) -> Decimal:
        """
        Converts the raw integer value and scale into a Decimal.
        This mimics rust_decimal::Decimal::new(value, scale).
        """
        s_val = str(self.value_int_part)
        sign = 0
        if self.value_int_part < 0:
            sign = 1
            s_val = s_val[1:]

        digits = tuple(map(int, list(s_val)))

        # In Python's Decimal, exponent is the negative of scale.
        exponent = -self.denom_as_scale

        return Decimal((sign, digits, exponent))


@dataclass
class SymbolMetadata:
    '''
    Symbol row in the symbols.csv file.
    '''
    # Exchange
    namespace: Optional[str]
    # Symbol at the exchange
    symbol: str
    # The currency used to express the symbol's price.
    currency: Optional[str]
    # The name of the price update provider.
    updater: Optional[str]
    # The symbol, as used by the updater.
    updater_symbol: Optional[str]
    # The symbol, as used in the Ledger journal.
    ledger_symbol: Optional[str]
    # The symbol, as used at Interactive Brokers.
    ib_symbol: Optional[str]
    # Remarks
    remarks: Optional[str]
