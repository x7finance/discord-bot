import discord
from discord.ext import commands
import tweepy
import items
import keys
import requests
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
from discord import *
from typing import *
import random
import variables


class PersitentViewBot(commands.Bot):
    def __init__(self):
        self.role = 1016664143220179077
        intents = discord.Intents().all()
        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(Button())


client = PersitentViewBot()

embed = discord.Embed(colour=7419530)
embed.set_footer(text="Trust no one, Trust code. Long live Defi")
thumb = discord.File('X7whitelogo.png')
embed.set_thumbnail(url='attachment://X7whitelogo.png')


class Button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Agree", emoji="<:x7:1023271910647271584>", style=discord.ButtonStyle.blurple,
                       custom_id="1")
    async def agree(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if type(client.role) is not discord.Role:
            client.role = interaction.guild.get_role(1016657044553617428)
        if client.role not in interaction.user.roles:
            await interaction.user.add_roles(client.role)
            await interaction.response.send_message("You are now verified!", ephemeral=True)
        else:
            await interaction.response.send_message("You are already verified!", ephemeral=True)


@client.tree.command(description="Agree to server rules")
@commands.has_any_role("Moderators")
async def agree_button(interaction: discord.Interaction):
    await interaction.response.send_message(content="Once you have read and understood the rules, Hit agree to "
                                                    "continue",
                                            view=Button())


@client.event
async def on_ready():
    print('Bot is ready')
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


@client.event
async def on_member_join(member):
    guild = client.get_guild(1016657044553617428)
    dao = guild.get_role(1017420479159607367)
    for channel in member.guild.channels:
        if channel.name.startswith('Members'):
            await channel.edit(name=f'Members: {member.guild.member_count}')
        if channel.name.startswith('DAO Members'):
            await channel.edit(name=f'DAO Members: {len(dao.members)}')


@client.event
async def on_member_leave(member):
    guild = client.get_guild(1016657044553617428)
    dao = guild.get_role(1017420479159607367)
    for channel in member.guild.channels:
        if channel.name.startswith('Members'):
            await channel.edit(name=f'Members: {member.guild.member_count}')

        if channel.name.startswith('DAO Members'):
            await channel.edit(name=f'DAO Members: {len(dao.members)}')


# COMMANDS
@client.tree.command(description="List all bot commands")
async def filters(interaction: discord.Interaction):
    embed.description = f'{variables.commands}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance server rules")
@app_commands.choices(rule_number=[
    app_commands.Choice(name="Full list", value="all"),
    app_commands.Choice(name="1. Discord TOS", value="tos"),
    app_commands.Choice(name="2. Be respectful with all members", value="respect"),
    app_commands.Choice(name="3. No advertising", value="advertising"),
    app_commands.Choice(name="4. No NSFW content", value="nsfw"),
    app_commands.Choice(name="5. No spamming in text or VC", value="spam"),
    app_commands.Choice(name="6. Be mindful of sensitive topics", value="topics"),
    app_commands.Choice(name="7. No malicious content", value="malicious"),
    app_commands.Choice(name="8. No Self Bots", value="bot"),
    app_commands.Choice(name="9. Do not DM the staff team", value="dm"),
    app_commands.Choice(name="10. Media and emoji usage", value="media"),
    ])
async def rules(interaction: discord.Interaction, rule_number: app_commands.Choice[str]):
    if rule_number.value == 'tos':
        embed.description = "**1. Follow discord TOS**\n\nhttps://discordapp.com/terms\n" \
                            "https://discordapp.com/guidelines"
    if rule_number.value == 'respect':
        embed.description = "> **2. Be respectful with all members**\n\n" \
                            "Be respectful to others , No death threats, sexism, hate speech, racism (NO N WORD, " \
                            "this includes soft N)\nNo doxxing, swatting, witch hunting"
    if rule_number.value == 'advertising':
        embed.description = "> **3. No advertising**\n\n" \
                            "This includes DM Advertising. We do not allow advertising here of any kind, this " \
                            "includes shilling or promoting your own services."
    if rule_number.value == 'nsfw':
        embed.description = "> **4. No NSFW content**\n\n" \
                            "Anything involving gore or sexual content is not allowed.\nNSFW = Not Safe for Work"
    if rule_number.value == 'spam':
        embed.description = "> **5. No spamming in text or VC**\n\n" \
                            "Do not spam messages, soundboards, voice changers in any channel."
    if rule_number.value == 'topics':
        embed.description = "> **6. Be mindful of sensitive topics**\n\n" \
                            "This isn\'t a debating server, be mindful of topics discussed in public"

    if rule_number.value == 'malicious':
        embed.description = "> **7. No malicious content**\n\n" \
                            "No grabify links, viruses, crash videos, links to viruses, or token grabbers." \
                            " These will result in an automated ban."
    if rule_number.value == 'bot':
        embed.description = "> **8. No self bots**\n\n" \
                            "This includes all kinds of selfbots: Nitro snipers, selfbots like " \
                            "nighty, auto changing statuses"
    if rule_number.value == 'dm':
        embed.description = "> **9. Do not DM the staff team **\n\n" \
                            "If you need assistance, please instead tag <@&1016659542303580221>. Staff members will " \
                            "never DM first unless explicitly saying in chat, always check who you are talking to"
    if rule_number.value == 'media':
        embed.description = "> **10. Media and emoji usage**\n\n" \
                            "No NSFW allowed\n" \
                            "No racism"
    if rule_number.value == 'all':
        embed.description = '**X7 Finance server rules:**\n\n' \
                            'By becoming a <@&1016664143220179077> member of the community. ' \
                            'You are agreeing to the following rules\n\n' \
                            '> **1. Follow Discord\'s TOS**\nhttps://discordapp.com/terms\nhttps://discor' \
                            'dapp.com/guidelines\n\n> **2. Be respectful with all members**\n' \
                            'Be respectful to others , No death threats, sexism, hate speech, racism (NO N WORD,' \
                            'this includes soft N)\nNo doxxing, swatting, witch hunting\n\n> **3. No Advertising**\n' \
                            'This includes DM Advertising. We do not allow advertising here of any kind, this ' \
                            'includes shilling or promoting your own services.\n\n' \
                            '> **4. No NSFW content**\nAnything involving gore or sexual content is not allowed.\n' \
                            'NSFW = Not Safe for Work\n\n' \
                            '> **5. No spamming in text or VC**\n' \
                            'Do not spam messages, soundboards, voice changers in any channel.\n\n' \
                            '> **6. Be mindful of sensitive topics**\n' \
                            'This isn\'t a debating server, be mindful of topics discussed in public\n\n' \
                            '> **7. No malicious content**\n' \
                            'No grabify links, viruses, crash videos, links to viruses, or token grabbers. These' \
                            ' will result in an automated ban.\n\n' \
                            '> **8. No Self Bots**\n' \
                            'This includes all kinds of selfbots: Nitro snipers, selfbots like nighty, auto changing ' \
                            'statuses\n\n' \
                            '> **9. Do not DM the staff team **\n' \
                            'If you need assistance, please instead tag <@&1016659542303580221>. Staff members will ' \
                            'never DM first unless explicitly saying in chat, always check who you are talking to\n\n' \
                            '> **10. Media and emoji usage**\n' \
                            'No NSFW allowed\nNo racism\n\n' \
                            '> Violating these rules will result in being muted as a warning, either automatically ' \
                            'by <@470723870270160917> or by the <@&1016659542303580221> Continued violations could' \
                            ' result in being banned from the server.\n\n' \
                            '> Be aware that list is not exclusive, you may be warned for something not listed here, ' \
                            'as per the <@&1016659542303580221> discretion, please use your common sense.\n\n' \
                            '> Anyone banned will have the right to appeal via our appeal system.\n\n' \
                            '> If you see something against the rules, please report to the <@&1016659542303580221> ' \
                            'using; ```/report @user reason```We want this server to be a welcoming space for ' \
                            'everyone!\n\n' \
                            '> Please remember to work within your means, Trade at your own risk, none of the ' \
                            'information here is financial advice, The <@&1016659542303580221> nor any other ' \
                            'community members will be held accountable for any loses you may incur.\n\n' \
                            '> Don\'t forget to claim your roles at <#1017417972920369164>\n\n' \
                            '> We have <@1018221723650379936> on the server for your benefit, use following ' \
                            'to familiarise yourself ```/bot```'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 NFT info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def nft(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if chain.value == "eth":
        embed.description = \
            f'**X7 Finance NFT Information (ETH)**\n\n' \
            f'[**Ecosystem Maxi**]({items.ethertoken}{items.ecoca})\n{items.ecopriceeth}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.ethertoken}{items.liqca})\n{items.liqpriceeth}\n' \
            f'> 50 % discount on x7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.ethertoken}{items.dexca})\n{items.dexpriceeth}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.ethertoken}{items.borrowca})\n{items.borrowpriceeth}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.ethertoken}{items.magisterca})\n{items.magisterpriceeth}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'[**Pioneer**]({items.ethertoken}{items.pioneerca})\n' \
            f' > 6% of profits that come into the X7 Treasury Splitter are now being allocated to the reward ' \
            f'pool. Each X7 Pioneer NFT grants you a proportional share of this pool\n\n' \
            f'https://x7.finance/x/nft/mint\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        embed.description = \
            f'**X7 Finance NFT Information (BSC)**\n\n' \
            f'[**Ecosystem Maxi**]({items.bsctoken}{items.ecoca})\n{items.ecopricebsc}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.bsctoken}{items.liqca})\n{items.liqpricebsc}\n' \
            f'> 50 % discount on x7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.bsctoken}{items.dexca})\n{items.dexpricebsc}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.bsctoken}{items.borrowca})\n{items.borrowpricebsc}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.bsctoken}{items.magisterca})\n{items.magisterpricebsc}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://x7.finance/x/nft/mint\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        embed.description = \
            f'**X7 Finance NFT Information (POLYGON)**\n\n' \
            f'[**Ecosystem Maxi**]({items.polytoken}{items.ecoca})\n{items.ecopricepoly}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.polytoken}{items.liqca})\n{items.liqpricepoly}\n' \
            f'> 50 % discount on x7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.polytoken}{items.dexca})\n{items.dexpricepoly}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.polytoken}{items.borrowca})\n{items.borrowpricepoly}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.polytoken}{items.magisterca})\n{items.magisterpricepoly}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://x7.finance/x/nft/mint\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        embed.description = \
            f'**X7 Finance NFT Information (ARBITRUM)**\n\n' \
            f'[**Ecosystem Maxi**]({items.arbtoken}{items.ecoca})\n{items.ecopricearb}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.arbtoken}{items.liqca})\n{items.liqpricearb}\n' \
            f'> 50 % discount on x7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.arbtoken}{items.dexca})\n{items.dexpricearb}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.arbtoken}{items.borrowca})\n{items.borrowpricearb}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.arbtoken}{items.magisterca})\n{items.magisterpricearb}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://x7.finance/x/nft/mint\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
        if chain.value == "opti":
            embed.description = \
                f'**X7 Finance NFT Information (OPTIMUM)**\n\n' \
                f'[**Ecosystem Maxi**]({items.optitoken}{items.ecoca})\n{items.ecopriceopti}\n' \
                f'> 25% discount on x7100 tax\n' \
                f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
                f'[**Liquidity Maxi**]({items.optitoken}{items.liqca})\n{items.liqpriceopti}\n' \
                f'> 50 % discount on x7100tax\n> 25 % discount on X7R tax\n' \
                f'> 15 % discount on X7DAO tax\n\n' \
                f'[**DEX Maxi**]({items.optitoken}{items.dexca})\n{items.dexpriceopti}\n' \
                f'> LP Fee Discounts while trading on X7 DEX\n\n' \
                f'[**Borrowing Maxi**]({items.optitoken}{items.borrowca})\n{items.borrowpriceopti}\n' \
                f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
                f'[**Magister**]({items.optitoken}{items.magisterca})\n{items.magisterpriceopti}\n' \
                f'> 25% discount on x7100 tax\n' \
                f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
                f'https://x7.finance/x/nft/mint\n\n{quote}'
            await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Treasury Info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def treasury(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if chain.value == 'eth':
        cg = CoinGeckoAPI()
        cgx7rprice = (cg.get_price(ids='x7r', vs_currencies='usd', include_24hr_change='true',
                                   include_24hr_vol='true', include_last_updated_at="true"))
        x7rprice = (cgx7rprice["x7r"]["usd"])
        treasuryurl = \
            items.ethbalanceapieth + items.devmultieth + ',' + items.commultieth + ',' + items.pioneerca +\
            '&tag=latest' + keys.ether
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        pioneer = float(treasurydata["result"][2]["balance"])
        pioneeramount = str(pioneer / 10 ** 18)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        pioneerdollar = float(pioneeramount) * float(ethvalue) / 1 ** 18
        comx7rurl = \
            items.tokenbalanceapieth + items.x7rca + '&address=' + items.commultieth + '&tag=latest' + keys.ether
        comx7rresponse = requests.get(comx7rurl)
        comx7rdata = comx7rresponse.json()
        comx7r = int(comx7rdata["result"][:-18])
        comx7rprice = comx7r * x7rprice
        comx7durl =\
            items.tokenbalanceapieth + items.x7dca + '&address=' + items.commultieth + '&tag=latest' + keys.ether
        comx7dresponse = requests.get(comx7durl)
        comx7ddata = comx7dresponse.json()
        comx7d = int(comx7ddata["result"][:-18])
        comx7ddollar = float(comamount) * float(ethvalue) / 1 ** 18
        comx7dprice = comx7d * ethvalue
        comtotal = comx7rprice + comdollar + comx7ddollar
        embed.description = \
            f'**X7 Finance Treasury Info (ETH)**\n\n' \
            f'Pioneer Pool:\n{pioneeramount[:4]}ETH (${"{:0,.0f}".format(pioneerdollar)})\n\n' \
            f'[Developer Wallet:]({items.etheraddress}{items.devmultieth})\n' \
            f'{devamount[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'[Community Wallet:]({items.etheraddress}{items.commultieth})\n' \
            f'{comamount[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n' \
            f'{comx7r} X7R (${"{:0,.0f}".format(comx7rprice)})\n' \
            f'{comx7d} X7D (${"{:0,.0f}".format(comx7dprice)})\n' \
            f'Total: (${"{:0,.0f}".format(comtotal)})\n\n' \
            f'[Treasury Splitter Contract]({items.etheraddress}{items.tsplitterca})\n\n' \
            f'{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        treasuryurl = items.bnbbalanceapi + items.devmultibsc + ',' + items.commultibsc + '&tag=latest' + keys.bsc
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        ethurl = items.bnbpriceapi + keys.bsc
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (BSC)**\n\n' \
            f'Developer Wallet:\n{devamount[:4]}BNB (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'Community Wallet:\n{comamount[:4]}BNB (${"{:0,.0f}".format(comdollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.bscaddress}{items.tsplitterca})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        treasuryurl = items.ethbalanceapiarb + items.devmultiarb + ',' + items.commultiarb + '&tag=latest' + keys.arb
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (ARB)**\n\n' \
            f'Developer Wallet:\n{devamount[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'Community Wallet:\n{comamount[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.arbaddress}{items.tsplitterca})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        treasuryurl = items.ethbalanceapiopti + items.devmultiopti + ',' + items.commultiopti + '&tag=latest' +\
                      keys.opti
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (OPTIMISM)**\n\n' \
            f'Developer Wallet:\n{devamount[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'Community Wallet:\n{comamount[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.optiaddress}{items.tsplitterca})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        treasuryurl = items.maticbalanceapi + items.devmultipoly + ',' + items.commultipoly + '&tag=latest' + keys.poly
        treasuryresponse = requests.get(treasuryurl)
        treasurydata = treasuryresponse.json()
        dev = float(treasurydata["result"][0]["balance"])
        devamount = str(dev / 10 ** 18)
        com = float(treasurydata["result"][1]["balance"])
        comamount = str(com / 10 ** 18)
        ethurl = items.maticpriceapi + keys.poly
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["maticusd"])
        devdollar = float(devamount) * float(ethvalue) / 1 ** 18
        comdollar = float(comamount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (POLYGON)**\n\n' \
            f'Developer Wallet:\n{devamount[:4]}MATIC (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'Community Wallet:\n{comamount[:4]}MATIC (${"{:0,.0f}".format(comdollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.polyaddress}{items.tsplitterca})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7DAO Info, use /x7dao followed by amount to convert to $")
@app_commands.rename(amountraw='amount')
@app_commands.describe(amountraw='Amount of tokens to convert to $')
async def x7dao(interaction: discord.Interaction, amountraw: Optional[str] = None):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7daoprice = (cg.get_price(ids='x7dao', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    daoprice = (cgx7daoprice["x7dao"]["usd"])
    uniurl = items.tokenbalanceapieth + items.x7daoca + '&address=' + items.x7daopair + '&tag=latest' + keys.ether
    uniresponse = requests.get(uniurl)
    unidata = uniresponse.json()
    unidata["result"] = int(unidata["result"][:-18])
    uniresult = round(((unidata["result"] / items.supply) * 100), 6)
    x7daoholdersurl = items.holdersapi + items.x7daoca + keys.holders
    x7daoholdersresponse = requests.get(x7daoholdersurl)
    x7daoholdersdata = x7daoholdersresponse.json()
    x7daoholders = x7daoholdersdata["holdersCount"]
    if amountraw == "500000":
        amount = round(float(amountraw) * float(daoprice), 2)
        embed.description = \
            f'{amountraw} X7DAO (ETH) Currently Costs:\n\n${amount}\n\nHolding {amountraw} X7DAO Tokens ' \
            f'will earn you the right to make proposals on X7 DAO dApp\n\n{quote}'
    if amountraw:
        amount = round(float(amountraw)*float(daoprice), 2)
        embed.description = f'{amountraw} X7DAO (ETH) Currently Costs:\n\n${amount} '
    if not amountraw:
        embed.description =\
            f'**X7DAO (ETH) Info**\n\n' \
            f'X7DAO Price: ${cgx7daoprice["x7dao"]["usd"]}\n' \
            f'24 Hour Change: {round(cgx7daoprice["x7dao"]["usd_24h_change"],1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(daoprice*items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(cgx7daoprice["x7dao"]["usd_24h_vol"])}\n' \
            f'Holders: {x7daoholders}\n\n' \
            f'Uniswap Supply:\n{"{:,}".format(unidata["result"])}\n{round(uniresult,2)}% of Supply\n\n' \
            f'Contract Address:\n`{items.x7daoca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7daoca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7daopair})\n' \
            f'[Buy]({items.xchangebuy}{items.x7daoca})\n\n{quote}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7R Info, use /x7r followed by amount to convert to $')
@app_commands.rename(amountraw='amount')
@app_commands.describe(amountraw='Amount of tokens to convert to $')
async def x7r(interaction: discord.Interaction, amountraw: Optional[str] = None):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7rprice = (cg.get_price(ids='x7r', vs_currencies='usd', include_24hr_change='true',
                               include_24hr_vol='true', include_last_updated_at="true"))
    x7rprice = (cgx7rprice["x7r"]["usd"])
    burnurl = items.tokenbalanceapieth + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.ether
    burnresponse = requests.get(burnurl)
    burndata = burnresponse.json()
    burndata["result"] = int(burndata["result"][:-18])
    burnresult = round(((burndata["result"] / items.supply) * 100), 6)
    uniurl = items.tokenbalanceapieth + items.x7rca + '&address=' + items.x7rpair + '&tag=latest' + keys.ether
    uniresponse = requests.get(uniurl)
    unidata = uniresponse.json()
    unidata["result"] = int(unidata["result"][:-18])
    uniresult = round(((unidata["result"] / items.supply) * 100), 6)
    x7rholdersurl = items.holdersapi + items.x7rca + keys.holders
    x7rholdersresponse = requests.get(x7rholdersurl)
    x7rholdersdata = x7rholdersresponse.json()
    x7rholders = x7rholdersdata["holdersCount"]
    if amountraw:
        amount = round(float(amountraw)*float(x7rprice), 2)
        embed.description = f'{amountraw} X7R (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}' \
                            f'{quote}'
    if not amountraw:
        embed.description =\
            f'**X7R (ETH) Info**\n\n' \
            f'X7R Price: ${cgx7rprice["x7r"]["usd"]}\n' \
            f'24 Hour Change: {round(cgx7rprice["x7r"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(x7rprice*items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(cgx7rprice["x7r"]["usd_24h_vol"])}\n' \
            f'Holders: {x7rholders}\n\n' \
            f'X7R Tokens Burned:\n' \
            f'{"{:,}".format(burndata["result"])}\n' \
            f'{burnresult}% of Supply\n\n' \
            f'Uniswap Supply:\n{"{:,}".format(unidata["result"])}\n{round(uniresult, 2)}% of Supply\n\n' \
            f'Contract Address:\n`{items.x7rca}\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7rca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7rpair})\n' \
            f'[Buy]({items.xchangebuy}{items.x7rca})\n\n{quote}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7101 Info, use /x7101 followed by amount to convert to $')
@app_commands.rename(amountraw='amount')
@app_commands.describe(amountraw='Amount of tokens to convert to $')
async def x7101(interaction: discord.Interaction, amountraw: Optional[str] = None):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7101price = (cg.get_price(ids='x7101', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7101price = (cgx7101price["x7101"]["usd"])
    x7101holdersurl = items.holdersapi + items.x7101ca + keys.holders
    x7101holdersresponse = requests.get(x7101holdersurl)
    x7101holdersdata = x7101holdersresponse.json()
    x7101holders = x7101holdersdata["holdersCount"]
    if amountraw:
        amount = round(float(amountraw)*float(x7101price), 2)
        embed.description = f'{amountraw} X7101 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)} '
    if not amountraw:
        embed.description =\
            f'**X7101 (ETH) Info**\n\n' \
            f'X7101 Price: ${cgx7101price["x7101"]["usd"]}\n' \
            f'24 Hour Change: {round(cgx7101price["x7101"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(x7101price * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(cgx7101price["x7101"]["usd_24h_vol"])}\n' \
            f'Holders: {x7101holders}\n\n' \
            f'Contract Address:\n`{items.x7101ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7101ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7101pair})\n' \
            f'[Buy]({items.xchangebuy}{items.x7101ca})\n\n{quote}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7102 Info, use /x7102 followed by amount to convert to $')
@app_commands.rename(amountraw='amount')
@app_commands.describe(amountraw='Amount of tokens to convert to $')
async def x7102(interaction: discord.Interaction, amountraw: Optional[str] = None):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7102price = (cg.get_price(ids='x7102', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7102price = (cgx7102price["x7102"]["usd"])
    x7102holdersurl = items.holdersapi + items.x7102ca + keys.holders
    x7102holdersresponse = requests.get(x7102holdersurl)
    x7102holdersdata = x7102holdersresponse.json()
    x7102holders = x7102holdersdata["holdersCount"]
    if amountraw:
        amount = round(float(amountraw)*float(x7102price), 2)
        embed.description = f'{amountraw} X7102 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n' \
                            f'{quote}'
    if not amountraw:
        embed.description = \
            f'**X7102 (ETH) Info**\n\n' \
            f'X7102 Price: ${cgx7102price["x7102"]["usd"]}\n' \
            f'24 Hour Change: {round(cgx7102price["x7102"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(x7102price*items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(cgx7102price["x7102"]["usd_24h_vol"])}\n' \
            f'Holders: {x7102holders}\n\n' \
            f'Contract Address:\n`{items.x7102ca}\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7102ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7102pair})\n' \
            f'[Buy]({items.xchangebuy}{items.x7102ca})\n\n{quote}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7103 Info, use /x7103 followed by amount to convert to $')
@app_commands.rename(amountraw='amount')
@app_commands.describe(amountraw='Amount of tokens to convert to $')
async def x7103(interaction: discord.Interaction, amountraw: Optional[str] = None):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7103price = (cg.get_price(ids='x7103', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7103price = (cgx7103price["x7103"]["usd"])
    x7103holdersurl = items.holdersapi + items.x7103ca + keys.holders
    x7103holdersresponse = requests.get(x7103holdersurl)
    x7103holdersdata = x7103holdersresponse.json()
    x7103holders = x7103holdersdata["holdersCount"]
    if amountraw:
        amount = round(float(amountraw)*float(x7103price), 2)
        embed.description = f'{amountraw} X7103 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n' \
                            f'{quote}'
    if not amountraw:
        embed.description = \
            f'**X7103 (ETH) Info**\n\n' \
            f'X7103 Price: ${cgx7103price["x7103"]["usd"]}\n' \
            f'24 Hour Change: {round(cgx7103price["x7103"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(x7103price * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(cgx7103price["x7103"]["usd_24h_vol"])}\n' \
            f'Holders: {x7103holders}\n\n' \
            f'Contract Address:\n`{items.x7103ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7103ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7103pair})\n' \
            f'[Buy]({items.xchangebuy}{items.x7103ca})\n\n{quote}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7104 Info, use /x7104 followed by amount to convert to $')
@app_commands.rename(amountraw='amount')
@app_commands.describe(amountraw='Amount of tokens to convert to $')
async def x7104(interaction: discord.Interaction, amountraw: Optional[str] = None):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7104price = (cg.get_price(ids='x7104', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7104price = (cgx7104price["x7104"]["usd"])
    x7104holdersurl = items.holdersapi + items.x7104ca + keys.holders
    x7104holdersresponse = requests.get(x7104holdersurl)
    x7104holdersdata = x7104holdersresponse.json()
    x7104holders = x7104holdersdata["holdersCount"]
    if amountraw:
        amount = round(float(amountraw)*float(x7104price), 2)
        embed.description = f'{amountraw} X7104 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n' \
                            f'{quote}'
    if not amountraw:
        embed.description = \
            f'**X7104 (ETH) Info**\n\n' \
            f'X7104 Price: ${cgx7104price["x7104"]["usd"]}\n' \
            f'24 Hour Change: {round(cgx7104price["x7104"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(x7104price * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(cgx7104price["x7104"]["usd_24h_vol"])}\n' \
            f'Holders: {x7104holders}\n\n' \
            f'Contract Address:\n`{items.x7104ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7104ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7104pair})\n' \
            f'[Buy]({items.xchangebuy}{items.x7104ca})\n\n{quote}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7105 Info, use /x7105 followed by amount to convert to $')
@app_commands.rename(amountraw='amount')
@app_commands.describe(amountraw='Amount of tokens to convert to $')
async def x7105(interaction: discord.Interaction, amountraw: Optional[str] = None):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7105price = (cg.get_price(ids='x7105', vs_currencies='usd', include_24hr_change='true',
                                 include_24hr_vol='true', include_last_updated_at="true"))
    x7105price = (cgx7105price["x7105"]["usd"])
    x7105holdersurl = items.holdersapi + items.x7105ca + keys.holders
    x7105holdersresponse = requests.get(x7105holdersurl)
    x7105holdersdata = x7105holdersresponse.json()
    x7105holders = x7105holdersdata["holdersCount"]
    if amountraw:
        amount = round(float(amountraw)*float(x7105price), 2)
        embed.description = f'{amountraw} X7105 (ETH) Currently Costs:\n\n${"{:0,.0f}".format(amount)}\n\n' \
                            f'{quote}'
    if not amountraw:
        embed.description = \
            f'**X7105 (ETH) Info**\n\n' \
            f'X7105 Price: ${cgx7105price["x7105"]["usd"]}\n' \
            f'24 Hour Change: {round(cgx7105price["x7105"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(x7105price * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(cgx7105price["x7105"]["usd_24h_vol"])}\n' \
            f'Holders: {x7105holders}\n\n' \
            f'Contract Address:\n`{items.x7105ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7105ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7105pair})\n' \
            f'[Buy]({items.xchangebuy}{items.x7105ca})\n\n{quote}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description="X7 Finance Whitepaper links")
async def wp(interaction: discord.Interaction):
    embed.description = \
        '**X7 Finance Whitepaper Links**\n\n' \
        f'{random.choice(items.quotes)}\n\n' \
        '[Full WP](https://x7.finance/whitepaper)\n' \
        '[Short WP](https://x7community.space/wp-short.pdf)'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Buy links")
async def buy(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = '**X7 Finance buy links**\n\nUse ``/x7tokenname`` for all other details\n\n' \
                        f'[X7R - Rewards Token]({items.xchangebuy}{items.x7rca})\n' \
                        f'[X7DAO - Governance Token]({items.xchangebuy}{items.x7daoca})\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Chart links")
async def chart(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = '**X7 Finance Chart links (ETH)**\n\nUse ``/x7tokenname`` for all other details\n\n' \
                        f'[X7R - Rewards Token]({items.dextoolseth}{items.x7rpair})\n' \
                        f'[X7DAO - Governance Token]({items.dextoolseth}{items.x7daopair})\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token contract info")
async def contract(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = f'**X7 Finance token contract info**\n\n**X7R**\n`{items.x7rca}`' \
                        f'\n\n**X7DAO**\n`{items.x7daoca}`\n\n' \
                        f'Use `/x7tokenname` for all other details\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="A Guide to buying all constellation tokens evenly")
async def buyevenly(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = '**Buy all X7 Finance constellation tokens evenly (ETH)**\n\n' \
                        'Simply connect to https://dapp.x7community.space/ via metamask mobile or desktop and ' \
                        'navigate to Buy X7 Constellation tokens equally\' and enter your desired Eth amount\n\n' \
                        'Alternatively you can interact with the follow contract and follow the steps below:\n\n' \
                        '1. Head over to the Buy Evenly contract:\nhttps://etherscan.io/address/0x0419074afe1a137dfa' \
                        '6afd5b6af5771c3ffbea49#code\n' \
                        '1.1. Press on "Contract" If it\'s not already selected.\n2. Press on "Write contract"\n' \
                        '3. Press on "Connect to Web3" and connect your desired wallet to the website. \n' \
                        '4. Deposit the desired values\n4.1. depositIntoX7SeriesTokens -> amount of ETH you want to ' \
                        'spend (e.g. 0.5).\n' \
                        '4.2. slippagePercent  -> desired slippage (e.g. 4)\n4.3 deadline -> Go to [epochconverter]' \
                        '(https://www.epochconverter.com/) and add like 500 to the current epoch. Click "Timestamp ' \
                        'to Human date" ' \
                        'and verify that Relative is at least "In 1 minute" (e.g. 1667508502).\n' \
                        '4.4 Copy the epoch to the "deadline" field\n4.4 Press "Write" and confirm the transaction ' \
                        'in your wallet.\n' \
                        '4.5 You should receive tokens to your wallet in few blocks.\n\n' \
                        '**Testrun TX**:\n' \
                        'https://etherscan.io/tx/0x321e5bb6cc1695d5d7085eceb92f01143b69c2274402aab46e4a0a47d069d' \
                        '0af\n\nCredit: @WoxieX\n\n' \
                        '[Via Dashboard](https://dapp.x7community.space/)\n' \
                        '[Via Etherscan](https://etherscan.io/address/0x0419074afe1a137dfa6afd5b6af5771c3ffbea4' \
                        f'9#code)\n[Epoch Convertor](https://www.epochconverter.com/)\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description='X7R Pioneer NFT info, use /pioneer followed by number to see NFT info')
@app_commands.rename(pioneerid='pioneer-id')
@app_commands.describe(pioneerid='Show Pioneer NFT #')
async def pioneer(interaction: discord.Interaction, pioneerid: Optional[str] = None):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if not pioneerid:
        slug = "/x7-pioneer"
        headers = {"X-API-KEY": keys.os}
        pioneerurl = items.osapi + slug
        pioneerresponse = requests.get(pioneerurl, headers=headers)
        pioneerdata = pioneerresponse.json()
        floor = (pioneerdata["collection"]["stats"]["floor_price"])
        traits = (pioneerdata["collection"]["traits"]["Transfer Lock Status"]["unlocked"])
        cap = round(pioneerdata["collection"]["stats"]["market_cap"], 2)
        sales = (pioneerdata["collection"]["stats"]["total_sales"])
        owners = (pioneerdata["collection"]["stats"]["num_owners"])
        avgprice = round(pioneerdata["collection"]["stats"]["average_price"], 2)
        volume = round(pioneerdata["collection"]["stats"]["total_volume"], 2)
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        pioneerethurl = items.ethbalanceapieth + items.pioneerca + '&tag=latest' + keys.ether
        pioneerethresponse = requests.get(pioneerethurl)
        pioneerethdata = pioneerethresponse.json()
        pioneerth = float(pioneerethdata["result"][0]["balance"])
        totalamount = str(pioneerth / 10 ** 18)
        totaldollarraw = float(totalamount) * float(ethvalue) / 1 ** 18
        totaldollar = str(totaldollarraw)
        pioneereamount = str(pioneerth / 10 ** 18 / 639)
        pioneerdollarraw = float(totalamount) * float(ethvalue) / 1 ** 18 / 639
        pioneerdollar = str(pioneerdollarraw)
        embed.description = \
            f'**X7 Pioneer NFT Info**\n\nFloor Price: {floor} ETH\n' \
            f'Average Price: {avgprice} ETH\n' \
            f'Market Cap: {cap} ETH\n' \
            f'Total Volume: {volume} ETH\n' \
            f'Total Sales: {sales}\n' \
            f'Number of Owners: {owners}\n' \
            f'Pioneers Unlocked: {traits}\n' \
            f'Pioneer Pool: {totalamount[:3]} ETH (${totaldollar[:4]})\n\n' \
            f'Pioneer Earnings: {pioneereamount[:5]} ETH (${pioneerdollar[:4]})\n\n{quote}'
    else:
        baseurl = "https://api.opensea.io/api/v1/asset/"
        slug = items.pioneerca + "/"
        headers = {"X-API-KEY": keys.os}
        singleurl = baseurl + slug + pioneerid + "/"
        singleresponse = requests.get(singleurl, headers=headers)
        singledata = singleresponse.json()
        status = (singledata["traits"][0]["value"])
        picture = (singledata["image_url"])
        embed.description = f'**X7 Pioneer {pioneerid} NFT info**\n\n' \
                            f'Transfer Lock Status: {status}\n\n' \
                            f'X7 Pioneer Dashboard - https://x7.finance/x/nft/pioneer\n\n' \
                            f'Opensea - https://opensea.io/assets/ethereum/0x70000299ee8910ccacd97b1bb560e' \
                            f'34f49c9e4f7/{pioneerid}'
        embed.set_image(url=picture)
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7R Token burn info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def burn(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if chain.value == "eth":
        burnurl = items.tokenbalanceapieth + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.ether
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (ETH)**:\n\n' \
            f'{"{:,}".format(burndata["result"])}\n' \
            f'{result}% of Supply\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7rca}?a={items.dead})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        burnurl = items.tokenbalanceapibsc + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.bsc
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (BSC)**:\n\n' \
            f'{"{:,}".format(burndata["result"])}\n' \
            f'{result}% of Supply\n\n' \
            f'[BSCscan]({items.bsctoken}{items.x7rca}?a={items.dead})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        burnurl = items.tokenbalanceapiarb + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.arb
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (ARBITRUM)**:\n\n' \
            f'{"{:,}".format(burndata["result"])}\n' \
            f'{result}% of Supply\n\n' \
            f'[Arbiscan]({items.arbtoken}{items.x7rca}?a={items.dead})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        burnurl = items.tokenbalanceapiopti + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.opti
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (OPTIMISM)**:\n\n' \
            f'{"{:,}".format(burndata["result"])}\n' \
            f'{result}% of Supply\n\n' \
            f'[Optimism.Etherscan]({items.optitoken}{items.x7rca}?a={items.dead})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        burnurl = items.tokenbalanceapipoly + items.x7rca + '&address=' + items.dead + '&tag=latest' + keys.poly
        burnresponse = requests.get(burnurl)
        burndata = burnresponse.json()
        burndata["result"] = int(burndata["result"][:-18])
        result = round(((burndata["result"] / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (POLYGON)**:\n\n' \
            f'{"{:,}".format(burndata["result"])}\n' \
            f'{result}% of Supply\n\n' \
            f'[Polygonscan]({items.polytoken}{items.x7rca}?a={items.dead})\n\n{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Market Cap Info")
async def mcap(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    cg = CoinGeckoAPI()
    cgx7rprice = (cg.get_price(ids='x7r', vs_currencies='usd'))
    x7rprice = (cgx7rprice["x7r"]["usd"]) * items.supply
    cgx7daoprice = (cg.get_price(ids='x7dao', vs_currencies='usd'))
    x7daoprice = (cgx7daoprice["x7dao"]["usd"]) * items.supply
    cgx7101price = (cg.get_price(ids='x7101', vs_currencies='usd'))
    x7101price = (cgx7101price["x7101"]["usd"]) * items.supply
    cgx7102price = (cg.get_price(ids='x7102', vs_currencies='usd'))
    x7102price = (cgx7102price["x7102"]["usd"]) * items.supply
    cgx7103price = (cg.get_price(ids='x7103', vs_currencies='usd'))
    x7103price = (cgx7103price["x7103"]["usd"]) * items.supply
    cgx7104price = (cg.get_price(ids='x7104', vs_currencies='usd'))
    x7104price = (cgx7104price["x7104"]["usd"]) * items.supply
    cgx7105price = (cg.get_price(ids='x7105', vs_currencies='usd'))
    x7105price = (cgx7105price["x7105"]["usd"]) * items.supply
    embed.description = \
        f'**X7 Finance Market Cap Info (ETH)**\n\n' \
        f'X7R:          ${"{:0,.0f}".format(x7rprice)}\n' \
        f'X7DAO:     ${"{:0,.0f}".format(x7daoprice)}\n' \
        f'X7101:       ${"{:0,.0f}".format(x7101price)}\n' \
        f'X7102:       ${"{:0,.0f}".format(x7102price)}\n' \
        f'X7103:       ${"{:0,.0f}".format(x7103price)}\n' \
        f'X7104:       ${"{:0,.0f}".format(x7104price)}\n' \
        f'X7105:       ${"{:0,.0f}".format(x7105price)}\n\n' \
        f'Constellations Combined: ' \
        f'${"{:0,.0f}".format(x7101price + x7102price + x7103price + x7104price + x7105price)}\n' \
        f'Total Token Marketcap:\n' \
        f'    ${"{:0,.0f}".format(x7rprice+x7daoprice+x7101price+x7102price+x7103price+x7104price+x7105price)}' \
        f'\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Roadmap Info")
async def roadmap(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = f'**X7 Finance Roadmap**\n\n' \
                        f'Devs are making incremental final progress against all ecosystem deliverables, we expect ' \
                        f'the following order of delivery:\n\n' \
                        f'1. Whitepaper ✅\n' \
                        f'2. Pioneer NFT & Reward Pool ✅\n' \
                        f'3. DEX and Leveraged Initial Liquidity:\n' \
                        f'3.1. X7D token contract ✅\n' \
                        f'3.2. A gnosis multisig wallet that will be used to manage the X7D token ownership' \
                        f' prior to DAO control turnover ✅\n' \
                        f'3.3. Lending pool reserve contract ✅\n' \
                        f'3.4. v1 lending pool contract ✅\n' \
                        f'3.5. First three Loan Term NFT contracts ✅\n' \
                        f'3.6. Lending Pool Discount Authority contract ✅\n' \
                        f'3.7. XchangeFactory and XchangePair contracts ✅\n' \
                        f'3.8. V1 XchangeRouter ✅\n' \
                        f'3.9. V1 XchangeOmniRouter, ✅\n' \
                        f'4. Lender dApp 🔄\n' \
                        f'5. X7D minting 🔄\n' \
                        f'6. X7D staking 🔄\n' \
                        f'7. X7D dApp 🔄\n' \
                        f'8. Governance contracts 🔄\n' \
                        f'9. Governance dApp 🔄\n' \
                        f'X. Initial DAO control turnover 🔄\n\n' \
                        f'In addition to the above development milestones, the following additional deliveries ' \
                        f'can be expected:\n\n' \
                        f'**Marketing Materials:**\n' \
                        f'> Investor deck / summary\n' \
                        f'> Prettified ecosystem diagrams and explanations\n\n' \
                        f'**Development Tooling and Documentation:**\n' \
                        f'> Technical design document for all smart contracts\n' \
                        f'> Smart contract trust diagram\n' \
                        f'> Technical User Guide for DAO interactions\n' \
                        f'> Integration Guide for third party integrations\n' \
                        f'> Open sourced SDKs for smart contract interactions\n' \
                        f'> Open sourced testing and development tooling\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Lending pool info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def pool(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if chain.value == 'eth':
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        poolurl = items.ethbalanceapieth + items.lpreserveca + '&tag=latest' + keys.ether
        poolresponse = requests.get(poolurl)
        pooldata = poolresponse.json()
        dev = float(pooldata["result"][0]["balance"])
        poolamount = str(dev / 10 ** 18)
        pooldollarraw = float(poolamount) * float(ethvalue) / 1 ** 18
        pooldollar = str(pooldollarraw)
        embed.description = \
            f'**X7 Finance Lending Pool Info (ETH)**\n\n' \
            f'{poolamount[:4]}ETH (${pooldollar[:8]})\n\n' \
            f'To contribute to the Lending Pool:\n\n' \
            '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.etheraddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.etheraddress}{items.x7dca})\n\n' \
            f'{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == 'bsc':
        ethurl = items.bnbpriceapi + keys.bsc
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        poolurl = items.bnbbalanceapi + items.lpreserveca + '&tag=latest' + keys.bsc
        poolresponse = requests.get(poolurl)
        pooldata = poolresponse.json()
        dev = float(pooldata["result"][0]["balance"])
        poolamount = str(dev / 10 ** 18)
        pooldollarraw = float(poolamount) * float(ethvalue) / 1 ** 18
        pooldollar = str(pooldollarraw)
        embed.description = \
            f'**X7 Finance Lending Pool Info (BSC)**\n\n' \
            f'{poolamount[:4]}BNB (${pooldollar[:8]})\n\n' \
            f'To contribute to the Lending Pool:\n\n' \
            '1. Send BNB (Not Swap) to the Lending Pool Reserve Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:BNB\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.bscaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.bscaddress}{items.x7dca})\n\n' \
            f'{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == 'poly':
        ethurl = items.maticpriceapi + keys.poly
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["maticusd"])
        poolurl = items.maticbalanceapi + items.lpreserveca + '&tag=latest' + keys.poly
        poolresponse = requests.get(poolurl)
        pooldata = poolresponse.json()
        dev = float(pooldata["result"][0]["balance"])
        poolamount = str(dev / 10 ** 18)
        pooldollarraw = float(poolamount) * float(ethvalue) / 1 ** 18
        pooldollar = str(pooldollarraw)
        embed.description = \
            f'**X7 Finance Lending Pool Info (POLYGON)**\n\n' \
            f'{poolamount[:4]}MATIC (${pooldollar[:8]})\n\n' \
            f'To contribute to the Lending Pool:\n\n' \
            '1. Send MATIC (Not Swap) to the Lending Pool Reserve Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:MATIC\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.polyaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.polyaddress}{items.x7dca})\n\n' \
            f'{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == 'arb':
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        poolurl = items.ethbalanceapiarb + items.lpreserveca + '&tag=latest' + keys.arb
        poolresponse = requests.get(poolurl)
        pooldata = poolresponse.json()
        dev = float(pooldata["result"][0]["balance"])
        poolamount = str(dev / 10 ** 18)
        pooldollarraw = float(poolamount) * float(ethvalue) / 1 ** 18
        pooldollar = str(pooldollarraw)
        embed.description = \
            f'**X7 Finance Lending Pool Info (ARB)**\n\n' \
            f'{poolamount[:4]}ETH (${pooldollar[:8]})\n\n' \
            f'To contribute to the Lending Pool:\n\n' \
            '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.arbaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.arbaddress}{items.x7dca})\n\n' \
            f'{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == 'opti':
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        poolurl = items.ethbalanceapiopti + items.lpreserveca + '&tag=latest' + keys.opti
        poolresponse = requests.get(poolurl)
        pooldata = poolresponse.json()
        dev = float(pooldata["result"][0]["balance"])
        poolamount = str(dev / 10 ** 18)
        pooldollarraw = float(poolamount) * float(ethvalue) / 1 ** 18
        pooldollar = str(pooldollarraw)
        embed.description = \
            f'**X7 Finance Lending Pool Info (OPTIMISM)**\n\n' \
            f'{poolamount[:4]}ETH (${pooldollar[:8]})\n\n' \
            f'To contribute to the Lending Pool:\n\n' \
            '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.optiaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.optiaddress}{items.x7dca})\n\n' \
            f'{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token listing links")
async def listings(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = f'**X7 Finance token listing links**\n\n' \
                        f'**X7R**\nhttps://coinmarketcap.com/currencies/x7r/\n' \
                        f'https://www.coingecko.com/en/coins/x7r\n' \
                        f'https://tokeninsight.com/en/coins/x7r/overview\n' \
                        f'https://coinbazooka.com/coin/X7R\n\n' \
                        f'**X7DAO**\n' \
                        f'https://coinmarketcap.com/currencies/x7dao/\n' \
                        f'https://www.coingecko.com/en/coins/x7dao\n' \
                        f'https://tokeninsight.com/en/coins/x7dao/overview\n' \
                        f'https://coinbazooka.com/coin/X7dao\n\n' \
                        f'**Constellations**\n' \
                        f'https://www.coingecko.com/en/coins/x7101\n' \
                        f'https://www.coingecko.com/en/coins/x7102\n' \
                        f'https://www.coingecko.com/en/coins/x7103\n' \
                        f'https://www.coingecko.com/en/coins/x7104\n' \
                        f'https://www.coingecko.com/en/coins/x7105\n\n' \
                        f'**NFTs**\n' \
                        f'https://www.coingecko.com/en/nft/x7-pioneer\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token tax info")
async def tax(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = f'**X7 Finance Token Tax Info**\n\n' \
                        f'X7R: 6%\nX7DAO: 6%\n' \
                        f'X7101-X7105: 2%\n\n' \
                        f'**Tax with NFTs**\n' \
                        f'Liquidity Maxi:\nX7R: 4.50%\n7DAO: 5.10%\nX7101-X7105: 1.00%\n\n' \
                        f'Ecosystem Maxi:\nX7R: 5.40%\nX7DAO: 5.40%\nX7101-X7105: 1.50%\n\n' \
                        f'Magister:\nX7R: 4.50%\nX7DAO: 6.00%\nX7101-X7105: 1.50%\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Opensea links")
async def opensea(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = '**X7 Finance Opensea links (ETH)**\n\n' \
                        '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi)\n' \
                        '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi)\n' \
                        '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi)\n' \
                        '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max)\n' \
                        '[Magister](https://opensea.io/collection/x7-magister)\n' \
                        f'[Pioneer](https://opensea.io/collection/x7-pioneer)\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Xchange DEX info")
async def swap(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = f'**X7 Finance Xchange Info**\n\nhttps://app.x7.finance/#/swap\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Report user to moderators")
async def report(interaction: discord.Interaction, username: str, reason: str):
    await interaction.response.send_message(f"Thanks {interaction.user}, Your report has been received", ephemeral=True)
    reportchannel = client.get_channel(1028614982000193588)
    await reportchannel.send(f'<@&1016659542303580221>\n\n{interaction.user} Has reported {username} for:\n{reason}')


@client.tree.command(description="Join X7Force!")
async def x7force(interaction: discord.Interaction, twitterhandle: str):
    await interaction.response.send_message(f"Thanks {interaction.user}, Your request for x7force has been "
                                            f"received", ephemeral=True)
    reportchannel = client.get_channel(1028614982000193588)
    await reportchannel.send(f'<@&1016659542303580221>\n\n{interaction.user} Has requested {twitterhandle} '
                             f'to be added to x7force')


@client.tree.command(description="X7 Finance Twitter Spaces Info")
async def spaces(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    then = variables.spacestime
    now = datetime.now()
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    if duration < timedelta(0):
        embed.description = f'X7 Finance Twitter space\n\nPlease check back for more details\n\n{quote}'
    else:
        embed.description = f'Next X7 Finance Twitter space is:\n\n{then} (UTC)\n\n' \
                            f'%d days, %d hours, %d minutes and %d seconds\n\n' \
                            f'[Click here]({variables.spaceslink}) to set a reminder!' \
                            f'\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Make a joke")
async def joke(interaction: discord.Interaction):
    url = 'https://v2.jokeapi.dev/joke/Any?safe-mode'
    response = requests.get(url)
    jokefull = response.json()
    if jokefull["type"] == "single":
        embed.description = f'`{jokefull["joke"]}`'
        await interaction.response.send_message(file=thumb, embed=embed)
    else:
        embed.description = f'`{jokefull["setup"]}\n\n{jokefull["delivery"]}`'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="An inspirational quote")
async def quote(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = f'{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token price info")
@app_commands.describe(coin='Coin Name')
async def price(interaction: discord.Interaction, coin: Optional[str] = ""):
    basetokenurl = 'https://api.coingecko.com/api/v3/search?query='
    tokenurl = basetokenurl + coin
    tokenresponse = requests.get(tokenurl)
    token = tokenresponse.json()
    tokenid = token["coins"][0]["api_symbol"]
    tokenlogo = token["coins"][0]["thumb"]
    symbol = token["coins"][0]["symbol"]
    cg = CoinGeckoAPI()
    tokenprice = (cg.get_price(ids=tokenid, vs_currencies='usd', include_24hr_change='true',
                               include_24hr_vol='true', include_market_cap="true"))
    cgtogetherprice = (cg.get_price(ids='x7r,x7dao', vs_currencies='usd', include_24hr_change='true',
                                    include_24hr_vol='true'))
    if coin == "eth":
        quoteresponse = requests.get(items.quoteapi)
        quotedata = quoteresponse.json()
        quoteraw = (random.choice(quotedata))
        quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
        cg = CoinGeckoAPI()
        eth = (cg.get_price(ids='ethereum', vs_currencies='usd', include_24hr_change='true',
                                include_market_cap="true"))
        baseurl = "https://api.etherscan.io/api"
        gas = "?module=gastracker&action=gasoracle"
        gasurl = baseurl + gas + keys.ether
        gasresponse = requests.get(gasurl)
        gasdata = gasresponse.json()
        ether = "?module=stats&action=ethprice"
        ethurl = baseurl + ether + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        block = "?module=proxy&action=eth_blockNumber"
        blockurl = baseurl + block + keys.ether
        blockresponse = requests.get(blockurl)
        blockdataraw = blockresponse.json()
        blockdata = int(blockdataraw["result"], 16)
        ethembed = discord.Embed(colour=7419530)
        ethembed.set_footer(text="Trust no one, Trust code. Long live Defi")
        ethembed.set_thumbnail(url=tokenlogo)
        eththumb = discord.File('X7whitelogo.png')
        ethembed.description = \
            f'**{symbol} price**\n\n' \
            f'Eth Price:\n${ethdata["result"]["ethusd"]}\n' \
            f'24 Hour Change: {round(eth["ethereum"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap: ${"{:0,.0f}".format(eth["ethereum"]["usd_market_cap"])}\n\n' \
            f'Gas Prices:\n' \
            f'Low: {gasdata["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gasdata["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gasdata["result"]["FastGasPrice"]} Gwei\n\n' \
            f'Last Block: {blockdata}\n\n{quote}'
        await interaction.response.send_message(file=eththumb, embed=ethembed)
        return
    if coin == "":
        quoteresponse = requests.get(items.quoteapi)
        quotedata = quoteresponse.json()
        quoteraw = (random.choice(quotedata))
        quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
        embed = discord.Embed(colour=7419530)
        embed.set_footer(text="Trust no one, Trust code. Long live Defi")
        embed.set_thumbnail(url='attachment://X7whitelogo.png')
        embed.description = f'**X7 Finance Token Prices  (ETH)**\n\n' \
                            f'X7R:      ${cgtogetherprice["x7r"]["usd"]}\n' \
                            f'24 Hour Change: {round(cgtogetherprice["x7r"]["usd_24h_change"], 1)}%\n\n' \
                            f'X7DAO:  ${cgtogetherprice["x7dao"]["usd"]}\n' \
                            f'24 Hour Change: {round(cgtogetherprice["x7dao"]["usd_24h_change"], 0)}%\n\n' \
                            f'{quote}'
        await interaction.response.send_message(embed=embed)
    else:
        quoteresponse = requests.get(items.quoteapi)
        quotedata = quoteresponse.json()
        quoteraw = (random.choice(quotedata))
        quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
        embed = discord.Embed(colour=7419530)
        embed.set_footer(text="Trust no one, Trust code. Long live Defi")
        embed.set_thumbnail(url=tokenlogo)
        embed.description = f'**{symbol} price**\n\n' \
                            f'Price:      ${tokenprice[tokenid]["usd"]}\n' \
                            f'24 Hour Change: {round(tokenprice[tokenid]["usd_24h_change"], 1)}%\n' \
                            f'Market Cap: ${"{:0,.0f}".format(tokenprice[tokenid]["usd_market_cap"])}\n\n' \
                            f'{quote}'
        await interaction.response.send_message(embed=embed)


@client.tree.command(description="X7 Finance Token Holders")
async def holders(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    x7rholdersurl = items.holdersapi + items.x7rca + keys.holders
    x7rholdersresponse = requests.get(x7rholdersurl)
    x7rholdersdata = x7rholdersresponse.json()
    x7rholders = x7rholdersdata["holdersCount"]
    x7daoholdersurl = items.holdersapi + items.x7daoca + keys.holders
    x7daoholdersresponse = requests.get(x7daoholdersurl)
    x7daoholdersdata = x7daoholdersresponse.json()
    x7daoholders = x7daoholdersdata["holdersCount"]
    embed.description = '**X7 Finance Token Holders (ETH)**\n\n' \
                        f'X7R Holders: {x7rholders}\n' \
                        f'X7DAO Holders: {x7daoholders}\n\n' \
                        f'{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Market Fear Greed Index")
async def fg(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    fearurl = "https://api.alternative.me/fng/?limit=0"
    fearresponse = requests.get(fearurl)
    feardata = fearresponse.json()
    timestamp = float(feardata["data"][0]["timestamp"])
    localtime = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][1]["timestamp"])
    localtime1 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][2]["timestamp"])
    localtime2 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][3]["timestamp"])
    localtime3 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][4]["timestamp"])
    localtime4 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][5]["timestamp"])
    localtime5 = datetime.fromtimestamp(timestamp)
    timestamp = float(feardata["data"][6]["timestamp"])
    localtime6 = datetime.fromtimestamp(timestamp)
    duration_in_s = float(feardata["data"][0]["time_until_update"])
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    embed.description = \
        f'**Market Fear and Greed Index**\n\n' \
        f'{feardata["data"][0]["value"]} - {feardata["data"][0]["value_classification"]} - {localtime} \n\n' \
        f'Change:\n' \
        f'{feardata["data"][1]["value"]} - {feardata["data"][1]["value_classification"]} - {localtime1}\n' \
        f'{feardata["data"][2]["value"]} - {feardata["data"][2]["value_classification"]} - {localtime2}\n' \
        f'{feardata["data"][3]["value"]} - {feardata["data"][3]["value_classification"]} - {localtime3}\n' \
        f'{feardata["data"][4]["value"]} - {feardata["data"][4]["value_classification"]} - {localtime4}\n' \
        f'{feardata["data"][5]["value"]} - {feardata["data"][5]["value_classification"]} - {localtime5}\n' \
        f'{feardata["data"][6]["value"]} - {feardata["data"][6]["value_classification"]} - {localtime6}\n\n' \
        f'Next Update:\n' \
        f'%d hours, %d minutes and %d seconds\n\n' \
        f'{quote}' % (hours[0], minutes[0], seconds[0])
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7D Token Info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def x7d(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if chain.value == "eth":
        x7dholdersurl = items.holdersapi + items.x7dca + keys.holders
        x7dholdersresponse = requests.get(x7dholdersurl)
        x7dholdersdata = x7dholdersresponse.json()
        x7dholders = x7dholdersdata["holdersCount"]
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7durl = items.ethbalanceapieth + items.lpreserveca + '&tag' + keys.ether
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7D Info (ETH)**\n\n' \
            f'Supply: {x7damount[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
            f'Holders: {x7dholders}\n\n' \
            f'To receive X7D:\n\n' \
            '1. Send ETH (Not Swap) to the Lending Pool Reserve Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.etheraddress}{items.lpreserveca})\n'\
            f'[X7D Contract]({items.etheraddress}{items.x7dca})\n\n'\
            f'`{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        ethurl = items.bnbpriceapi + keys.bsc
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7durl = items.bnbbalanceapi + items.lpreserveca + '&tag' + keys.bsc
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7D Info (BSC)**\n\n' \
            f'Supply: {x7damount[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
            f'To receive X7D:\n\n' \
            '1. Send BNB (Not Swap) to the Lending Pool Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:BNB\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.bscaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.bscaddress}{items.x7dca})\n\n' \
            f'`{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        ethurl = items.maticpriceapi + keys.poly
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["maticusd"])
        x7durl = items.maticbalanceapi + items.lpreserveca + '&tag' + keys.poly
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7D Info (POLYGON)**\n\n' \
            f'Supply: {x7damount[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
            f'To receive X7D:\n\n' \
            '1. Send MATIC (Not Swap) to the Lending Pool Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:MATIC\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.polyaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.polyaddress}{items.x7dca})\n\n' \
            f'`{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7durl = items.ethbalanceapiarb + items.lpreserveca + '&tag' + keys.arb
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7D Info (ETH)**\n\n' \
            f'Supply: {x7damount[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
            f'To receive X7D:\n\n' \
            '1. Send ETH (Not Swap) to the Lending Pool Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.arbaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.arbaddress}{items.x7dca})\n\n' \
            f'`{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        ethurl = items.ethpriceapi + keys.ether
        ethresponse = requests.get(ethurl)
        ethdata = ethresponse.json()
        ethvalue = float(ethdata["result"]["ethusd"])
        x7durl = items.ethbalanceapiopti + items.lpreserveca + '&tag' + keys.opti
        x7dresponse = requests.get(x7durl)
        x7ddata = x7dresponse.json()
        damount = float(x7ddata["result"][0]["balance"])
        x7damount = str(damount / 10 ** 18)
        x7ddollar = float(x7damount) * float(ethvalue) / 1 ** 18
        embed.description = \
            '**X7D Info (OPTIMISM)**\n\n' \
            f'Supply: {x7damount[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
            f'To receive X7D:\n\n' \
            '1. Send ETH (Not Swap) to the Lending Pool Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.optiaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.optiaddress}{items.x7dca})\n\n' \
            f'`{quote}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Loan Term Info")
@app_commands.choices(loan_type=[
    app_commands.Choice(name="Full list", value="all"),
    app_commands.Choice(name="1. Simple Loan", value="x7ill001"),
    app_commands.Choice(name="2. Amortizing Loan with interest", value="x7ill002"),
    app_commands.Choice(name="3. Interest Only Loan", value="x7illoo3"),
    ])
@app_commands.rename(loan_type='type')
async def loans(interaction: discord.Interaction, loan_type: app_commands.Choice[str]):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    if loan_type.value == "all":
        embed.description = \
            '**X7 Finance Loan Terms**\n\n' \
            'Loan terms are defined by standalone smart contracts that provide the following:\n\n' \
            '1. Loan origination fee\n' \
            '2. Loan retention premium fee schedule\n' \
            '3. Principal repayment condition/maximum loan duration\n' \
            '4. Liquidation conditions and Reward\n' \
            '5. Loan duration\n\n' \
            'The lending process delegates the loan terms to standalone smart contracts (see whitepaper below for' \
            ' more details). These loan terms contracts must be deployed, and then “added” or “removed” from the ' \
            'Lending Pool as “available” loan terms for new loans. The DAO will be able to add or remove these term ' \
            'contracts.\n\nLoan term contracts may be created by any interested third party, enabling a market ' \
            'process by which new loan terms may be invented, provided they implement the proper interface.\n\n' \
            f'use `/loans ill001 - ill003` for more details on individual loan contrats\n\n' \
            f'{quote}'
    if loan_type.value == "x7ill001":
        embed.description =\
            f'{items.ill001name}\n\n' \
            f'{items.ill001terms}\n\n' \
            f'[Ethereum]({items.etheraddress}{items.ill001ca})\n' \
            f'[BSC]({items.bscaddress}{items.ill001ca})\n' \
            f'[Polygon]({items.polyaddress}{items.ill001ca})\n' \
            f'[Arbitrum]({items.arbaddress}{items.ill001ca})\n' \
            f'[Optimism]({items.etheraddress}{items.ill001ca})\n\n' \
            f'{quote}'
    if loan_type.value == "x7ill002":
        embed.description = \
            f'{items.ill002name}\n\n' \
            f'{items.ill002terms}\n\n' \
            f'[Ethereum]({items.etheraddress}{items.ill002ca})\n' \
            f'[BSC]({items.bscaddress}{items.ill002ca})\n' \
            f'[Polygon]({items.polyaddress}{items.ill002ca})\n' \
            f'[Arbitrum]({items.arbaddress}{items.ill002ca})\n' \
            f'[Optimism]({items.etheraddress}{items.ill002ca})\n\n' \
            f'{quote}'
    if loan_type.value == "x7ill003":
        embed.description = \
            f'{items.ill003name}\n\n' \
            f'{items.ill003terms}\n\n' \
            f'[Ethereum]({items.etheraddress}{items.ill003ca})\n' \
            f'[BSC]({items.bscaddress}{items.ill003ca})\n' \
            f'[Polygon]({items.polyaddress}{items.ill003ca})\n' \
            f'[Arbitrum]({items.arbaddress}{items.ill003ca})\n' \
            f'[Optimism]({items.etheraddress}{items.ill003ca})\n\n' \
            f'{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Latest X7 Finance Twitter Post")
async def twitter(interaction: discord.Interaction):
    auth = tweepy.OAuthHandler(keys.twitterapi, keys.secret)
    auth.set_access_token(keys.access, keys.accesssecret)
    username = '@x7_finance'
    tweepyclient = tweepy.API(auth)
    tweet = tweepyclient.user_timeline(screen_name=username, count=1)
    embed.description = \
        f'**Latest X7 Finance Tweet**\n\n{tweet[0].text}\n\n' \
        f'{random.choice(items.twitterresp)}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Discount Info")
async def discount(interaction: discord.Interaction):
    embed.description =\
        '**X7 Finance Discount**\n\n' \
        '20 Lucrative X7 Borrowing Incentive NFTs have been minted, granting;\n\n' \
        '50% Origination fee discount\n' \
        '50% Premium fee discount\n\n' \
        'These are a consumable utility NFT offering fee discounts when borrowing funds for initial liquidity on ' \
        'Xchange. The discount will be determined by the X7 Lending Discount Authority smart contract.\n\n' \
        'Usage will cause a token owned by the holder to be burned\n\n' \
        'To apply for a limited NFT see the link below\n\n' \
        ' --------------- \n\n' \
        'There are four mechanisms to receive loan origination and premium discounts:\n\n' \
        '1. Holding the Borrowing Maxi NFT\n' \
        '2. Holding (and having consumed) the Borrowing Incentive NFT\n' \
        '3. Borrowing a greater amount\n' \
        '4. Borrowing for a shorter time\n\n' \
        'All discounts are additive.\n\n' \
        'The NFTs provide a fixed percentage discount. The Borrowing Incentive NFT is consumed upon loan ' \
        'origination.\n\n' \
        'The latter two discounts provide a linear sliding scale, based on the minimum and maximum loan amounts and ' \
        'loan periods. The starting values for these discounts are 0-10% discount.\n\n' \
        'The time based discount is imposing an opportunity cost of lent funds - and incentivizing taking out the ' \
        'shortest loan possible.\n' \
        'The amount based discount is recognizing that a loan origination now is more valuable than a possible loan ' \
        'origination later.\n\nThese sliding scales can be modified to ensure they have optimal market fit.\n\n' \
        f'[Discount Application]({items.dac})\n' \
        f'[X7 Lending Discount Contract]({items.etheraddress}{items.lendingdis}#code)'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Giveaway Info")
async def giveaway(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    then = variables.giveawaytime
    now = datetime.now()
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    if duration < timedelta(0):
        embed.description =\
            f'X7 Finance Giveaway is now closed\n\nPlease check back for more details' \
            f'\n\n{quote}'
    else:
        embed.description =\
            f'*{variables.giveawaytitle}*\n\n' \
            f'X7 Finance Giveaway ends:\n\n{then} (UTC)\n\n' \
            f'%d days, %d hours, %d minutes and %d seconds\n\n' \
            f'{variables.giveawayinfo}' \
            f'\n\n{quote}' \
            % (days[0], hours[0], minutes[0], seconds[0])
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Multichain rollout")
async def snapshot(interaction: discord.Interaction):
    quoteresponse = requests.get(items.quoteapi)
    quotedata = quoteresponse.json()
    quoteraw = (random.choice(quotedata))
    quote = f'`"{quoteraw["text"]}"\n\n-{quoteraw["author"]}`'
    embed.description = \
        f'**X7 Finance NFT Information**\n\nThe rollout of the Ecosystem Contracts on BNB Smart Chain, Polygon ' \
        f'(MATIC), Arbitrum, and Optimism has begun.\n\n' \
        f'In order to deploy the X7 ecosystem more than 30 contracts need to be deployed from unique deployer ' \
        f'addresses per chain. After being deployed many require careful initial configuration. We are moving through' \
        f' a very long checklist and will be double checking these deployments very carefully. Each contract should ' \
        f'have the exact same address on all 5 chains. We expect this may take 1-2 days to fully complete, but do ' \
        f'enjoy watching the on chain progress.\n\nWe will go live with Xchange, borrowing, lending, revenue ' \
        f'splitting, and profit splitting on other chains as soon as we can in concert with the full release on ' \
        f'Ethereum.\n\nThe tokens however will not go live until we have built up a sufficient amount of initial ' \
        f'liquidity for the tokens on any particular chain.\n\nWhen the tokens do go live all X7 token holders on ' \
        f'Ethereum will be airdropped vested tokens and/or be given an opportunity to take a cash payout for their ' \
        f'share of tokens. We will set prices and payouts to ensure that there will be no incentive to exit an ' \
        f'Ethereum X7 Token position in order to gain an "early" L1 or L2 ecosystem X7 token position. On the ' \
        f'contrary, the more tokens held on Ethereum, the greater the reward will be when the tokens and ecosystem ' \
        f'are released on other chains.\n\nThese airdrop snapshots will occur just prior to the token launch\n\n{quote}'
    await interaction.response.send_message(file=thumb, embed=embed)


# MOD COMMANDS
@client.command(pass_context=True)
@commands.has_any_role("Moderators")
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(f"{message}")


@client.command(pass_context=True)
@commands.has_any_role("Moderators")
async def shout(ctx, *, message):
    await ctx.message.delete()
    embed.description = f'GM or GN Wherever you are.\n\n {message}'
    await ctx.send(f"@everyone")
    await ctx.send(file=thumb, embed=embed)


@client.command(pass_context=True)
@commands.has_any_role("Moderators")
async def embedmsg(ctx, *, message):
    await ctx.message.delete()
    embed.description = f'GM or GN Wherever you are.\n\n {message}'
    await ctx.send(file=thumb, embed=embed)


@client.command(pass_context=True)
@commands.has_any_role("Moderators")
async def chain(ctx, *, message, **args):
    await ctx.message.delete()
    link = message.split()[0]
    embed.description = f'**New On Chain Message:**\n\n```{message[91:]}```'
    await ctx.send(f"@everyone\n<{link}>")
    await ctx.send(file=thumb, embed=embed)


@client.command()
async def movemsg(ctx, channel: discord.TextChannel, *message_ids: int):
    for message_id in message_ids:
        message = await ctx.channel.fetch_message(message_id)
        if not message:
            return
        if message.embeds:
            embed = message.embeds[0]
            embed.title = f'Embed by: {message.author}'
        else:
            embed = discord.Embed(
                title=f'Message by: {message.author}',
                description=message.content
            )
        await channel.send(embed=embed)
        await message.delete()


# MESSAGES
@client.event
async def on_error(*args, **kwargs):
    print(f'Unhandled message: {args[0]}\n')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'GM':
        await message.channel.send('GM or GN, Where ever you are!')
    if message.content == 'Trust no one, Trust code ':
        await message.channel.send('Long Live Defi!')
    if message.content == 'Trust no one':
        await message.channel.send('trust code!')
    await client.process_commands(message)


client.run(keys.DISCORD_TOKEN)
