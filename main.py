import discord
from discord.ext import commands, tasks
import tweepy
import items
import keys
import requests
from datetime import datetime, timedelta, timezone
import pytz
from discord import *
from typing import *
import random
import variables
import api

localtime = pytz.timezone("Europe/London")

class PersitentViewBot(commands.Bot):
    def __init__(self):
        self.role = 1016664143220179077
        intents = discord.Intents().all()
        super().__init__(command_prefix=commands.when_mentioned_or('/'), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(Button())

class Button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Agree", emoji="<:x7:1023271910647271584>", style=discord.ButtonStyle.blurple,
                       custom_id="1")
    async def agree(self, interaction: discord.Interaction, button: discord.ui.button):
        if type(client.role) is not discord.Role:
            client.role = interaction.guild.get_role(1016664143220179077)
        if client.role not in interaction.user.roles:
            await interaction.user.add_roles(client.role)
            await interaction.response.send_message("You are now verified!", ephemeral=True)
        else:
            await interaction.response.send_message("You are already verified!", ephemeral=True)


client = PersitentViewBot()
embed = discord.Embed(colour=7419530)
embed.set_footer(text="Trust no one, Trust code. Long live Defi")
thumb = discord.File('X7whitelogo.png')
embed.set_thumbnail(url='attachment://X7whitelogo.png')


@tasks.loop(hours=variables.autotimewp)
async def wp_message():
    mainchannel = client.get_channel(1017887733953347678)
    embed.description = \
        '**X7 Finance Whitepaper Links**\n\n' \
        f'{random.choice(items.quotes)}\n\n' \
        '[Full WP](https://x7.finance/whitepaper)\n' \
        '[Short WP](https://x7community.space/wp-short.pdf)'
    await mainchannel.send(file=thumb, embed=embed)
    print("WP Message Sent")


@client.event
async def on_ready():
    print('Bot is ready')
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
    if not wp_message.is_running():
        wp_message.start()
        print("WP Message Started")


@client.event
async def on_member_join(joinmember):
    joinguild = client.get_guild(1016657044553617428)
    dao = joinguild.get_role(1017420479159607367)
    for joinchannel in joinmember.guild.channels:
        if joinchannel.name.startswith('Members'):
            await joinchannel.edit(name=f'Members: {joinmember.guild.member_count}')
        if joinchannel.name.startswith('DAO Members'):
            await joinchannel.edit(name=f'DAO Members: {len(dao.members)}')


@client.event
async def on_member_leave(leavemember):
    leaveguild = client.get_guild(1016657044553617428)
    dao = leaveguild.get_role(1017420479159607367)
    for leavechannel in leavemember.guild.channels:
        if leavechannel.name.startswith('Members'):
            await leavechannel.edit(name=f'Members: {leavemember.guild.member_count}')
        if leavechannel.name.startswith('DAO Members'):
            await leavechannel.edit(name=f'DAO Members: {len(dao.members)}')


# COMMANDS
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


@client.tree.command(description="X7 NFT Info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def nft(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    if chain.value == "eth":
        embed.description = \
            f'**X7 Finance NFT Information (ETH)**\n\n' \
            f'[**Ecosystem Maxi**]({items.ethertoken}{items.ecoca})\n{items.ecopriceeth}\n' \
            f'Available - {500-int(api.get_holders_nft_eth(items.ecoca))}\n'\
            f'> 25% discount on X7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.ethertoken}{items.liqca})\n{items.liqpriceeth}\n' \
            f'Available - {250-int(api.get_holders_nft_eth(items.liqca))}\n' \
            f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.ethertoken}{items.dexca})\n{items.dexpriceeth}\n' \
            f'Available - {150-int(api.get_holders_nft_eth(items.dexca))}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.ethertoken}{items.borrowca})\n{items.borrowpriceeth}\n' \
            f'Available - {100-int(api.get_holders_nft_eth(items.borrowca))}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.ethertoken}{items.magisterca})\n{items.magisterpriceeth}\n' \
            f'Available - {49 - int(api.get_holders_nft_eth(items.magisterca))}\n'\
            f'> 25% discount on X7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'[**Pioneer**]({items.ethertoken}{items.pioneerca})\n' \
            f' > 6% of profits that come into the X7 Treasury Splitter are now being allocated to the reward ' \
            f'pool. Each X7 Pioneer NFT grants you a proportional share of this pool\n\n' \
            f'https://x7.finance/x/nft/mint\n\n{api.get_quote()}'
    if chain.value == "bsc":
        embed.description = \
            f'**X7 Finance NFT Information (BSC)**\n\n' \
            f'[**Ecosystem Maxi**]({items.bsctoken}{items.ecoca})\n{items.ecopricebsc}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.bsctoken}{items.liqca})\n{items.liqpricebsc}\n' \
            f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.bsctoken}{items.dexca})\n{items.dexpricebsc}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.bsctoken}{items.borrowca})\n{items.borrowpricebsc}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.bsctoken}{items.magisterca})\n{items.magisterpricebsc}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://www.x7finance.org/nfts/\n\n{api.get_quote()}'
    if chain.value == "poly":
        embed.description = \
            f'**X7 Finance NFT Information (POLYGON)**\n\n' \
            f'[**Ecosystem Maxi**]({items.polytoken}{items.ecoca})\n{items.ecopricepoly}\n' \
            f'Available - {500-int(api.get_holders_nft_poly(items.ecoca))}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.polytoken}{items.liqca})\n{items.liqpricepoly}\n' \
            f'Available - {250-int(api.get_holders_nft_poly(items.liqca))}\n' \
            f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.polytoken}{items.dexca})\n{items.dexpricepoly}\n' \
            f'Available - {150-int(api.get_holders_nft_poly(items.dexca))}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.polytoken}{items.borrowca})\n{items.borrowpricepoly}\n' \
            f'Available - {100-int(api.get_holders_nft_poly(items.borrowca))}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.polytoken}{items.magisterca})\n{items.magisterpricepoly}\n'\
            f'Available - {49-int(api.get_holders_nft_poly(items.magisterca))}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://www.x7finance.org/nfts/\n\n{api.get_quote()}'
    if chain.value == "arb":
        embed.description = \
            f'**X7 Finance NFT Information (ARBITRUM)**\n\n' \
            f'[**Ecosystem Maxi**]({items.arbtoken}{items.ecoca})\n{items.ecopricearb}\n' \
            f'Available - {500-int(api.get_holders_nft_arb(items.ecoca))}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.arbtoken}{items.liqca})\n{items.liqpricearb}\n' \
            f'Available - {250-int(api.get_holders_nft_arb(items.liqca))}\n' \
            f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.arbtoken}{items.dexca})\n{items.dexpricearb}\n' \
            f'Available - {150-int(api.get_holders_nft_arb(items.dexca))}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.arbtoken}{items.borrowca})\n{items.borrowpricearb}\n' \
            f'Available - {100-int(api.get_holders_nft_arb(items.borrowca))}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.arbtoken}{items.magisterca})\n{items.magisterpricearb}\n'\
            f'Available - {49-int(api.get_holders_nft_arb(items.magisterca))}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://www.x7finance.org/nfts/\n\n{api.get_quote()}'
    if chain.value == "opti":
        embed.description = \
            f'**X7 Finance NFT Information (OPTIMUM)**\n\n' \
            f'[**Ecosystem Maxi**]({items.optitoken}{items.ecoca})\n{items.ecopriceopti}\n' \
            f'Available - {500-int(api.get_holders_nft_opti(items.ecoca))}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.optitoken}{items.liqca})\n{items.liqpriceopti}\n' \
            f'Available - {250-int(api.get_holders_nft_opti(items.liqca))}\n' \
            f'> 50 % discount on x7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.optitoken}{items.dexca})\n{items.dexpriceopti}\n' \
            f'Available - {150-int(api.get_holders_nft_opti(items.dexca))}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.optitoken}{items.borrowca})\n{items.borrowpriceopti}\n' \
            f'Available - {100-int(api.get_holders_nft_opti(items.borrowca))}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.optitoken}{items.magisterca})\n{items.magisterpriceopti}\n' \
            f'Available - {49-int(api.get_holders_nft_opti(items.magisterca))}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://www.x7finance.org/nfts/\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


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
    embed.description = '**X7 Finance buy links**\n\nUse ``/x7tokenname`` for all other details\n\n' \
                        f'[X7R - Rewards Token]({items.xchangebuy}{items.x7rca})\n' \
                        f'[X7DAO - Governance Token]({items.xchangebuy}{items.x7daoca})\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Chart links")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def chart(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    if chain.value == "eth":
        embed.description = '**X7 Finance Chart links (ETH)**\n\nUse ``/x7tokenname`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dextoolseth}{items.x7rpaireth})\n' \
                            f'[X7DAO - Governance Token]({items.dextoolseth}{items.x7daopaireth})\n\n' \
                            f'{api.get_quote()}'
    if chain.value == "bsc":
        embed.description = '**X7 Finance Chart links (BSC)**\n\nUse ``/x7tokenname`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dextoolsbsc}{items.x7rpairbsc})\n' \
                            f'[X7DAO - Governance Token]({items.dextoolsbsc}{items.x7daopairbsc})\n\n' \
                            f'{api.get_quote()}'
    if chain.value == "poly":
        embed.description = '**X7 Finance Chart links (POLYGON)**\n\nUse ``/x7tokenname`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dextoolspoly}{items.x7rpairpoly})\n' \
                            f'[X7DAO - Governance Token]({items.dextoolspoly}{items.x7daopairpoly})\n\n' \
                            f'{api.get_quote()}'
    if chain.value == "arb":
        embed.description = '**X7 Finance Chart links (ARBITRUM)**\n\nUse ``/x7tokenname`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dextoolsarb}{items.x7rpairarb})\n' \
                            f'[X7DAO - Governance Token]({items.dextoolsarb}{items.x7daopairarb})\n\n' \
                            f'{api.get_quote()}'
    if chain.value == "opti":
        embed.description = '**X7 Finance Chart links (OPTIMISM)**\n\nUse ``/x7tokenname`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dextoolsopti}{items.x7rpairopti})\n' \
                            f'[X7DAO - Governance Token]({items.dextoolsopti}{items.x7daopairopti})\n\n' \
                            f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token contract info")
async def contract(interaction: discord.Interaction):
    embed.description = f'**X7 Finance token contract info**\n\n**X7R**\n`{items.x7rca}`' \
                        f'\n\n**X7DAO**\n`{items.x7daoca}`\n\n' \
                        f'Use `/x7tokenname` for all other details\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="A Guide to buying all constellation tokens evenly")
async def buyevenly(interaction: discord.Interaction):
    embed.description = '**Buy all X7 Finance constellation tokens evenly (ETH)**\n\n' \
                        'Simply connect to https://dapp.x7community.space/constellation via metamask mobile or ' \
                        'desktop and enter your desired Eth amount\n\n' \
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
                        f'9#code)\n[Epoch Convertor](https://www.epochconverter.com/)\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description='X7 Pioneer NFT info')
@app_commands.rename(pioneerid='pioneer-id')
@app_commands.describe(pioneerid='Show Pioneer NFT #')
async def pioneer(interaction: discord.Interaction, pioneerid: Optional[str] = None):
    if not pioneerid:
        data = api.get_nft("/x7-pioneer")
        floor = (data["collection"]["stats"]["floor_price"])
        traits = (data["collection"]["traits"]["Transfer Lock Status"]["unlocked"])
        cap = round(data["collection"]["stats"]["market_cap"], 2)
        sales = (data["collection"]["stats"]["total_sales"])
        owners = (data["collection"]["stats"]["num_owners"])
        avgprice = round(data["collection"]["stats"]["average_price"], 2)
        volume = round(data["collection"]["stats"]["total_volume"], 2)
        pioneerpool = api.get_native_balance(items.pioneerca, "eth")
        totaldollar = float(pioneerpool) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            f'**X7 Pioneer NFT Info**\n\nFloor Price: {floor} ETH (including locked pioneers)\n' \
            f'Average Price: {avgprice} ETH\n' \
            f'Market Cap: {cap} ETH\n' \
            f'Total Volume: {volume} ETH\n' \
            f'Total Sales: {sales}\n' \
            f'Number of Owners: {owners}\n' \
            f'Pioneers Unlocked: {traits}\n' \
            f'Pioneer Pool: {pioneerpool[:3]} ETH (${"{:0,.0f}".format(totaldollar)})\n\n' \
            f'{api.get_quote()}\n\n' \
            f'[X7 Pioneer Dashboard](https://x7.finance/x/nft/pioneer)\n' \
            f'[Opensea](https://opensea.io/collection/x7-pioneer)'
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
    if chain.value == "eth":
        amount = api.get_token_balance(items.dead, "eth", items.x7rca)
        percent = round(amount / items.supply * 100, 2)
        burndollar = api.get_cg_price("x7r")["x7r"]["usd"] * float(amount)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (ETH)**:\n\n' \
            f'{"{:0,.0f}".format(float(amount))} (${"{:0,.0f}".format(burndollar)})\n' \
            f'{percent}% of Supply\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7rca}?a={items.dead})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        amount = api.get_token_balance(items.dead, "bsc", items.x7rca)
        percent = round(((amount / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (BSC)**:\n\n' \
            f'{"{:,}".format(amount)}' \
            f'{percent}% of Supply\n\n' \
            f'[BSCscan]({items.bsctoken}{items.x7rca}?a={items.dead})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        amount = api.get_token_balance(items.dead, "arb", items.x7rca)
        percent = round(((amount / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (ARBITRUM)**:\n\n' \
            f'{"{:,}".format(amount)}' \
            f'{percent}% of Supply\n\n' \
            f'[Arbiscan]({items.arbtoken}{items.x7rca}?a={items.dead})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        amount = api.get_token_balance(items.dead, "opti", items.x7rca)
        percent = round(((amount / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (OPTIMISM)**:\n\n' \
            f'{"{:,}".format(amount)}\n' \
            f'{percent}% of Supply\n\n' \
            f'[Optimism.Etherscan]({items.optitoken}{items.x7rca}?a={items.dead})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        amount = api.get_token_balance(items.dead, "poly", items.x7rca)
        percent = round(((amount / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (POLYGON)**:\n\n' \
            f'{"{:,}".format(amount)}\n' \
            f'{percent}% of Supply\n\n' \
            f'[Polygonscan]({items.polytoken}{items.x7rca}?a={items.dead})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Roadmap Info")
async def roadmap(interaction: discord.Interaction):
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
                        f'5. X7D minting ✅\n' \
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
                        f'> Open sourced testing and development tooling\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Lending Pool info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def pool(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    if chain.value == 'eth':
        ethpool = api.get_native_balance(items.lpreserveca, "eth")
        pooldollar = float(ethpool) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (ETH)**\n\n' \
            f'{ethpool[:5]} ETH (${"{:0,.0f}".format(pooldollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.etheraddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.etheraddress}{items.x7dca})\n\n' \
            f'{api.get_quote()}'
    if chain.value == 'bsc':
        bscpool = api.get_native_balance(items.lpreserveca, "bsc")
        bscpooldollar = float(bscpool) * float(api.get_native_price("bnb")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (BSC)**\n\n' \
            f'{bscpool[:4]} BNB (${"{:0,.0f}".format(bscpooldollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.bscaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.bscaddress}{items.x7dca})\n\n' \
            f'{api.get_quote()}'
    if chain.value == 'poly':
        polypool = api.get_native_balance(items.lpreserveca, "poly")
        polypooldollar = float(polypool) * float(api.get_native_price("matic")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (POLYGON)**\n\n' \
            f'{polypool[:6]} MATIC (${"{:0,.0f}".format(polypooldollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.polyaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.polyaddress}{items.x7dca})\n\n' \
            f'{api.get_quote()}'
    if chain.value == 'arb':
        arbpool = api.get_native_balance(items.lpreserveca, "arb")
        arbpooldollar = float(arbpool) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (ARB)**\n\n' \
            f'{arbpool[:4]} ETH (${"{:0,.0f}".format(arbpooldollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.arbaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.arbaddress}{items.x7dca})\n\n' \
            f'{api.get_quote()}'
    if chain.value == 'opti':
        optipool = api.get_native_balance(items.lpreserveca, "opti")
        optipooldollar = float(optipool) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (OPTIMISM)**\n\n' \
            f'{optipool[:4]}ETH (${"{:0,.0f}".format(optipooldollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.optiaddress}{items.lpreserveca})\n' \
            f'[X7D Contract]({items.optiaddress}{items.x7dca})\n\n' \
            f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token tax info")
async def tax(interaction: discord.Interaction):
    embed.description = f'**X7 Finance Token Tax Info**\n\n' \
                        f'X7R: 6%\nX7DAO: 6%\n' \
                        f'X7101-X7105: 2%\n\n' \
                        f'**Tax with NFTs**\n' \
                        f'Liquidity Maxi:\nX7R: 4.50%\n7DAO: 5.10%\nX7101-X7105: 1.00%\n\n' \
                        f'Ecosystem Maxi:\nX7R: 5.40%\nX7DAO: 5.40%\nX7101-X7105: 1.50%\n\n' \
                        f'Magister:\nX7R: 4.50%\nX7DAO: 6.00%\nX7101-X7105: 1.50%\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Opensea links")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def opensea(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    if chain.value == "eth":
        embed.description = '**X7 Finance Opensea links (ETH)**\n\n' \
                            '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi)\n' \
                            '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi)\n' \
                            '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi)\n' \
                            '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max)\n' \
                            '[Magister](https://opensea.io/collection/x7-magister)\n' \
                            f'[Pioneer](https://opensea.io/collection/x7-pioneer)\n\n{api.get_quote()}'
    if chain.value == "bsc":
        embed.description = '**X7 Finance Opensea links (BSC)**\n\n' \
                            '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi-binance)\n' \
                            '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi-binance)\n' \
                            '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi-binance)\n' \
                            '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max-binance)\n' \
                            f'[Magister](https://opensea.io/collection/x7-magister-binance)\n\n{api.get_quote()}'
    if chain.value == "poly":
        embed.description = '**X7 Finance Opensea links (POLYGON)**\n\n' \
                            '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi-polygon)\n' \
                            '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi-polygon)\n' \
                            '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi-polygon)\n' \
                            '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max-polygon)\n' \
                            f'[Magister](https://opensea.io/collection/x7-magister-polygon)\n\n{api.get_quote()}'
    if chain.value == "arb":
        embed.description = '**X7 Finance Opensea links (ARB)**\n\n' \
                            '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi-arbitrum)\n' \
                            '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi-arbitrum)\n' \
                            '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi-arbitrum)\n' \
                            '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max-arbitrum)\n' \
                            f'[Magister](https://opensea.io/collection/x7-magister-arbitrum)\n\n{api.get_quote()}'
    if chain.value == "opti":
        embed.description = '**X7 Finance Opensea links (OPTI)**\n\n' \
                            '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi-optimism)\n' \
                            '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi-optimism)\n' \
                            '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi-optimism)\n' \
                            '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max-optimism)\n' \
                            f'[Magister](https://opensea.io/collection/x7-magister-optimism)\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Xchange DEX info")
async def swap(interaction: discord.Interaction):

    embed.description = f'**X7 Finance Xchange Info**\n\nhttps://app.x7.finance/#/swap\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Twitter Spaces Info")
async def spaces(interaction: discord.Interaction):
    local_dt = localtime.localize(variables.spacestime, is_dst=None)
    then = local_dt.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    if duration < timedelta(0):
        embed.description = f'X7 Finance Twitter space\n\nPlease check back for more details\n\n{api.get_quote()}'
    else:
        embed.description =\
            f'Next X7 Finance Twitter space is:\n\n{then.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n' \
            f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes\n\n' \
            f'[Click here]({variables.spaceslink}) to set a reminder!' \
            f'\n\n{api.get_quote()}'
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
    embed.description = f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token Holders")
async def holders(interaction: discord.Interaction, view: app_commands.Choice[str]):
    x7daoholders = api.get_holders(items.x7daoca)
    x7rholders = api.get_holders(items.x7rca)
    embed.description = '**X7 Finance Token Holders (ETH)**\n\n' \
                        f'X7R Holders: {x7rholders}\n' \
                        f'X7DAO Holders: {x7daoholders}\n\n' \
                        f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Market Fear Greed Index")
async def fg(interaction: discord.Interaction):
    fearurl = "https://api.alternative.me/fng/?limit=0"
    fearresponse = requests.get(fearurl)
    feardata = fearresponse.json()
    timestamp0 = float(feardata["data"][0]["timestamp"])
    localtime0 = datetime.fromtimestamp(timestamp0)
    timestamp1 = float(feardata["data"][1]["timestamp"])
    localtime1 = datetime.fromtimestamp(timestamp1)
    timestamp2 = float(feardata["data"][2]["timestamp"])
    localtime2 = datetime.fromtimestamp(timestamp2)
    timestamp3 = float(feardata["data"][3]["timestamp"])
    localtime3 = datetime.fromtimestamp(timestamp3)
    timestamp4 = float(feardata["data"][4]["timestamp"])
    localtime4 = datetime.fromtimestamp(timestamp4)
    timestamp5 = float(feardata["data"][5]["timestamp"])
    localtime5 = datetime.fromtimestamp(timestamp5)
    timestamp6 = float(feardata["data"][6]["timestamp"])
    localtime6 = datetime.fromtimestamp(timestamp6)
    duration_in_s = float(feardata["data"][0]["time_until_update"])
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    embed.set_image(url="https://alternative.me/crypto/fear-and-greed-index.png")
    embed.description = \
        f'{feardata["data"][0]["value"]} - {feardata["data"][0]["value_classification"]} - ' \
        f'{localtime0.strftime("%A %B %d")} \n\n' \
        f'Change:\n' \
        f'{feardata["data"][1]["value"]} - {feardata["data"][1]["value_classification"]} - ' \
        f'{localtime1.strftime("%A %B %d")}\n' \
        f'{feardata["data"][2]["value"]} - {feardata["data"][2]["value_classification"]} - ' \
        f'{localtime2.strftime("%A %B %d")}\n' \
        f'{feardata["data"][3]["value"]} - {feardata["data"][3]["value_classification"]} - ' \
        f'{localtime3.strftime("%A %B %d")}\n' \
        f'{feardata["data"][4]["value"]} - {feardata["data"][4]["value_classification"]} - ' \
        f'{localtime4.strftime("%A %B %d")}\n' \
        f'{feardata["data"][5]["value"]} - {feardata["data"][5]["value_classification"]} - ' \
        f'{localtime5.strftime("%A %B %d")}\n' \
        f'{feardata["data"][6]["value"]} - {feardata["data"][6]["value_classification"]} - ' \
        f'{localtime6.strftime("%A %B %d")}\n\n' \
        f'Next Update:\n' \
        f'{int(hours[0])} hours and {int(minutes[0])} minutes\n\n{api.get_quote()}'
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
    if chain.value == "eth":
        supply = api.get_native_balance(items.x7dca, "eth")
        holders = api.get_holders(items.x7dca)
        x7ddollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7D Info (ETH)**\n\n' \
            f'Supply: {supply[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
            f'Holders: {holders}\n\n' \
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
            f'`{api.get_quote()}'
    if chain.value == "bsc":
        supply = api.get_native_balance(items.x7dca, "bnb")
        x7ddollar = float(supply) * float(api.get_native_price("bnb")) / 1 ** 18
        embed.description = \
            '**X7D Info (BSC)**\n\n' \
            f'Supply: {supply[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
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
            f'`{api.get_quote()}'
    if chain.value == "poly":
        supply = api.get_native_balance(items.x7dca, "poly")
        x7ddollar = float(supply) * float(api.get_native_price("matic")) / 1 ** 18
        embed.description = \
            '**X7D Info (POLYGON)**\n\n' \
            f'Supply: {supply[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
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
            f'`{api.get_quote()}'
    if chain.value == "arb":
        supply = api.get_native_balance(items.lpreserveca, "arb")
        x7ddollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7D Info (ETH)**\n\n' \
            f'Supply: {supply[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
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
            f'`{api.get_quote()}'
    if chain.value == "opti":
        supply = api.get_native_balance(items.x7dca, "opti")
        x7ddollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7D Info (OPTIMISM)**\n\n' \
            f'Supply: {supply[:4]}ETH (${"{:0,.0f}".format(x7ddollar)})\n' \
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
            f'`{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Loan Term Info")
@app_commands.choices(terms=[
    app_commands.Choice(name="Full list", value="all"),
    app_commands.Choice(name="1. Simple Loan", value="x7ill001"),
    app_commands.Choice(name="2. Amortizing Loan with interest", value="x7ill002"),
    app_commands.Choice(name="3. Interest Only Loan", value="x7illoo3"),
    ])
async def loans(interaction: discord.Interaction, terms: app_commands.Choice[str]):
    if terms.value == "all":
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
            f'{api.get_quote()}'
    if terms.value == "x7ill001":
        embed.description =\
            f'{items.ill001name}\n\n' \
            f'{items.ill001terms}\n\n' \
            f'[Ethereum]({items.etheraddress}{items.ill001ca})\n' \
            f'[BSC]({items.bscaddress}{items.ill001ca})\n' \
            f'[Polygon]({items.polyaddress}{items.ill001ca})\n' \
            f'[Arbitrum]({items.arbaddress}{items.ill001ca})\n' \
            f'[Optimism]({items.etheraddress}{items.ill001ca})\n\n' \
            f'{api.get_quote()}'
    if terms.value == "x7ill002":
        embed.description = \
            f'{items.ill002name}\n\n' \
            f'{items.ill002terms}\n\n' \
            f'[Ethereum]({items.etheraddress}{items.ill002ca})\n' \
            f'[BSC]({items.bscaddress}{items.ill002ca})\n' \
            f'[Polygon]({items.polyaddress}{items.ill002ca})\n' \
            f'[Arbitrum]({items.arbaddress}{items.ill002ca})\n' \
            f'[Optimism]({items.etheraddress}{items.ill002ca})\n\n' \
            f'{api.get_quote()}'
    if terms.value == "x7ill003":
        embed.description = \
            f'{items.ill003name}\n\n' \
            f'{items.ill003terms}\n\n' \
            f'[Ethereum]({items.etheraddress}{items.ill003ca})\n' \
            f'[BSC]({items.bscaddress}{items.ill003ca})\n' \
            f'[Polygon]({items.polyaddress}{items.ill003ca})\n' \
            f'[Arbitrum]({items.arbaddress}{items.ill003ca})\n' \
            f'[Optimism]({items.etheraddress}{items.ill003ca})\n\n' \
            f'{api.get_quote()}'
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
        f'{random.choice(items.twitterresp)}\n'
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
        f'[X7 Lending Discount Contract]({items.etheraddress}{items.lendingdisca}#code)'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Giveaway Info")
async def giveaway(interaction: discord.Interaction):
    local_dt = localtime.localize(variables.giveawaytime, is_dst=None)
    then = local_dt.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 1)
    if duration < timedelta(0):
        embed.description =\
            f'X7 Finance Giveaway is now closed\n\nPlease check back for more details' \
            f'\n\n{api.get_quote()}'
    else:
        embed.description =\
            f'*{variables.giveawaytitle}*\n\n' \
            f'X7 Finance Giveaway ends:\n\n{then} (UTC)\n\n' \
            f'%d days, %d hours, %d minutes and %d seconds\n\n' \
            f'{variables.giveawayinfo}' \
            f'\n\n{api.get_quote()}' \
            % (days[0], hours[0], minutes[0], seconds[0])
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Multichain Rollout")
async def snapshot(interaction: discord.Interaction):
    embed.description = \
        f'**X7 Finance NFT Information**\n\nThe rollout of the Ecosystem Contracts on BNB Smart Chain, Polygon ' \
        f'(MATIC), Arbitrum, and Optimism has begun.\n\n' \
        f'We will go live with Xchange, borrowing, lending, revenue ' \
        f'splitting, and profit splitting on other chains as soon as we can in concert with the full release on ' \
        f'Ethereum.\n\nThe tokens however will not go live until we have built up a sufficient amount of initial ' \
        f'liquidity for the tokens on any particular chain.\n\nWhen the tokens do go live all X7 token holders on ' \
        f'Ethereum will be airdropped vested tokens and/or be given an opportunity to take a cash payout for their ' \
        f'share of tokens. We will set prices and payouts to ensure that there will be no incentive to exit an ' \
        f'Ethereum X7 Token position in order to gain an "early" L1 or L2 ecosystem X7 token position. On the ' \
        f'contrary, the more tokens held on Ethereum, the greater the reward will be when the tokens and ecosystem ' \
        f'are released on other chains.\n\nThese airdrop snapshots will occur just prior to the token launch\n\n' \
        f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="World Clock")
async def time(interaction: discord.Interaction):
    westcoastraw = pytz.timezone("America/Los_Angeles")
    westcoast = datetime.now(westcoastraw)
    westcoasttime = westcoast.strftime("%I:%M %p")
    eastcoastraw = pytz.timezone("America/New_York")
    eastcoast = datetime.now(eastcoastraw)
    eastcoasttime = eastcoast.strftime("%I:%M %p")
    londonraw = pytz.timezone("Europe/London")
    london = datetime.now(londonraw)
    londontime = london.strftime("%I:%M %p")
    berlinraw = pytz.timezone("Europe/Berlin")
    berlin = datetime.now(berlinraw)
    berlintime = berlin.strftime("%I:%M %p")
    tokyoraw = pytz.timezone("Asia/Tokyo")
    tokyo = datetime.now(tokyoraw)
    tokyotime = tokyo.strftime("%I:%M %p")
    dubairaw = pytz.timezone("Asia/Dubai")
    dubai = datetime.now(dubairaw)
    dubaitime = dubai.strftime("%I:%M %p")
    embed.description = \
        f'UTC: {datetime.now().strftime("%A %B %d %Y")}\n' \
        f'{datetime.now().strftime("%I:%M %p")}\n\n' \
        f'PST: {westcoasttime}\n' \
        f'EST: {eastcoasttime}\n' \
        f'UK: {londontime}\n' \
        f'EU: {berlintime}\n' \
        f'Dubai: {dubaitime}\n' \
        f'Tokyo: {tokyotime}\n'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance FAQ")
async def faq(interaction: discord.Interaction):
    embed.description = \
        "[Constellation Tokens]('https://www.x7finance.org/faq/constellations')" \
        "[Developer Questions]('https://www.x7finance.org/faq/devs')" \
        "[General Questions]('https://www.x7finance.org/faq/general')" \
        "[Governance Questions](https://www.x7finance.org/faq/governance')" \
        "[Investor Questions]('https://www.x7finance.org/faq/investors')" \
        "[Liquidity Lending Questions]('https://www.x7finance.org/faq/liquiditylending')" \
        "[NFT Questions]('https://www.x7finance.org/faq/nfts')" \
        "[Xchange Questions]('https://www.x7finance.org/faq/xchange')"
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Dashboard")
async def dashboard(interaction: discord.Interaction):
    embed.description = \
        "[Constellation Tokens]('https://www.x7finance.org/faq/constellations')" \
        "[Developer Questions]('https://www.x7finance.org/faq/devs')" \
        "[General Questions]('https://www.x7finance.org/faq/general')" \
        "[Governance Questions](https://www.x7finance.org/faq/governance')" \
        "[Investor Questions]('https://www.x7finance.org/faq/investors')" \
        "[Liquidity Lending Questions]('https://www.x7finance.org/faq/liquiditylending')" \
        "[NFT Questions]('https://www.x7finance.org/faq/nfts')" \
        "[Xchange Questions]('https://www.x7finance.org/faq/xchange')"
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Deployer Info")
async def deployer(interaction: discord.Interaction):
    embed.description = \
        '**X7 Finance Deployer**\n\n' \
        'V2: https://etherscan.io/address/0x7000a09c425abf5173ff458df1370c25d1c58105\n\n' \
        'V1 DAO: https://etherscan.io/address/0x7565cE5E02d368BB3aEC044b7C3398911E27dB1E\n\n' \
        'V1 Protocol https://etherscan.io/address/0x8FE821FB171076B850A3048B9AAD7600BE8d0F30'
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="On this day in history")
async def today(interaction: discord.Interaction):
    data = api.get_today()
    today = (random.choice(data["data"]["Events"]))
    embed.description = \
        f'`On this day in {today["year"]}:\n\n{today["text"]}`',
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="X7 Finance Voting Infi=o")
async def voting(interaction: discord.Interaction):
    embed.description = \
        '**Proposals and Voting**\n\nVoting will occur in multiple phases, each of which has either a minimum or ' \
        'maximum time phase duration.\n\n*Phase 1: Quorum-seeking*\nX7DAO token holders will be able to stake ' \
        'their tokens as X7sDAO, a non-transferrable staked version of X7DAO.\n\nA quorum is reached when more ' \
        'than 50% of circulating X7DAO has been staked as X7sDAO.\n\nOnce a quorum is reached and a minimum ' \
        'quorum-seeking time period has passed, the X7sDAO tokens are temporarily locked (and no more X7DAO tokens ' \
        'may be staked until the next Quorum seeking period) and the governance process moves to the next phase\n\n' \
        '**Phase 2: Proposal creation**\n A proposal is created by running a transaction on the governance contract ' \
        'which specifies a specific transaction on a specific contract (e.g. setFeeNumerator(0) on the X7R token ' \
        'contract).\n\nProposals are ordered, and any proposals that are passed/adopted must be run in the order ' \
        'that they were created.\n\nProposals can be made by X7sDAO stakes of 500,000 tokens or more. Additionally, ' \
        'holders of Magister tokens may make proposals. Proposals may require a refundable proposal fee to prevent ' \
        'process griefing.\n\n**Phase 3: Proposal voting**\n Each proposal may be voted on once by each address. ' \
        'The voter may specify the weight of their vote between 0 and the total amount of X7sDAO they have ' \
        'staked.\n\nProposals pass by a majority vote of the quorum of X7sDAO tokens.\n\nA parallel voting process ' \
        'will occur with Magister tokens, where each Magister token carries ' \
        'one vote.\n\nIf a majority of magister token holders vote against a proposal, the proposal must ' \
        'reach an X7sDAO vote of 75% of the quorum of X7sDAO tokens.\n\n*Phase 4: Proposal adoption*\nDuring this ' \
        'phase, proposals that have passed will be enqueued for execution. This step ensures proper ordering and is ' \
        'a guard against various forms of process griefing.\n\n*Phase 5: Proposal execution*\nAfter proposal ' \
        'adoption, all passed proposals must be executed before a new Quorum Seeking phase may commence.\n\n' \
        '{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="Market Gas Info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance Smart Chain", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    ])
async def gas(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    if chain.value == "eth":
        gasdata = api.get_gas("eth")
        embed.description = \
            f'**Eth Gas Prices:**\n' \
            f'Low: {gasdata["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gasdata["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gasdata["result"]["FastGasPrice"]} Gwei\n\n' \
            f'{api.get_quote()}'
    if chain.value == "bsc":
        gasdata = api.get_gas("bsc")
        embed.description = \
            f'**BSC Gas Prices:**\n' \
            f'For other chains use `/gas [chain-name]`\n\n' \
            f'Low: {gasdata["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gasdata["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gasdata["result"]["FastGasPrice"]} Gwei\n\n' \
            f'{api.get_quote()}'
    if chain.value == "poly":
        gasdata = api.get_gas("poly")
        embed.description = \
            f'**POLYGON Gas Prices:**\n' \
            f'For other chains use `/gas [chain-name]`\n\n' \
            f'Low: {gasdata["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gasdata["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gasdata["result"]["FastGasPrice"]} Gwei\n\n' \
            f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="Wei conversion")
@app_commands.describe(eth='amount to convert')
async def wei(interaction: discord.Interaction, eth: Optional[str] = ""):
    weiraw = float(eth)
    wei = weiraw * 10 ** 18
    embed.description = \
        f'{eth} ETH is equal to \n\n' \
        f'`{wei:.0f}` wei' \
        f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="X7 Finance Alumni")
async def alumni(interaction: discord.Interaction):
    embed.description = \
        f'**X7 Finance Alumni**\n\n' \
        f'@Callmelandlord - The Godfather of the X7 Finance community, the OG, the creator - X7 God\n\n' \
        f'@WoxieX - Creator of the OG dashboard -  x7community.space\n\n' \
        f'@Zaratustra  - Defi extraordinaire and protocol prophet\n\n' \
        f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)

# CG COMMANDS
@client.tree.command(description="X7DAO Info")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def x7dao(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    price = api.get_cg_price("x7dao")
    if price["x7dao"]["usd_24h_change"] is None:
        price["x7dao"]["usd_24h_change"] = 0
    if chain.value == "eth":
        holders = api.get_holders(items.x7daoca)
        x7daoliq = api.get_liquidity(items.x7daopaireth)
        x7daotoken = float(x7daoliq["reserve0"])
        x7daoweth = float(x7daoliq["reserve1"]) / 10 ** 18
        x7daowethdollar = float(x7daoweth) * float(api.get_native_price("eth"))
        x7daotokendollar = float(price["x7dao"]["usd"]) * float(x7daotoken) / 10 ** 18
        embed.description =\
            f'**X7DAO (ETH) Info**\n\n' \
            f'X7DAO Price: ${price["x7dao"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"],1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7dao"]["usd"]*items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7dao"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Liquidity:\n' \
            f'{"{:0,.0f}".format(x7daotoken)[:4]}M X7DAO (${"{:0,.0f}".format(x7daotokendollar)})\n' \
            f'{x7daoweth[:5]} WETH (${"{:0,.0f}".format(x7daowethdollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(x7daowethdollar + x7daotokendollar)})\n\n' \
            f'Contract Address:\n`{items.x7daoca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7daoca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7daopaireth})\n' \
            f'[Buy]({items.xchangebuy}{items.x7daoca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description =\
            f'**X7DAO (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7daoca}`\n\n' \
            f'[BSCscan]({items.bsctoken}{items.x7daoca})\n' \
            f'[Chart]({items.dextoolsbsc}{items.x7daopairbsc})\n' \
            f'[Buy]({items.xchangebuy}{items.x7daoca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description =\
            f'**X7DAO (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7daoca}`\n\n' \
            f'[Polygonscan]({items.polytoken}{items.x7daoca})\n' \
            f'[Chart]({items.dextoolspoly}{items.x7daopairpoly})\n' \
            f'[Buy]({items.xchangebuy}{items.x7daoca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7DAO (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7daoca}`\n\n' \
            f'[Arbiscan]({items.arbtoken}{items.x7daoca})\n' \
            f'[Chart]({items.dextoolsarb}{items.x7daopairarb})\n' \
            f'[Buy]({items.xchangebuy}{items.x7daoca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description =\
            f'**X7DAO (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7daoca}`\n\n' \
            f'[Optimistic.etherscan]({items.optitoken}{items.x7daoca})\n' \
            f'[Chart]({items.dextoolsopti}{items.x7daopairopti})\n' \
            f'[Buy]({items.xchangebuy}{items.x7daoca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7R Info')
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def x7r(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    price = api.get_cg_price("x7r")
    if price["x7r"]["usd_24h_change"] is None:
        price["x7r"]["usd_24h_change"] = 0
    if chain.value == "eth":
        holders = api.get_holders(items.x7rca)
        x7rburn = api.get_token_balance(items.dead, "eth", items.x7rca)
        percent = round(((x7rburn / items.supply) * 100), 6)
        x7rliq = api.get_liquidity(items.x7rpaireth)
        x7rtoken = float(x7rliq["reserve0"])
        x7rweth = float(x7rliq["reserve1"]) / 10 ** 18
        x7rwethdollar = float(x7rweth) * float(api.get_native_price("eth"))
        x7rtokendollar = float(price["x7r"]["usd"]) * float(x7rtoken) / 10 ** 18
        embed.description =\
            f'**X7R (ETH) Info**\n\n' \
            f'X7R Price: ${price["x7r"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7dao"]["usd"]*items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7r"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'X7R Tokens Burned:\n' \
            f'{"{:,}".format(burn)}\n' \
            f'{percent}% of Supply\n\n' \
            f'Liquidity:\n' \
            f'{"{:0,.0f}".format(x7rtoken)[:4]}M X7R (${"{:0,.0f}".format(x7rtokendollar)})\n' \
            f'{x7rweth[:6]} WETH (${"{:0,.0f}".format(x7rwethdollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(x7rwethdollar + x7rtokendollar)})\n\n' \
            f'Contract Address:\n`{items.x7rca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7rca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7rpaireth})\n' \
            f'[Buy]({items.xchangebuy}{items.x7rca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description =\
            f'**X7R (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7rca}\n\n`' \
            f'[BSCscan]({items.bsctoken}{items.x7rca})\n' \
            f'[Chart]({items.dextoolsbsc}{items.x7rpairbsc})\n' \
            f'[Buy]({items.xchangebuy}{items.x7rca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description =\
            f'**X7R (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7rca}\n\n`' \
            f'[Polygonscan]({items.polytoken}{items.x7rca})\n' \
            f'[Chart]({items.dextoolspoly}{items.x7rpairpoly})\n' \
            f'[Buy]({items.xchangebuy}{items.x7rca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7R (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7rca}\n\n`' \
            f'[Arbiscan]({items.arbtoken}{items.x7rca})\n' \
            f'[Chart]({items.dextoolsarb}{items.x7rpairarb})\n' \
            f'[Buy]({items.xchangebuy}{items.x7rca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description =\
            f'**X7R (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7rca}\n\n`' \
            f'[Optimistic.etherscan]({items.optitoken}{items.x7rca})\n' \
            f'[Chart]({items.dextoolsopti}{items.x7rpairopti})\n' \
            f'[Buy]({items.xchangebuy}{items.x7rca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)

@client.tree.command(description='X7101 Info')
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    app_commands.Choice(name="Image", value="img"),
    ])
async def x7101(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    price = api.get_cg_price("x7101")
    if price["x7101"]["usd_24h_change"] is None:
        price["x7101"]["usd_24h_change"] = 0
    if chain.value == "eth":
        holders = api.get_holders(items.x7101ca)
        embed.description =\
            f'**X7101 (ETH) Info**\n\n' \
            f'X7101 Price: ${price["x7101"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7101"]["usd"] * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7101"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7101ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7101ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7101paireth})\n' \
            f'[Buy]({items.xchangebuy}{items.x7101ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description =\
            f'**X7101 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7101ca}`\n\n' \
            f'[BSCscan]({items.bsctoken}{items.x7101ca})\n' \
            f'[Chart]({items.dextoolsbsc}{items.x7101pairbsc})\n' \
            f'[Buy]({items.xchangebuy}{items.x7101ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description =\
            f'**X7101 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7101ca}`\n\n' \
            f'[Polygonscan]({items.polytoken}{items.x7101ca})\n' \
            f'[Chart]({items.dextoolspoly}{items.x7101pairpoly})\n' \
            f'[Buy]({items.xchangebuy}{items.x7101ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7101 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7101ca}`\n\n' \
            f'[Arbiscan]({items.arbtoken}{items.x7101ca})\n' \
            f'[Chart]({items.dextoolsarb}{items.x7101pairarb})\n' \
            f'[Buy]({items.xchangebuy}{items.x7101ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7101 (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7101ca}`\n\n' \
            f'[Optimistic.etherscan]({items.optitoken}{items.x7101ca})\n' \
            f'[Chart]({items.dextoolsopti}{items.x7101pairopti})\n' \
            f'[Buy]({items.xchangebuy}{items.x7101ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)

@client.tree.command(description='X7102 Info')
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def x7102(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    price = api.get_cg_price("x7102")
    if price["x7102"]["usd_24h_change"] is None:
        price["x7102"]["usd_24h_change"] = 0
    if chain.value == "eth":
        holders = api.get_holders(items.x7102ca)
        embed.description = \
            f'**X7102 (ETH) Info**\n\n' \
            f'X7102 Price: ${price["x7102"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7102"]["usd"]*items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7102"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7102ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7102ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7102paireth})\n' \
            f'[Buy]({items.xchangebuy}{items.x7102ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description = \
            f'**X7102 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7102ca}`\n\n' \
            f'[BSCscan]({items.bsctoken}{items.x7102ca})\n' \
            f'[Chart]({items.dextoolsbsc}{items.x7102pairbsc})\n' \
            f'[Buy]({items.xchangebuy}{items.x7102ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description = \
            f'**X7102 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7102ca}`\n\n' \
            f'[Polygonscan]({items.polytoken}{items.x7102ca})\n' \
            f'[Chart]({items.dextoolspoly}{items.x7102pairpoly})\n' \
            f'[Buy]({items.xchangebuy}{items.x7102ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description = \
            f'**X7102 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7102ca}`\n\n' \
            f'[Arbiscan]({items.arbtoken}{items.x7102ca})\n' \
            f'[Chart]({items.dextoolsarb}{items.x7102pairarb})\n' \
            f'[Buy]({items.xchangebuy}{items.x7102ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description = \
            f'**X7102 (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7102ca}`\n\n' \
            f'[Optimistic.etherscan]({items.optitoken}{items.x7102ca})\n' \
            f'[Chart]({items.dextoolsopti}{items.x7102pairopti})\n' \
            f'[Buy]({items.xchangebuy}{items.x7102ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7103 Info')
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    app_commands.Choice(name="Image", value="img"),
    ])
async def x7103(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    price = api.get_cg_price("x7103")
    if price["x7103"]["usd_24h_change"] is None:
        price["x7103"]["usd_24h_change"] = 0
    if chain.value == "eth":
        holders = api.get_holders(items.x7103ca)
        embed.description = \
            f'**X7103 (ETH) Info**\n\n' \
            f'X7103 Price: ${price["x7103"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7103"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7103"]["usd"] * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7103"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7103ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7103ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7103paireth})\n' \
            f'[Buy]({items.xchangebuy}{items.x7103ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description = \
            f'**X7103 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7103ca}`\n\n' \
            f'[BSCscan]({items.bsctoken}{items.x7103ca})\n' \
            f'[Chart]({items.dextoolsbsc}{items.x7103pairbsc})\n' \
            f'[Buy]({items.xchangebuy}{items.x7103ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description = \
            f'**X7103 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7103ca}`\n\n' \
            f'[Polgonscan]({items.polytoken}{items.x7103ca})\n' \
            f'[Chart]({items.dextoolspoly}{items.x7103pairpoly})\n' \
            f'[Buy]({items.xchangebuy}{items.x7103ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description = \
            f'**X7103 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7103ca}`\n\n' \
            f'[Arbiscan]({items.arbtoken}{items.x7103ca})\n' \
            f'[Chart]({items.dextoolsarb}{items.x7103pairarb})\n' \
            f'[Buy]({items.xchangebuy}{items.x7103ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description = \
            f'**X7103 (OPTMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7103ca}`\n\n' \
            f'[Optimistic.etherscan]({items.optitoken}{items.x7103ca})\n' \
            f'[Chart]({items.dextoolsopti}{items.x7103pairopti})\n' \
            f'[Buy]({items.xchangebuy}{items.x7103ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)

@client.tree.command(description='X7104 Info')
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def x7104(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    price = api.get_cg_price("x7104")
    if price["x7104"]["usd_24h_change"] is None:
        price["x7104"]["usd_24h_change"] = 0
    if chain.value == "eth":
        holders = api.get_holders(items.x7104ca)
        embed.description = \
            f'**X7104 (ETH) Info**\n\n' \
            f'X7104 Price: ${price["x7104"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7104"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7104"]["usd"] * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7104"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7104ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7104ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7104paireth})\n' \
            f'[Buy]({items.xchangebuy}{items.x7104ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description =\
            f'**X7104 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7104ca}`\n\n' \
            f'[BSCscan]({items.bsctoken}{items.x7104ca})\n' \
            f'[Chart]({items.dextoolsbsc}{items.x7104pairbsc})\n' \
            f'[Buy]({items.xchangebuy}{items.x7104ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description =\
            f'**X7104 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7104ca}`\n\n' \
            f'[Polygonscan]({items.polytoken}{items.x7104ca})\n' \
            f'[Chart]({items.dextoolspoly}{items.x7104pairpoly})\n' \
            f'[Buy]({items.xchangebuy}{items.x7104ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7104 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7104ca}`\n\n' \
            f'[Arbiscan]({items.arbtoken}{items.x7104ca})\n' \
            f'[Chart]({items.dextoolsarb}{items.x7104pairarb})\n' \
            f'[Buy]({items.xchangebuy}{items.x7104ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description =\
            f'**X7104 (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7104ca}`\n\n' \
            f'[Optimistic.etherscan]({items.optitoken}{items.x7104ca})\n' \
            f'[Chart]({items.dextoolsopti}{items.x7104pairopti})\n' \
            f'[Buy]({items.xchangebuy}{items.x7104ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description='X7105 Info')
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def x7105(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    price = api.get_cg_price("x7105")
    if price["x7105"]["usd_24h_change"] is None:
        price["x7105"]["usd_24h_change"] = 0
    if chain.value == "eth":
        holders = api.get_holders(items.x7105ca)
        embed.description = \
            f'**X7105 (ETH) Info**\n\n' \
            f'X7105 Price: ${price["x7105"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7105"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7105"]["usd"] * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7105"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7105ca}`\n\n' \
            f'[Etherscan]({items.ethertoken}{items.x7105ca})\n' \
            f'[Chart]({items.dextoolseth}{items.x7105paireth})\n' \
            f'[Buy]({items.xchangebuy}{items.x7105ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description = \
            f'**X7105 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7105ca}`\n\n' \
            f'[BSCscan]({items.bsctoken}{items.x7105ca})\n' \
            f'[Chart]({items.dextoolsbsc}{items.x7105pairbsc})\n' \
            f'[Buy]({items.xchangebuy}{items.x7105ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description = \
            f'**X7105 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7105ca}`\n\n' \
            f'[Polygonscan]({items.polytoken}{items.x7105ca})\n' \
            f'[Chart]({items.dextoolspoly}{items.x7105pairpoly})\n' \
            f'[Buy]({items.xchangebuy}{items.x7105ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description = \
            f'**X7105 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7105ca}`\n\n' \
            f'[Arbiscan]({items.arbtoken}{items.x7105ca})\n' \
            f'[Chart]({items.dextoolsarb}{items.x7105pairarb})\n' \
            f'[Buy]({items.xchangebuy}{items.x7105ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description = \
            f'**X7105 (AOPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7105ca}`\n\n' \
            f'[Optimistic.etherscan]({items.optitoken}{items.x7105ca})\n' \
            f'[Chart]({items.dextoolsopti}{items.x7105pairopti})\n' \
            f'[Buy]({items.xchangebuy}{items.x7105ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)

@client.tree.command(description='Constellation Info')
async def constellations(interaction: discord.Interaction):
    price = api.get_cg_price("x7101, x7102, x7103, x7104, x7105")
    x7101mc = price["x7101"]["usd"] * items.supply
    x7102mc = price["x7102"]["usd"] * items.supply
    x7103mc = price["x7103"]["usd"] * items.supply
    x7104mc = price["x7104"]["usd"] * items.supply
    x7105mc = price["x7105"]["usd"] * items.supply
    constmc = x7101mc + x7102mc + x7103mc + x7104mc + x7105mc
    if price["x7101"]["usd_24h_change"] is None:
        price["x7101"]["usd_24h_change"] = 0
    if price["x7102"]["usd_24h_change"] is None:
        price["x7102"]["usd_24h_change"] = 0
    if price["x7103"]["usd_24h_change"] is None:
        price["x7103"]["usd_24h_change"] = 0
    if price["x7104"]["usd_24h_change"] is None:
        price["x7104"]["usd_24h_change"] = 0
    if price["x7105"]["usd_24h_change"] is None:
        price["x7105"]["usd_24h_change"] = 0
    embed.description = \
        f'**X7 Finance Constellation Token Prices (ETH)**\n\n' \
        f'For more info use `/x7tokenname`\n\n' \
        f'X7101:      ${price["x7101"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7101"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7101mc)}\n' \
        f'CA: `{items.x7101ca}`\n\n' \
        f'X7102:      ${price["x7102"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7102"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7102mc)}\n' \
        f'CA: `{items.x7102ca}`\n\n' \
        f'X7103:      ${price["x7103"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7103"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7103mc)}\n' \
        f'CA: `{items.x7103ca}`\n\n' \
        f'X7104:      ${price["x7104"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7104"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7104mc)}\n' \
        f'CA: `{items.x7104ca}`\n\n' \
        f'X7105:      ${price["x7105"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7105"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7105mc)}\n' \
        f'CA: `{items.x7105ca}`\n\n' \
        f'Combined Market Cap: ${"{:0,.0f}".format(constmc)}\n\n' \
        f'{api.get_quote()}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description="Market Cap Info")
@app_commands.choices(view=[
    app_commands.Choice(name="Text", value="text"),
    app_commands.Choice(name="Image", value="img"),
    ])
async def mcap(interaction: discord.Interaction, view: app_commands.Choice[str]):
    x7rsupply = items.supply - api.get_token_balance(items.dead, "eth", items.x7rca)
    price = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    x7rcap = (price["x7r"]["usd"]) * x7rsupply
    x7daocap = (price["x7dao"]["usd"]) * items.supply
    x7101cap = (price["x7101"]["usd"]) * items.supply
    x7102cap = (price["x7102"]["usd"]) * items.supply
    x7103cap = (price["x7103"]["usd"]) * items.supply
    x7104cap = (price["x7104"]["usd"]) * items.supply
    x7105cap = (price["x7105"]["usd"]) * items.supply
    conscap = x7101cap + x7102cap + x7103cap + x7104cap + x7105cap
    totalcap = x7rcap + x7daocap + x7101cap + x7102cap + x7103cap + x7104cap + x7105cap
    if view.value == "text":
        embed.description = \
            f'**X7 Finance Market Cap Info (ETH)**\n\n' \
            f'X7R:          ${"{:0,.0f}".format(x7rcap)}\n' \
            f'X7DAO:     ${"{:0,.0f}".format(x7daocap)}\n' \
            f'X7101:       ${"{:0,.0f}".format(x7101cap)}\n' \
            f'X7102:       ${"{:0,.0f}".format(x7102cap)}\n' \
            f'X7103:       ${"{:0,.0f}".format(x7103cap)}\n' \
            f'X7104:       ${"{:0,.0f}".format(x7104cap)}\n' \
            f'X7105:       ${"{:0,.0f}".format(x7105cap)}\n\n' \
            f'Constellations Combined: ' \
            f'${"{:0,.0f}".format(x7101cap + x7102cap + x7103cap + x7104cap + x7105cap)}\n' \
            f'Total Token Marketcap:\n' \
            f'    ${"{:0,.0f}".format(totalcap)}' \
            f'\n\n{api.get_quote()}'
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
    if chain.value == 'eth':
        deveth = api.get_native_balance(items.devmultieth, "eth")
        cometh = api.get_native_balance(items.commultieth, "eth")
        pioneereth = api.get_native_balance(items.pioneerca, "eth")
        devdollar = float(deveth) * float(api.get_native_price("eth")) / 1 ** 18
        comdollar = float(cometh) * float(api.get_native_price("eth")) / 1 ** 18
        pioneerdollar = float(pioneereth) * float(api.get_native_price("eth")) / 1 ** 18
        comx7r = api.get_token_balance(items.commultieth, "eth", items.x7rca)
        comx7rprice = comx7r * api.get_cg_price("x7r")["x7r"]["usd"]
        comx7d = api.get_token_balance(items.commultieth, "eth", items.x7dca)
        comx7dprice = comx7d * api.get_native_price("eth")
        comtotal = comx7rprice + comdollar + comx7dprice
        embed.description = \
            f'**X7 Finance Treasury Info (ETH)**\n\n' \
            f'Pioneer Pool:\n{pioneereth[:4]}ETH (${"{:0,.0f}".format(pioneerdollar)})\n\n' \
            f'[Developer Wallet:]({items.etheraddress}{items.devmultieth})\n' \
            f'{deveth[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'[Community Wallet:]({items.etheraddress}{items.commultieth})\n' \
            f'{cometh[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n' \
            f'{comx7r} X7R (${"{:0,.0f}".format(comx7rprice)})\n' \
            f'{comx7d} X7D (${"{:0,.0f}".format(comx7dprice)})\n' \
            f'Total: (${"{:0,.0f}".format(comtotal)})\n\n' \
            f'[Treasury Splitter Contract]({items.etheraddress}{items.tsplitterca})\n\n' \
            f'{api.get_quote()}'
    if chain.value == "bsc":
        deveth = api.get_native_balance(items.devmultibsc, "bsc")
        cometh = api.get_native_balance(items.commultibsc, "bsc")
        devdollar = float(deveth) * float(api.get_native_price("bnb")) / 1 ** 18
        comdollar = float(cometh) * float(api.get_native_price("bnb")) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (BSC)**\n\n' \
            f'Developer Wallet:\n{deveth[:4]}BNB (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'Community Wallet:\n{cometh[:4]}BNB (${"{:0,.0f}".format(comdollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.bscaddress}{items.tsplitterca})\n\n{api.get_quote()}'
    if chain.value == "arb":
        deveth = api.get_native_balance(items.devmultiarb, "arb")
        cometh = api.get_native_balance(items.devmultiarb, "arb")
        devdollar = float(deveth) * float(api.get_native_price("eth")) / 1 ** 18
        comdollar = float(cometh) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (ARB)**\n\n' \
            f'Developer Wallet:\n{deveth[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'Community Wallet:\n{cometh[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.arbaddress}{items.tsplitterca})\n\n{api.get_quote()}'
    if chain.value == "opti":
        deveth = api.get_native_balance(items.devmultiopti, "opti")
        cometh = api.get_native_balance(items.commultiopti, "opti")
        devdollar = float(deveth) * float(api.get_native_price("eth")) / 1 ** 18
        comdollar = float(cometh) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (OPTIMISM)**\n\n' \
            f'Developer Wallet:\n{deveth[:4]}ETH (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'Community Wallet:\n{cometh[:4]}ETH (${"{:0,.0f}".format(comdollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.optiaddress}{items.tsplitterca})\n\n{api.get_quote()}'
    if chain.value == "poly":
        deveth = api.get_native_balance(items.devmultipoly, "poly")
        cometh = api.get_native_balance(items.commultipoly, "poly")
        devdollar = float(deveth) * float(api.get_native_price("matic")) / 1 ** 18
        comdollar = float(cometh) * float(api.get_native_price("matic")) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (POLYGON)**\n\n' \
            f'Developer Wallet:\n{deveth[:4]}MATIC (${"{:0,.0f}".format(devdollar)})\n\n' \
            f'Community Wallet:\n{cometh[:4]}MATIC (${"{:0,.0f}".format(comdollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.polyaddress}{items.tsplitterca})\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token price info")
@app_commands.describe(coin='Coin Name')
async def price(interaction: discord.Interaction, coin: Optional[str] = ""):
    token = api.get_cg_search(coin)
    tokenid = token["coins"][0]["api_symbol"]
    tokenlogo = token["coins"][0]["thumb"]
    symbol = token["coins"][0]["symbol"]
    tokenprice = api.get_cg_price(tokenid)
    if coin == "":
        price = api.get_cg_price("x7r, x7dao")
        embed.description = f'**X7 Finance Token Prices  (ETH)**\n\n' \
                            f'X7R:      ${price["x7r"]["usd"]}\n' \
                            f'24 Hour Change: {round(price["x7r"]["usd_24h_change"], 1)}%\n\n' \
                            f'X7DAO:  ${price["x7dao"]["usd"]}\n' \
                            f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"], 0)}%\n\n' \
                            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if coin == "eth":
        eth = api.get_cg_price("ethereum")
        gasdata = api.get_gas("eth")
        ethembed = discord.Embed(colour=7419530)
        ethembed.set_footer(text="Trust no one, Trust code. Long live Defi")
        ethembed.set_thumbnail(url=tokenlogo)
        ethembed.description = \
            f'**{symbol} price**\n\n' \
            f'Eth Price:\n${eth["result"]["ethusd"]}\n' \
            f'24 Hour Change: {round(eth["ethereum"]["usd_24h_change"], 1)}%\n\n' \
            f'Gas Prices:\n' \
            f'Low: {gasdata["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gasdata["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gasdata["result"]["FastGasPrice"]} Gwei\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=ethembed)
    if coin == "bnb":
        bnb = api.get_cg_price("binancecoin")
        gasdata = api.get_gas("bsc")
        bnbembed = discord.Embed(colour=7419530)
        bnbembed.set_footer(text="Trust no one, Trust code. Long live Defi")
        bnbembed.set_thumbnail(url=tokenlogo)
        bnbembed.description = \
            f'**{symbol} price**\n\n' \
            f'Price: ${bnb["binancecoin"]["usd"]}\n' \
            f'24 Hour Change: {round(bnb["binancecoin"]["usd_24h_change"], 1)}%\n\n' \
            f'Gas Prices:\n' \
            f'Low: {gasdata["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gasdata["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gasdata["result"]["FastGasPrice"]} Gwei\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=bnbembed)
        return
    if coin == "matic" or coin == "poly" or coin == "polygon":
        matic = api.get_cg_price("matic-network")
        gasdata = api.get_gas("poly")
        polyembed = discord.Embed(colour=7419530)
        polyembed.set_footer(text="Trust no one, Trust code. Long live Defi")
        polyembed.set_thumbnail(url=tokenlogo)
        polyembed.description = \
            f'**{symbol} price**\n\n' \
            f'Price: ${matic["matic-network"]["usd"]}\n' \
            f'24 Hour Change: {round(matic["matic-network"]["usd_24h_change"], 1)}%\n\n' \
            f'Gas Prices:\n' \
            f'Low: {gasdata["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gasdata["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gasdata["result"]["FastGasPrice"]} Gwei\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(embed=polyembed)
        return
    else:
        tokenembed = discord.Embed(colour=7419530)
        tokenembed.set_footer(text="Trust no one, Trust code. Long live Defi")
        tokenembed.set_thumbnail(url=tokenlogo)
        tokenembed.description = \
            f'**{symbol} price**\n\n' \
            f'Price:      ${"{:f}".format(float(tokenprice[tokenid]["usd"]))}\n' \
            f'24 Hour Change: {round(tokenprice[tokenid]["usd_24h_change"], 1)}%\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(embed=tokenembed)


@client.tree.command(description="X7 Token Liquidity")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    app_commands.Choice(name="Optimism", value="opti"),
    ])
async def liquidity(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    if chain.value == "eth":
        price = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
        x7rprice = (price["x7r"]["usd"])
        x7daoprice = (price["x7dao"]["usd"])
        x7101price = (price["x7101"]["usd"])
        x7102price = (price["x7102"]["usd"])
        x7103price = (price["x7103"]["usd"])
        x7104price = (price["x7104"]["usd"])
        x7105price = (price["x7105"]["usd"])
        x7rliq = api.get_liquidity(items.x7rpaireth)
        x7daoliq = api.get_liquidity(items.x7daopaireth)
        x7101liq = api.get_liquidity(items.x7101paireth)
        x7102liq = api.get_liquidity(items.x7102paireth)
        x7103liq = api.get_liquidity(items.x7103paireth)
        x7104liq = api.get_liquidity(items.x7104paireth)
        x7105liq = api.get_liquidity(items.x7105paireth)
        x7rtoken = float(x7rliq["reserve0"])
        x7rweth = float(x7rliq["reserve1"]) / 10 ** 18
        x7rwethdollar = float(x7rweth) * float(api.get_native_price("eth"))
        x7rtokendollar = float(x7rprice) * float(x7rtoken) / 10 ** 18
        x7daotoken = float(x7daoliq["reserve0"])
        x7daoweth = float(x7daoliq["reserve1"]) / 10 ** 18
        x7daowethdollar = float(x7daoweth) * float(api.get_native_price("eth"))
        x7daotokendollar = float(x7daoprice) * float(x7daotoken) / 10 ** 18
        x7101token = float(x7101liq["reserve0"])
        x7101weth = float(x7101liq["reserve1"]) / 10 ** 18
        x7101wethdollar = float(x7101weth) * float(api.get_native_price("eth"))
        x7101tokendollar = float(x7101price) * float(x7101token) / 10 ** 18
        x7102token = float(x7102liq["reserve0"])
        x7102weth = float(x7102liq["reserve1"]) / 10 ** 18
        x7102wethdollar = float(x7102weth) * float(api.get_native_price("eth"))
        x7102tokendollar = float(x7102price) * float(x7102token) / 10 ** 18
        x7103token = float(x7103liq["reserve0"])
        x7103weth = float(x7103liq["reserve1"]) / 10 ** 18
        x7103wethdollar = float(x7103weth) * float(api.get_native_price("eth"))
        x7103tokendollar = float(x7103price) * float(x7103token) / 10 ** 18
        x7104token = float(x7104liq["reserve0"])
        x7104weth = float(x7104liq["reserve1"]) / 10 ** 18
        x7104wethdollar = float(x7104weth) * float(api.get_native_price("eth"))
        x7104tokendollar = float(x7104price) * float(x7104token) / 10 ** 18
        x7105token = float(x7105liq["reserve0"])
        x7105weth = float(x7105liq["reserve1"]) / 10 ** 18
        x7105wethdollar = float(x7105weth) * float(api.get_native_price("eth"))
        x7105tokendollar = float(x7105price) * float(x7105token) / 10 ** 18
        constellationstokens = x7101token + x7102token + x7103token + x7104token + x7105token
        constellationsweth = x7101weth + x7102weth + x7103weth + x7104weth + x7105weth
        constellationswethdollar = \
            x7101wethdollar + x7102wethdollar + x7103wethdollar + x7104wethdollar + x7105wethdollar
        constellationstokendollar = \
            x7101tokendollar + x7102tokendollar + x7103tokendollar + x7104tokendollar + x7105tokendollar
        embed.description = \
            f'**X7 Finance Token Liquidity (ETH)**\n\n' \
            f'*X7R*\n' \
            f'{"{:0,.0f}".format(x7rtoken)[:4]}M X7R (${"{:0,.0f}".format(x7rtokendollar)})\n' \
            f'{x7rweth[:6]} WETH (${"{:0,.0f}".format(x7rwethdollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(x7rwethdollar + x7rtokendollar)})\n\n' \
            f'*X7DAO*\n' \
            f'{"{:0,.0f}".format(x7daotoken)[:4]}M X7DAO (${"{:0,.0f}".format(x7daotokendollar)})\n' \
            f'{x7daoweth[:5]} WETH (${"{:0,.0f}".format(x7daowethdollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(x7daowethdollar + x7daotokendollar)})\n\n' \
            f'**Constellations**\n' \
            f'{"{:0,.0f}".format(constellationstokens)[:4]}M' \
            f' X7100 (${"{:0,.0f}".format(constellationstokendollar)})\n' \
            f'{constellationsweth} WETH' \
            f' (${"{:0,.0f}".format(constellationswethdollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(constellationswethdollar+constellationstokendollar)})\n\n' \
            f'{api.get_quote()}'
    if chain.value == "bsc":
        x7ramount = api.get_native_balance(items.x7rliq, "bsc")
        x7daoamount = api.get_native_balance(items.daoliq, "bsc")
        x7consamount = api.get_native_balance(items.consliq, "bsc")
        x7daodollar = float(x7daoamount) * float(api.get_native_price("bnb")) / 1 ** 18
        x7rdollar = float(x7ramount) * float(api.get_native_price("bnb")) / 1 ** 18
        x7consdollar = float(x7consamount) * float(api.get_native_price("bnb")) / 1 ** 18
        embed.description = \
            '**X7 Finance Initial Liquidity (BSC)**\n\n' \
            f'X7R:\n{x7ramount} BNB (${"{:0,.0f}".format(x7rdollar)})\n\n' \
            f'X7DAO:\n{x7daoamount} BNB (${"{:0,.0f}".format(x7daodollar)})\n\n' \
            f'X7100:\n{x7consamount} BNB (${"{:0,.0f}".format(x7consdollar)})\n\n{api.get_quote()}'
    if chain.value == "arb":
        x7ramount = api.get_native_balance(items.x7rliq, "arb")
        x7daoamount = api.get_native_balance(items.daoliq, "arb")
        x7consamount = api.get_native_balance(items.consliq, "arb")
        x7daodollar = float(x7daoamount) * float(api.get_native_price("eth")) / 1 ** 18
        x7rdollar = float(x7ramount) * float(api.get_native_price("eth")) / 1 ** 18
        x7consdollar = float(x7consamount) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7 Finance Initial Liquidity (ARBITRUM)**\n\n' \
            f'X7R:\n{x7ramount} ETH (${"{:0,.0f}".format(x7rdollar)})\n\n' \
            f'X7DAO:\n{x7daoamount} ETH (${"{:0,.0f}".format(x7daodollar)})\n\n' \
            f'X7100:\n{x7consamount} ETH (${"{:0,.0f}".format(x7consdollar)})\n\n{api.get_quote()}'
    if chain.value == "opti":
        x7ramount = api.get_native_balance(items.x7rliq, "opti")
        x7daoamount = api.get_native_balance(items.daoliq, "opti")
        x7consamount = api.get_native_balance(items.consliq, "opti")
        x7daodollar = float(x7daoamount) * float(api.get_native_price("eth")) / 1 ** 18
        x7rdollar = float(x7ramount) * float(api.get_native_price("eth")) / 1 ** 18
        x7consdollar = float(x7consamount) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7 Finance Initial Liquidity (OPTIMISM)**\n\n' \
            f'X7R:\n{x7ramount} ETH (${"{:0,.0f}".format(x7rdollar)})\n\n' \
            f'X7DAO:\n{x7daoamount} ETH (${"{:0,.0f}".format(x7daodollar)})\n\n' \
            f'X7100:\n{x7consamount} ETH (${"{:0,.0f}".format(x7consdollar)})\n\n{api.get_quote()}'
    if chain.value == "poly":
        x7ramount = api.get_native_balance(items.x7rliq, "poly")
        x7daoamount = api.get_native_balance(items.daoliq, "poly")
        x7consamount = api.get_native_balance(items.consliq, "poly")
        x7daodollar = float(x7daoamount) * float(api.get_native_price("matic")) / 1 ** 18
        x7rdollar = float(x7ramount) * float(api.get_native_price("matic")) / 1 ** 18
        x7consdollar = float(x7consamount) * float(api.get_native_price("matic")) / 1 ** 18
        embed.description = \
            '**X7 Finance Initial Liquidity (POLYGON)**\n\n' \
            f'X7R:\n{x7ramount} MATIC (${"{:0,.0f}".format(x7rdollar)})\n\n' \
            f'X7DAO:\n{x7daoamount} MATIC (${"{:0,.0f}".format(x7daodollar)})\n\n' \
            f'X7100:\n{x7consamount} MATIC (${"{:0,.0f}".format(x7consdollar)})\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


# DISCORD COMMANDS
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


# MOD COMMANDS
@client.command(pass_context=True)
@commands.has_any_role("Community Team")
async def say(ctx, *, saymessage):
    await ctx.message.delete()
    await ctx.send(f"{saymessage}")


@client.command(pass_context=True)
@commands.has_any_role("Community Team")
async def shout(ctx, *, shoutmessage):
    embed = discord.Embed(colour=7419530)
    embed.set_footer(text="Trust no one, Trust code. Long live Defi")
    thumb = discord.File('X7whitelogo.png')
    embed.set_thumbnail(url='attachment://X7whitelogo.png')
    await ctx.message.delete()
    embed.description = f'GM or GN Wherever you are.\n\n {shoutmessage}'
    await ctx.send(f"@everyone")
    await ctx.send(file=thumb, embed=embed)


@client.command(pass_context=True)
@commands.has_any_role("Community Team")
async def chain(ctx, *, chainmessage):
    embed = discord.Embed(colour=7419530)
    embed.set_footer(text="Trust no one, Trust code. Long live Defi")
    thumb = discord.File('X7whitelogo.png')
    embed.set_thumbnail(url='attachment://X7whitelogo.png')
    await ctx.message.delete()
    link = chainmessage.split()[0]
    embed.description = f'**New On Chain Message:**\n\n```{chainmessage[91:]}```'
    await ctx.send(f"@everyone\n<{link}>")
    await ctx.send(file=thumb, embed=embed)


@client.command()
async def move(ctx, movechannel: discord.TextChannel, *message_ids: int):
    for message_id in message_ids:
        movemessage = await ctx.channel.fetch_message(message_id)
        if not message:
            return
        if movemessage.embeds:
            moveembed = movemessage.embeds[0]
            moveembed.title = f'Embed by: {movemessage.author}'
        else:
            moveembed = discord.Embed(
                title=f'Message by: {movemessage.author}',
                description=movemessage.content
            )
        await movechannel.send(embed=moveembed)
        await movemessage.delete()


@client.command()
@commands.has_any_role("Community Team")
async def agree_button(interaction: discord.Interaction):
    await interaction.response.send_message(content="Once you have read and understood the rules, Hit agree to "
                                                    "continue",
                                            view=Button())


# MESSAGES
@client.event
async def on_error(*args):
    print(f'Unhandled message: {args[0]}\n')


@client.event
async def on_message(newmessage):
    if newmessage.author == client.user:
        return
    if newmessage.content == 'GM':
        await newmessage.channel.send('GM or GN, Where ever you are!')
    if newmessage.content == 'Trust no one, Trust code ':
        await newmessage.channel.send('Long Live Defi!')
    if newmessage.content == 'Trust no one':
        await newmessage.channel.send('trust code!')
    await client.process_commands(newmessage)


client.run(keys.DISCORD_TOKEN)
