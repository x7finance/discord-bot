from pycoingecko import CoinGeckoAPI
from moralis import evm_api
import keys
import items

# CG
cg = CoinGeckoAPI()
price = cg.get_price(ids=',x7r,x7dao,x7101,x7102,x7103,x7104,x7105', vs_currencies='usd',
                     include_24hr_change='true', include_24hr_vol='true')
# MORALIS LIQ
# noinspection PyTypeChecker
x7rliq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                        params={"chain": "eth", "pair_address": items.x7rpaireth})
# noinspection PyTypeChecker
x7daoliq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7daopaireth})
# noinspection PyTypeChecker
x7101liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7101paireth})
# noinspection PyTypeChecker
x7102liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7102paireth})
# noinspection PyTypeChecker
x7103liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7103paireth})
# noinspection PyTypeChecker
x7104liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7104paireth})
# noinspection PyTypeChecker
x7105liq = evm_api.defi.get_pair_reserves(api_key=keys.moralis,
                                          params={"chain": "eth", "pair_address": items.x7105paireth})


# ETH
ethprice = 'https://api.etherscan.io/api?module=stats&action=ethprice&'
tokenbalanceeth = 'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
ethbalanceeth = 'https://api.etherscan.io/api?module=account&action=balancemulti&address='
ethgas = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle'

# BSC
bnbprice = 'https://api.bscscan.com/api?module=stats&action=bnbprice&'
tokenbalancebsc = 'https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress='
bnbbalance = 'https://api.bscscan.com/api?module=account&action=balancemulti&address='
bscgas = 'https://api.bscscan.com/api?module=gastracker&action=gasoracle'

# POLY
maticprice = 'https://api.polygonscan.com/api?module=stats&action=maticprice&'
tokenbalancepoly = 'https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress='
maticbalance = 'https://api.polygonscan.com/api?module=account&action=balancemulti&address='
polygas = 'https://api.polygonscan.com/api?module=gastracker&action=gasoracle'

# ARB
tokenbalancearb = 'https://api.arbiscan.io/api?module=account&action=tokenbalance&contractaddress='
ethbalancearb = 'https://api.arbiscan.io/api?module=account&action=balancemulti&address='

# OPTI
tokenbalanceopti = 'https://api-optimistic.etherscan.io/api?module=account&action=tokenbalance&contractaddress='
ethbalanceopti = 'https://api-optimistic.etherscan.io/api?module=account&action=balancemulti&address='

blockspan = 'https://api.blockspan.com/v1/collections/contract/'
ethplorer = 'https://api.ethplorer.io/getTokenInfo/'
os = "https://api.opensea.io/api/v1/collection/"
quote = 'https://type.fit/api/quotes'
fear = 'https://api.alternative.me/fng/?limit=0'
today = 'http://history.muffinlabs.com/date/'
joke = 'https://v2.jokeapi.dev/joke/Any?safe-mode'
