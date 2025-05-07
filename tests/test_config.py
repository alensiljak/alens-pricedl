'''
Test configuration
'''
import pricedb
import pricedb.config

def test_config():
    '''
    Test if the configuration can be instantiated.
    '''
    cfg = pricedb.config.PriceDbConfig()

    assert cfg.prices_path is not None
