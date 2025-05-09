'''
Main entry point for the script executable.
'''

# todo: setup logging
# todo: setup commands/arguments

import importlib.metadata

import click

import pricedb
import pricedb.cli
from pricedb.config import PriceDbConfig


def download_quotes():
    '''
    dl command
    '''
    pass

def get_version():
    '''Identifies the package version'''

    try:
        version = importlib.metadata.version("pricedb-python")
    except importlib.metadata.PackageNotFoundError:
        version = None
    return version

def show_config():
    '''
    `config` command
    '''
    pass


@click.command()
@click.option("--debug/--no-debug", default=False, help="Enable debug logging")
def main(debug):
    '''
    Entry point for the `pricedb` utility.
    '''
    version = get_version()
    print(f'PriceDb v{version}')
    print(debug)

    # load configuration
    # cfg = PriceDbConfig()
    # todo: initialize application
    # todo: handle command
    # pricedb.cli.cli(debug)


if __name__ == '__main__':
    # main()
    pricedb.cli.cli()
