from pycoingecko import CoinGeckoAPI
coin_gecko = CoinGeckoAPI()

def get_cryptocurrencies_last_price():
    coin_gecko = CoinGeckoAPI()
    cryptocurrencies=['bitcoin', 'litecoin', 'ethereum','cardano','bitcoin-cash',
                              'ripple','iota','eos','dash','monero','neo','omisego',
                              'digibyte','dogecoin','steem','ravencoin','polkadot',
                              'chainlink','stellar','binancecoin','uniswap','solana',
                              'ethereum-classic','tron','tezos','nem','zcash']
    cryptocurrencies_last_price=coin_gecko.get_price(ids=cryptocurrencies, vs_currencies='usd')
    return cryptocurrencies_last_price



