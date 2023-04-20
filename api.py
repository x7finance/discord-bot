from pycoingecko import CoinGeckoAPI
from moralis import evm_api
import keys
import requests
import random
from datetime import datetime
import nfts


def get_signers(wallet):
    url = f'https://safe-transaction-mainnet.safe.global/api/v1/safes/{wallet}/'
    response = requests.get(url)
    result = response.json()
    return result

def get_cg_search(token):
    url = 'https://api.coingecko.com/api/v3/search?query=' + token
    response = requests.get(url)
    result = response.json()
    return result

def get_cg_price(token):
    coingecko = CoinGeckoAPI()
    cg = coingecko.get_price(ids=token, vs_currencies='usd',
                             include_24hr_change='true', include_24hr_vol='true')
    return cg

# noinspection PyTypeChecker
def get_nft_holder_list(nft, chain):
    result = evm_api.nft.get_nft_owners(
        api_key=keys.moralis, params={"chain": chain, "format": "decimal", "address": nft})
    return result

# noinspection PyTypeChecker
def get_liquidity(pair):
    amount = evm_api.defi.get_pair_reserves(api_key=keys.moralis, params={"chain": "eth", "pair_address": pair})
    return amount

def get_tx(address, chain):
    result = evm_api.transaction.get_wallet_transactions(
        api_key=keys.moralis, params={"address": address, "chain": chain})
    return result

def get_today():
    current_day = str(datetime.now().day)
    current_month = str(datetime.now().month)
    url = f'http://history.muffinlabs.com/date/{current_month}/{current_day}'
    response = requests.get(url)
    data = response.json()
    return data

def get_os_nft(slug):
    slug = slug
    headers = {"X-API-KEY": keys.os}
    url = "https://api.opensea.io/api/v1/collection/" + slug
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def get_gas(chain):
    if chain == "eth":
        url = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle' + keys.ether
        response = requests.get(url)
        data = response.json()
        return data
    if chain == "poly":
        url = 'https://api.polygonscan.com/api?module=gastracker&action=gasoracle' + keys.poly
        response = requests.get(url)
        data = response.json()
        return data
    if chain == "bsc":
        url = 'https://api.bscscan.com/api?module=gastracker&action=gasoracle' + keys.bsc
        response = requests.get(url)
        data = response.json()
        return data

def get_holders(token):
    url = 'https://api.ethplorer.io/getTokenInfo/' + token + keys.ethplorer
    response = requests.get(url)
    data = response.json()
    amount = data["holdersCount"]
    return amount

def get_ath(token):
    url = f"https://api.coingecko.com/api/v3/coins/{token}?localization=false&tickers=false&market_data=" \
          "true&community_data=false&developer_data=false&sparkline=false"
    response = requests.get(url)
    data = response.json()
    value = data["market_data"]
    ath = value["ath"]["usd"]
    return ath


def get_ath_change(token):
    url = f"https://api.coingecko.com/api/v3/coins/{token}?localization=false&tickers=false&market_data=" \
          "true&community_data=false&developer_data=false&sparkline=false"
    response = requests.get(url)
    data = response.json()
    value = data["market_data"]
    change = value["ath_change_percentage"]["usd"]
    return change

def get_ath_date(token):
    url = f"https://api.coingecko.com/api/v3/coins/{token}?localization=false&tickers=false&market_data=" \
          "true&community_data=false&developer_data=false&sparkline=false"
    response = requests.get(url)
    data = response.json()
    value = data["market_data"]
    date = value["ath_date"]["usd"]
    return date

def get_quote():
    response = requests.get('https://type.fit/api/quotes')
    data = response.json()
    quote_raw = (random.choice(data))
    quote = quote_raw["text"] + quote_raw["author"]
    quote = f'`"{quote_raw["text"]}"\n\n-{quote_raw["author"]}`'
    return quote

def get_nft_holder_count(nft, chain):
    url = 'https://api.blockspan.com/v1/collections/contract/' + nft + chain
    response = requests.get(url, headers={"accept": "application/json", "X-API-KEY": keys.blockspan})
    data = response.json()
    amount = data["total_tokens"]
    return amount

def get_nft_price(nft, chain):
    if chain == "eth":
        return nfts.eco_price_eth, nfts.liq_price_eth, nfts.borrow_price_eth, nfts.dex_price_eth, \
            nfts.magister_price_eth
    if chain == "bsc":
        return nfts.eco_price_bsc, nfts.liq_price_bsc, nfts.borrow_price_bsc, nfts.dex_price_bsc, \
            nfts.magister_price_bsc
    if chain == "poly":
        return nfts.eco_price_poly, nfts.liq_price_poly, nfts.borrow_price_poly, nfts.dex_price_poly, \
            nfts.magister_price_poly
    if chain == "opti":
        return nfts.eco_price_opti, nfts.liq_price_opti, nfts.borrow_price_opti, nfts.dex_price_opti, \
            nfts.magister_price_opti
    if chain == "arb":
        return nfts.eco_price_arb, nfts.liq_price_arb, nfts.borrow_price_arb, nfts.dex_price_arb, \
            nfts.magister_price_arb

def get_token_balance(wallet, chain, token):
    if chain == "eth":
        url = 'https://api.etherscan.io/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.ether
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "bsc":
        url = 'https://api.bscscan.com/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.bsc
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "opti":
        url = 'https://api-optimistic.etherscan.io/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.opti
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "poly":
        url = 'https://api.polygonscan.com/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.poly
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount
    if chain == "arb":
        url = 'https://api.arbiscan.io/' \
              'api?module=account&action=tokenbalance&contractaddress='
        key = keys.arb
        response = requests.get(url + token + '&address=' + wallet + '&tag=latest' + key)
        data = response.json()
        amount = int(data["result"][:-18])
        return amount

def get_native_balance(wallet, chain):
    if chain == "opti":
        key = keys.opti
        link = 'https://api-optimistic.etherscan.io/' \
               'api?module=account&action=balancemulti&address='
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount
    if chain == "eth":
        key = keys.ether
        link = 'https://api.etherscan.io/' \
               'api?module=account&action=balancemulti&address='
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount
    if chain == "arb":
        key = keys.arb
        link = 'https://api.arbiscan.io/' \
               'api?module=account&action=balancemulti&address='
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount
    if chain == "bsc":
        key = keys.bsc
        link = "https://api.bscscan.com/" \
               "api?module=account&action=balancemulti&address="
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount
    if chain == "poly":
        key = keys.poly
        link = "https://api.polygonscan.com/" \
               "api?module=account&action=balancemulti&address="
        response = requests.get(link + wallet + '&tag=latest' + key)
        data = response.json()
        amount_raw = float(data["result"][0]["balance"])
        amount = str(amount_raw / 10 ** 18)
        return amount

def get_native_price(token):
    if token == "eth":
        url = 'https://api.etherscan.io/api?module=stats&action=ethprice&' + keys.ether
        response = requests.get(url)
        data = response.json()
        value = float(data["result"]["ethusd"])
        return value
    if token == "bnb":
        url = 'https://api.bscscan.com/api?module=stats&action=bnbprice&' + keys.bsc
        response = requests.get(url)
        data = response.json()
        value = float(data["result"]["ethusd"])
        return value
    if token == "matic":
        url = 'https://api.polygonscan.com/api?module=stats&action=maticprice&' + keys.poly
        response = requests.get(url)
        data = response.json()
        value = float(data["result"]["maticusd"])
        return value
