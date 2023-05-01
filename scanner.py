import api
from discord.ext import commands
from web3 import Web3
import asyncio
import keys
import ca
import main

client = main.PersitentViewBot()

infura_url = f'https://mainnet.infura.io/v3/{keys.infura}'
web3 = Web3(Web3.HTTPProvider(infura_url))

factory = web3.eth.contract(address=ca.uniswap, abi=api.get_abi(ca.uniswap))
ill001 = web3.eth.contract(address=ca.ill001, abi=api.get_abi(ca.ill001))
ill002 = web3.eth.contract(address=ca.ill002, abi=api.get_abi(ca.ill002))
ill003 = web3.eth.contract(address=ca.ill003, abi=api.get_abi(ca.ill003))

async def new_loan(event):
    await application.bot.send_photo(
        "-1001780235511",
        photo=open('media/logo10.png', 'rb'),
        caption=f'*New Loan Originated*\n\n{event["loanID"]}\n\n'
                f'https://etherscan.io/tx/{event["transactionHash"].hex()}', parse_mode='Markdown')

async def new_pair(event):
    name_token0 = api.get_token_name(event["args"]["token0"])
    name_token1 = api.get_token_name(event["args"]["token1"])
    await application.bot.send_photo(
        "-1001780235511",
        photo=open('media/logo10.png', 'rb'),
        caption=f'*New Pair Created*\n\n{event["args"]["pair"]}\n\n'
                f'Token 0: {name_token0} ({name_token0[1]})\n'
                f'Token 1: {name_token1} ({name_token1[1]})\n\n'
                f'https://etherscan.io/tx/{event["transactionHash"].hex()}', parse_mode='Markdown')

async def log_loop(pair_filter, ill001_filter, ill002_filter, ill003_filter, poll_interval):
    while True:
        for PairCreated in pair_filter.get_new_entries():
            await new_pair(PairCreated)
        await asyncio.sleep(poll_interval)
        for LoanOriginated in \
                ill001_filter.get_new_entries() or ill002_filter.get_new_entries() or ill003_filter.get_new_entries():
            await new_loan(LoanOriginated)
        await asyncio.sleep(poll_interval)


def main():
    print("Scanning X7 Finance ecosystem")
    pair_filter = factory.events.PairCreated.create_filter(fromBlock='latest')
    ill001_filter = ill001.events.LoanOriginated.create_filter(fromBlock='latest')
    ill002_filter = ill002.events.LoanOriginated.create_filter(fromBlock='latest')
    ill003_filter = ill003.events.LoanOriginated.create_filter(fromBlock='latest')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(asyncio.gather(log_loop(pair_filter, ill001_filter, ill002_filter, ill003_filter, 2)))
    finally:
        loop.close()

    main.client.run(keys.DISCORD_TOKEN)
if __name__ == "__main__":
    asyncio.run(main())



