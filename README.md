# pricedb-python
Price-database utility converted to Python

This is a rewrite of Pricedb-Rust utility. Pricedb-Rust originally came from Price-Database, which was in Python and was storing the prices in a SQLite database.
In later versions of Price-Database, the database was replaced with an in-memory store, outputting the final result into a Ledger prices text file.
In this project, the idea remains to fetch the prices, sort them by time, and output them into a Ledger prices text file.
