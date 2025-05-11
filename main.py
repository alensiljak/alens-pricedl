'''
Main entry point for the script executable.
'''

# todo: setup logging
# todo: setup commands/arguments

import importlib.metadata


def get_version():
    '''Identifies the package version'''

    try:
        version = importlib.metadata.version("pricedb-python")
    except importlib.metadata.PackageNotFoundError:
        version = None
    return version


def main():
    '''
    Entry point for the `pricedb` utility.
    '''
    version = get_version()
    print(f'PriceDb v{version}')

    # load configuration
    # cfg = PriceDbConfig()
    # todo: initialize application
    # todo: handle command
    # pricedb.cli.cli(debug)


if __name__ == '__main__':
    main()
    # pricedb.cli.cli()
