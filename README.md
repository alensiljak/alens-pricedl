# pricedb-python
Price-database utility converted to Python

This is a rewrite of Pricedb-Rust utility. Pricedb-Rust originally came from Price-Database, which was in Python and was storing the prices in a SQLite database.
In later versions of Price-Database, the database was replaced with an in-memory store, outputting the final result into a Ledger prices text file.
In this project, the idea remains to fetch the prices, sort them by time, and output them into a Ledger prices text file.

# Install
```sh
uv tool install pricedb-python
```

# Run
Example configuration file (.config/pricedb/pricedb.toml):
```
price_database_path = ":memory:"
alphavantage_api_key = ""
fixerio_api_key = "<KEY>"
prices_path = "/home/prices.txt"
symbols_path = "/home/symbols.csv"
```


# Development
```sh
uv run python main.py [dl]
```
