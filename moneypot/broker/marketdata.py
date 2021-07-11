import moneypot
import pandas as pd

def get_all_coins_by_marketcap_coinmarketcap():
    """ Load a list of all coins by marketcap from coinmarketcap
    """
    import coinmarketcapapi
    api_key = moneypot.config['coinmarketcap']['API_KEY']
    cmc = coinmarketcapapi.CoinMarketCapAPI(api_key)


    # Get all coins
    cmap = cmc.cryptocurrency_map()
    cmap = pd.DataFrame(cmap.data).sort_values(by='rank', ascending=True)

    cmap['first_historical_data'] = pd.to_datetime(cmap['first_historical_data'])
    cmap['last_historical_data'] = pd.to_datetime(cmap['last_historical_data'])

    return cmap
