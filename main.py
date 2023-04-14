import discord
from discord.ext import commands
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
embed.set_thumbnail(url='attachment://X7whitelogo.png')
thumb = discord.File('X7whitelogo.png')


@client.event
async def on_ready():
    print('Bot is ready')
    try:
        synced = await client.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


@client.event
async def on_member_join(join_member):
    join_guild = client.get_guild(1016657044553617428)
    dao = join_guild.get_role(1017420479159607367)
    for joinchannel in join_member.guild.channels:
        if joinchannel.name.startswith('Members'):
            await joinchannel.edit(name=f'Members: {join_member.guild.member_count}')
        if joinchannel.name.startswith('DAO Members'):
            await joinchannel.edit(name=f'DAO Members: {len(dao.members)}')


@client.event
async def on_member_leave(leave_member):
    leaveguild = client.get_guild(1016657044553617428)
    dao = leaveguild.get_role(1017420479159607367)
    for leavechannel in leave_member.guild.channels:
        if leavechannel.name.startswith('Members'):
            await leavechannel.edit(name=f'Members: {leave_member.guild.member_count}')
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
                            "This includes all kinds of self-bots: Nitro snipers, self-bots like " \
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
                            'This includes all kinds of self-bots: Nitro snipers, self-bots like nighty, ' \
                            'auto changing statuses\n\n' \
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
            f'[**Ecosystem Maxi**]({items.ether_token}{items.eco_ca})\n{items.eco_price_eth}\n' \
            f'Available - {500-int(api.get_holders_nft(items.eco_ca, "?chain=eth-main"))}\n'\
            f'> 25% discount on X7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.ether_token}{items.liq_ca})\n{items.liq_price_eth}\n' \
            f'Available - {250-int(api.get_holders_nft(items.liq_ca, "?chain=eth-main"))}\n' \
            f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.ether_token}{items.dex_ca})\n{items.dex_price_eth}\n' \
            f'Available - {150-int(api.get_holders_nft(items.dex_ca, "?chain=eth-main"))}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.ether_token}{items.borrow_ca})\n{items.borrow_price_eth}\n' \
            f'Available - {100-int(api.get_holders_nft(items.borrow_ca, "?chain=eth-main"))}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.ether_token}{items.magister_ca})\n{items.magister_price_eth}\n' \
            f'Available - {49 - int(api.get_holders_nft(items.magister_ca, "?chain=eth-main"))}\n'\
            f'> 25% discount on X7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'[**Pioneer**]({items.ether_token}{items.pioneer_ca})\n' \
            f' > 6% of profits that come into the X7 Treasury Splitter are now being allocated to the reward ' \
            f'pool. Each X7 Pioneer NFT grants you a proportional share of this pool\n\n' \
            f'https://x7.finance/x/nft/mint\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        embed.description = \
            f'**X7 Finance NFT Information (BSC)**\n\n' \
            f'[**Ecosystem Maxi**]({items.bsc_token}{items.eco_ca})\n{items.eco_price_bsc}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.bsc_token}{items.liq_ca})\n{items.liq_price_bsc}\n' \
            f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.bsc_token}{items.dex_ca})\n{items.dex_price_bsc}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.bsc_token}{items.borrow_ca})\n{items.borrow_price_bsc}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.bsc_token}{items.magister_ca})\n{items.magister_price_bsc}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://www.x7finance.org/nfts/\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        embed.description = \
            f'**X7 Finance NFT Information (POLYGON)**\n\n' \
            f'[**Ecosystem Maxi**]({items.poly_token}{items.eco_ca})\n{items.eco_price_poly}\n' \
            f'Available - {500-int(api.get_holders_nft(items.eco_ca, "?chain=poly-main"))}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.poly_token}{items.liq_ca})\n{items.liq_price_poly}\n' \
            f'Available - {250-int(api.get_holders_nft(items.liq_ca, "?chain=poly-main"))}\n' \
            f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.poly_token}{items.dex_ca})\n{items.dex_price_poly}\n' \
            f'Available - {150-int(api.get_holders_nft(items.dex_ca, "?chain=poly-main"))}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.poly_token}{items.borrow_ca})\n{items.borrow_price_poly}\n' \
            f'Available - {100-int(api.get_holders_nft(items.borrow_ca, "?chain=poly-main"))}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.poly_token}{items.magister_ca})\n{items.magister_price_poly}\n'\
            f'Available - {49-int(api.get_holders_nft(items.magister_ca, "?chain=poly-main"))}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://www.x7finance.org/nfts/\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        embed.description = \
            f'**X7 Finance NFT Information (ARBITRUM)**\n\n' \
            f'[**Ecosystem Maxi**]({items.arb_token}{items.eco_ca})\n{items.eco_price_arb}\n' \
            f'Available - {500-int(api.get_holders_nft(items.eco_ca, "?chain=arbitrum"))}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.arb_token}{items.liq_ca})\n{items.liq_price_arb}\n' \
            f'Available - {250-int(api.get_holders_nft(items.liq_ca, "?chain=arbitrum"))}\n' \
            f'> 50 % discount on X7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.arb_token}{items.dex_ca})\n{items.dex_price_arb}\n' \
            f'Available - {150-int(api.get_holders_nft(items.dex_ca, "?chain=arbitrum"))}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.arb_token}{items.borrow_ca})\n{items.borrow_price_arb}\n' \
            f'Available - {100-int(api.get_holders_nft(items.borrow_ca, "?chain=arbitrum"))}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.arb_token}{items.magister_ca})\n{items.magister_price_arb}\n'\
            f'Available - {49-int(api.get_holders_nft(items.magister_ca, "?chain=arbitrum"))}\n' \
            f'> 25% discount on X7100 tax\n' \
            f'> 25% discount on X7R tax\n> No discount on X7DAO tax\n\n' \
            f'https://www.x7finance.org/nfts/\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        embed.description = \
            f'**X7 Finance NFT Information (OPTIMUM)**\n\n' \
            f'[**Ecosystem Maxi**]({items.opti_token}{items.eco_ca})\n{items.eco_price_opti}\n' \
            f'Available - {500-int(api.get_holders_nft(items.eco_ca, "?chain=optimism-main"))}\n' \
            f'> 25% discount on x7100 tax\n' \
            f'> 10% discount on X7R tax\n> 10% discount on X7DAO tax\n\n' \
            f'[**Liquidity Maxi**]({items.opti_token}{items.liq_ca})\n{items.liq_price_opti}\n' \
            f'Available - {250-int(api.get_holders_nft(items.liq_ca, "?chain=optimism-main"))}\n' \
            f'> 50 % discount on x7100tax\n> 25 % discount on X7R tax\n' \
            f'> 15 % discount on X7DAO tax\n\n' \
            f'[**DEX Maxi**]({items.opti_token}{items.dex_ca})\n{items.dex_price_opti}\n' \
            f'Available - {150-int(api.get_holders_nft(items.dex_ca, "?chain=optimism-main"))}\n' \
            f'> LP Fee Discounts while trading on X7 DEX\n\n' \
            f'[**Borrowing Maxi**]({items.opti_token}{items.borrow_ca})\n{items.borrow_price_opti}\n' \
            f'Available - {100-int(api.get_holders_nft(items.borrow_ca, "?chain=optimism-main"))}\n' \
            f'> Fee discounts for borrowing funds for ILO on X7 DEX\n\n' \
            f'[**Magister**]({items.opti_token}{items.magister_ca})\n{items.magister_price_opti}\n' \
            f'Available - {49-int(api.get_holders_nft(items.magister_ca, "?chain=optimism-main"))}\n' \
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
    embed.description = '**X7 Finance buy links**\n\nUse ``/x7token-name`` for all other details\n\n' \
                        f'[X7R - Rewards Token]({items.xchange_buy}{items.x7r_ca})\n' \
                        f'[X7DAO - Governance Token]({items.xchange_buy}{items.x7dao_ca})\n\n{api.get_quote()}'
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
        embed.description = '**X7 Finance Chart links (ETH)**\n\nUse ``/x7token-name`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dex_tools_eth}{items.x7r_pair_eth})\n' \
                            f'[X7DAO - Governance Token]({items.dex_tools_eth}{items.x7dao_pair_eth})\n\n' \
                            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        embed.description = '**X7 Finance Chart links (BSC)**\n\nUse ``/x7token-name`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dex_tools_bsc}{items.x7r_pair_bsc})\n' \
                            f'[X7DAO - Governance Token]({items.dex_tools_bsc}{items.x7dao_pair_bsc})\n\n' \
                            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        embed.description = '**X7 Finance Chart links (POLYGON)**\n\nUse ``/x7token-name`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dex_tools_poly}{items.x7r_pair_poly})\n' \
                            f'[X7DAO - Governance Token]({items.dex_tools_poly}{items.x7dao_pair_poly})\n\n' \
                            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        embed.description = '**X7 Finance Chart links (ARBITRUM)**\n\nUse ``/x7token-name`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dex_tools_arb}{items.x7r_pair_arb})\n' \
                            f'[X7DAO - Governance Token]({items.dex_tools_arb}{items.x7dao_pair_arb})\n\n' \
                            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        embed.description = '**X7 Finance Chart links (OPTIMISM)**\n\nUse ``/x7token-name`` for all other details\n\n' \
                            f'[X7R - Rewards Token]({items.dex_tools_opti}{items.x7r_pair_opti})\n' \
                            f'[X7DAO - Governance Token]({items.dex_tools_opti}{items.x7dao_pair_opti})\n\n' \
                            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token contract info")
async def contract(interaction: discord.Interaction):
    embed.description = f'**X7 Finance token contract info**\n\n**X7R**\n`{items.x7r_ca}`' \
                        f'\n\n**X7DAO**\n`{items.x7dao_ca}`\n\n' \
                        f'Use `/x7token-name` for all other details\n\n{api.get_quote()}'
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
                        '4.2. slippagePercent  -> desired slippage (e.g. 4)\n4.3 deadline -> Go to [epoch-converter]' \
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
@app_commands.rename(pioneer_id='pioneer-id')
@app_commands.describe(pioneer_id='Show Pioneer NFT #')
async def pioneer(interaction: discord.Interaction, pioneer_id: Optional[str] = None):
    if not pioneer_id:
        data = api.get_os_nft("/x7-pioneer")
        data = api.get_os_nft("/x7-pioneer")
        floor = (data["collection"]["stats"]["floor_price"])
        floor_dollar = floor * float(api.get_native_price("eth")) / 1 ** 18
        floor_dollar = floor * float(api.get_native_price("eth")) / 1 ** 18
        traits = (data["collection"]["traits"]["Transfer Lock Status"]["unlocked"])
        cap = round(data["collection"]["stats"]["market_cap"], 2)
        cap_dollar = cap * float(api.get_native_price("eth")) / 1 ** 18
        sales = (data["collection"]["stats"]["total_sales"])
        owners = (data["collection"]["stats"]["num_owners"])
        price = round(data["collection"]["stats"]["average_price"], 2)
        price_dollar = price * float(api.get_native_price("eth")) / 1 ** 18
        volume = round(data["collection"]["stats"]["total_volume"], 2)
        volume_dollar = volume * float(api.get_native_price("eth")) / 1 ** 18
        pioneer_pool = api.get_native_balance(items.pioneer_ca, "eth")
        total_dollar = float(pioneer_pool) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            f'X7 Pioneer NFT Info\n\nFloor Price: {floor} ETH (${"{:0,.0f}".format(floor_dollar)})\n' \
            f'Average Price: {price} ETH (${"{:0,.0f}".format(price_dollar)})\n' \
            f'Market Cap: {cap} ETH (${"{:0,.0f}".format(cap_dollar)})\n' \
            f'Total Volume: {volume} ETH (${"{:0,.0f}".format(volume_dollar)})\n' \
            f'Number of Owners: {owners}\n' \
            f'Pioneers Unlocked: {traits}\n\n' \
            f'Pioneer Pool: {pioneer_pool[:3]} ETH (${"{:0,.0f}".format(total_dollar)})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    else:
        baseurl = "https://api.opensea.io/api/v1/asset/"
        slug = items.pioneer_ca + "/"
        headers = {"X-API-KEY": keys.os}
        single_url = baseurl + slug + pioneer_id + "/"
        single_response = requests.get(single_url, headers=headers)
        single_data = single_response.json()
        status = (single_data["traits"][0]["value"])
        picture = (single_data["image_url"])
        embed.description = f'**X7 Pioneer {pioneer_id} NFT info**\n\n' \
                            f'Transfer Lock Status: {status}\n\n' \
                            f'X7 Pioneer Dashboard - https://x7.finance/x/nft/pioneer\n\n' \
                            f'Opensea - https://opensea.io/assets/ethereum/0x70000299ee8910ccacd97b1bb560e' \
                            f'34f49c9e4f7/{pioneer_id}'
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
        amount = api.get_token_balance(items.dead, "eth", items.x7r_ca)
        percent = round(amount / items.supply * 100, 2)
        burn_dollar = api.get_cg_price("x7r")["x7r"]["usd"] * float(amount)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (ETH)**:\n\n' \
            f'{"{:0,.0f}".format(float(amount))} (${"{:0,.0f}".format(burn_dollar)})\n' \
            f'{percent}% of Supply\n\n' \
            f'[Etherscan]({items.ether_token}{items.x7r_ca}?a={items.dead})\n\n{api.get_quote()}'
    if chain.value == "bsc":
        amount = api.get_token_balance(items.dead, "bsc", items.x7r_ca)
        percent = round(((amount / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (BSC)**:\n\n' \
            f'{"{:,}".format(amount)}' \
            f'{percent}% of Supply\n\n' \
            f'[BSCscan]({items.bsc_token}{items.x7r_ca}?a={items.dead})\n\n{api.get_quote()}'
    if chain.value == "arb":
        amount = api.get_token_balance(items.dead, "arb", items.x7r_ca)
        percent = round(((amount / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (ARBITRUM)**:\n\n' \
            f'{"{:,}".format(amount)}' \
            f'{percent}% of Supply\n\n' \
            f'[Arbiscan]({items.arb_token}{items.x7r_ca}?a={items.dead})\n\n{api.get_quote()}'
    if chain.value == "opti":
        amount = api.get_token_balance(items.dead, "opti", items.x7r_ca)
        percent = round(((amount / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (OPTIMISM)**:\n\n' \
            f'{"{:,}".format(amount)}\n' \
            f'{percent}% of Supply\n\n' \
            f'[Optimism.Etherscan]({items.opti_token}{items.x7r_ca}?a={items.dead})\n\n{api.get_quote()}'
    if chain.value == "poly":
        amount = api.get_token_balance(items.dead, "poly", items.x7r_ca)
        percent = round(((amount / items.supply) * 100), 6)
        embed.description = \
            f'\n\n**X7R Tokens Burn Info (POLYGON)**:\n\n' \
            f'{"{:,}".format(amount)}\n' \
            f'{percent}% of Supply\n\n' \
            f'[Polygonscan]({items.poly_token}{items.x7r_ca}?a={items.dead})\n\n{api.get_quote()}'
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
                        f'3.2. A gnosis multi-sig wallet that will be used to manage the X7D token ownership' \
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
        eth_pool = api.get_native_balance(items.lpool_reserve_ca, "eth")
        pool_dollar = float(eth_pool) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (ETH)**\n\n' \
            f'{eth_pool[:5]} ETH (${"{:0,.0f}".format(pool_dollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.ether_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.ether_address}{items.x7d_ca})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == 'bsc':
        bsc_pool = api.get_native_balance(items.lpool_reserve_ca, "bsc")
        bsc_pool_dollar = float(bsc_pool) * float(api.get_native_price("bnb")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (BSC)**\n\n' \
            f'{bsc_pool[:4]} BNB (${"{:0,.0f}".format(bsc_pool_dollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.bsc_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.bsc_address}{items.x7d_ca})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == 'poly':
        poly_pool = api.get_native_balance(items.lpool_reserve_ca, "poly")
        poly_pool_dollar = float(poly_pool) * float(api.get_native_price("matic")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (POLYGON)**\n\n' \
            f'{poly_pool[:6]} MATIC (${"{:0,.0f}".format(poly_pool_dollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.poly_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.poly_address}{items.x7d_ca})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == 'arb':
        arb_pool = api.get_native_balance(items.lpool_reserve_ca, "arb")
        arb_pool_dollar = float(arb_pool) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (ARB)**\n\n' \
            f'{arb_pool[:4]} ETH (${"{:0,.0f}".format(arb_pool_dollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.arb_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.arb_address}{items.x7d_ca})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == 'opti':
        opti_pool = api.get_native_balance(items.lpool_reserve_ca, "opti")
        opti_pool_dollar = float(opti_pool) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            f'**X7 Finance Lending Pool Info (OPTIMISM)**\n\n' \
            f'{opti_pool[:4]}ETH (${"{:0,.0f}".format(opti_pool_dollar)})\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.opti_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.opti_address}{items.x7d_ca})\n\n' \
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
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        embed.description = '**X7 Finance Opensea links (BSC)**\n\n' \
                            '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi-binance)\n' \
                            '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi-binance)\n' \
                            '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi-binance)\n' \
                            '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max-binance)\n' \
                            f'[Magister](https://opensea.io/collection/x7-magister-binance)\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        embed.description = '**X7 Finance Opensea links (POLYGON)**\n\n' \
                            '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi-polygon)\n' \
                            '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi-polygon)\n' \
                            '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi-polygon)\n' \
                            '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max-polygon)\n' \
                            f'[Magister](https://opensea.io/collection/x7-magister-polygon)\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        embed.description = '**X7 Finance Opensea links (ARB)**\n\n' \
                            '[Ecosystem Maxi](https://opensea.io/collection/x7-ecosystem-maxi-arbitrum)\n' \
                            '[Liquidity Maxi](https://opensea.io/collection/x7-liquidity-maxi-arbitrum)\n' \
                            '[DEX Maxi](https://opensea.io/collection/x7-dex-maxi-arbitrum)\n' \
                            '[Borrowing Maxi](https://opensea.io/collection/x7-borrowing-max-arbitrum)\n' \
                            f'[Magister](https://opensea.io/collection/x7-magister-arbitrum)\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
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
    local_dt = localtime.localize(variables.spaces_time, is_dst=None)
    then = local_dt.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    if duration < timedelta(0):
        embed.description = f'X7 Finance Twitter space\n\nPlease check back for more details\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    else:
        embed.description =\
            f'Next X7 Finance Twitter space is:\n\n{then.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n\n' \
            f'{int(days[0])} days, {int(hours[0])} hours and {int(minutes[0])} minutes\n\n' \
            f'[Click here]({variables.spaces_link}) to set a reminder!' \
            f'\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Make a joke")
async def joke(interaction: discord.Interaction):
    joke_response = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode')
    joke = joke_response.json()
    if joke["type"] == "single":
        embed.description = f'`{joke["joke"]}`'
        await interaction.response.send_message(file=thumb, embed=embed)
    else:
        embed.description = f'`{joke["setup"]}\n\n{joke["delivery"]}`'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="An inspirational quote")
async def quote(interaction: discord.Interaction):
    embed.description = f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token Holders")
async def holders(interaction: discord.Interaction, view: app_commands.Choice[str]):
    x7dao_holders = api.get_holders(items.x7dao_ca)
    x7r_holders = api.get_holders(items.x7r_ca)
    embed.description = '**X7 Finance Token Holders (ETH)**\n\n' \
                        f'X7R Holders: {x7r_holders}\n' \
                        f'X7DAO Holders: {x7dao_holders}\n\n' \
                        f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Market Fear Greed Index")
async def fg(interaction: discord.Interaction):
    fear_response = requests.get("https://api.alternative.me/fng/?limit=0")
    fear_data = fear_response.json()
    timestamp0 = float(fear_data["data"][0]["timestamp"])
    localtime0 = datetime.fromtimestamp(timestamp0)
    timestamp1 = float(fear_data["data"][1]["timestamp"])
    localtime1 = datetime.fromtimestamp(timestamp1)
    timestamp2 = float(fear_data["data"][2]["timestamp"])
    localtime2 = datetime.fromtimestamp(timestamp2)
    timestamp3 = float(fear_data["data"][3]["timestamp"])
    localtime3 = datetime.fromtimestamp(timestamp3)
    timestamp4 = float(fear_data["data"][4]["timestamp"])
    localtime4 = datetime.fromtimestamp(timestamp4)
    timestamp5 = float(fear_data["data"][5]["timestamp"])
    localtime5 = datetime.fromtimestamp(timestamp5)
    timestamp6 = float(fear_data["data"][6]["timestamp"])
    localtime6 = datetime.fromtimestamp(timestamp6)
    duration_in_s = float(fear_data["data"][0]["time_until_update"])
    days = divmod(duration_in_s, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    embed.set_image(url="https://alternative.me/crypto/fear-and-greed-index.png")
    embed.description = \
        f'{fear_data["data"][0]["value"]} - {fear_data["data"][0]["value_classification"]} - ' \
        f'{localtime0.strftime("%A %B %d")} \n\n' \
        f'Change:\n' \
        f'{fear_data["data"][1]["value"]} - {fear_data["data"][1]["value_classification"]} - ' \
        f'{localtime1.strftime("%A %B %d")}\n' \
        f'{fear_data["data"][2]["value"]} - {fear_data["data"][2]["value_classification"]} - ' \
        f'{localtime2.strftime("%A %B %d")}\n' \
        f'{fear_data["data"][3]["value"]} - {fear_data["data"][3]["value_classification"]} - ' \
        f'{localtime3.strftime("%A %B %d")}\n' \
        f'{fear_data["data"][4]["value"]} - {fear_data["data"][4]["value_classification"]} - ' \
        f'{localtime4.strftime("%A %B %d")}\n' \
        f'{fear_data["data"][5]["value"]} - {fear_data["data"][5]["value_classification"]} - ' \
        f'{localtime5.strftime("%A %B %d")}\n' \
        f'{fear_data["data"][6]["value"]} - {fear_data["data"][6]["value_classification"]} - ' \
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
        supply = api.get_native_balance(items.lpool_reserve_ca, "eth")
        holders = api.get_holders(items.x7d_ca)
        x7d_dollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7D Info (ETH)**\n\n' \
            f'Supply: {supply[:5]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n' \
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
            f'[X7 Lending Pool Reserve Contract]({items.ether_address}{items.lpool_reserve_ca})\n'\
            f'[X7D Contract]({items.ether_address}{items.x7d_ca})\n\n'\
            f'`{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        supply = api.get_native_balance(items.lpool_reserve_ca, "bnb")
        x7d_dollar = float(supply) * float(api.get_native_price("bnb")) / 1 ** 18
        embed.description = \
            '**X7D Info (BSC)**\n\n' \
            f'Supply: {supply[:4]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n' \
            f'To receive X7D:\n\n' \
            '1. Send BNB (Not Swap) to the Lending Pool Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:BNB\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.bsc_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.bsc_address}{items.x7d_ca})\n\n' \
            f'`{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        supply = api.get_native_balance(items.lpool_reserve_ca, "poly")
        x7d_dollar = float(supply) * float(api.get_native_price("matic")) / 1 ** 18
        embed.description = \
            '**X7D Info (POLYGON)**\n\n' \
            f'Supply: {supply[:4]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n' \
            f'To receive X7D:\n\n' \
            '1. Send MATIC (Not Swap) to the Lending Pool Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:MATIC\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.poly_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.poly_address}{items.x7d_ca})\n\n' \
            f'`{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        supply = api.get_native_balance(items.lpool_reserve_ca, "arb")
        x7d_dollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7D Info (ETH)**\n\n' \
            f'Supply: {supply[:4]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n' \
            f'To receive X7D:\n\n' \
            '1. Send ETH (Not Swap) to the Lending Pool Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.arb_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.arb_address}{items.x7d_ca})\n\n' \
            f'`{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        supply = api.get_native_balance(items.lpool_reserve_ca, "opti")
        x7d_dollar = float(supply) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7D Info (OPTIMISM)**\n\n' \
            f'Supply: {supply[:4]} X7D (${"{:0,.0f}".format(x7d_dollar)})\n' \
            f'To receive X7D:\n\n' \
            '1. Send ETH (Not Swap) to the Lending Pool Contract:\n' \
            '`0x7Ca54e9Aa3128bF15f764fa0f0f93e72b5267000`\n\n' \
            '2. Import the X7D contract address to your custom tokens in your wallet to see your tokens:\n' \
            '`0x7D000a1B9439740692F8942A296E1810955F5000`\n\n' \
            'You will receive X7D in your wallet which has a 1:1 price X7D:ETH\n\n' \
            'Note:\n' \
            'Do not interact directly with the X7D contract\n' \
            'Do not send from CEX\n\n' \
            f'[X7 Lending Pool Reserve Contract]({items.opti_address}{items.lpool_reserve_ca})\n' \
            f'[X7D Contract]({items.opti_address}{items.x7d_ca})\n\n' \
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
            f'use `/loans ill001 - ill003` for more details on individual loan contracts\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if terms.value == "x7ill001":
        embed.description =\
            f'{items.ill001_name}\n\n' \
            f'{items.ill001_terms}\n\n' \
            f'[Ethereum]({items.ether_address}{items.ill001_ca})\n' \
            f'[BSC]({items.bsc_address}{items.ill001_ca})\n' \
            f'[Polygon]({items.poly_address}{items.ill001_ca})\n' \
            f'[Arbitrum]({items.arb_address}{items.ill001_ca})\n' \
            f'[Optimism]({items.ether_address}{items.ill001_ca})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if terms.value == "x7ill002":
        embed.description = \
            f'{items.ill002_name}\n\n' \
            f'{items.ill002_terms}\n\n' \
            f'[Ethereum]({items.ether_address}{items.ill002_ca})\n' \
            f'[Polygon]({items.poly_address}{items.ill002_ca})\n' \
            f'[Arbitrum]({items.arb_address}{items.ill002_ca})\n' \
            f'[Optimism]({items.ether_address}{items.ill002_ca})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if terms.value == "x7ill003":
        embed.description = \
            f'{items.ill003_name}\n\n' \
            f'{items.ill003_terms}\n\n' \
            f'[Ethereum]({items.ether_address}{items.ill003_ca})\n' \
            f'[BSC]({items.bsc_address}{items.ill003_ca})\n' \
            f'[Polygon]({items.poly_address}{items.ill003_ca})\n' \
            f'[Arbitrum]({items.arb_address}{items.ill003_ca})\n' \
            f'[Optimism]({items.ether_address}{items.ill003_ca})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="Latest X7 Finance Twitter Post")
async def twitter(interaction: discord.Interaction):
    auth = tweepy.OAuthHandler(keys.twitterapi, keys.secret)
    auth.set_access_token(keys.access, keys.accesssecret)
    username = '@x7_finance'
    tweepy_client = tweepy.API(auth)
    tweet = tweepy_client.user_timeline(screen_name=username, count=1)
    embed.description = \
        f'**Latest X7 Finance Tweet**\n\n{tweet[0].text}\n\n' \
        f'{random.choice(items.twitter_replies)}\n'
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
        f'[X7 Lending Discount Contract]({items.ether_address}{items.lending_discount_ca}#code)'
    await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Multichain Rollout")
async def airdrop(interaction: discord.Interaction):
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
    west_coast_raw = pytz.timezone("America/Los_Angeles")
    west_coast = datetime.now(west_coast_raw)
    west_coast_time = west_coast.strftime("%I:%M %p")
    east_coast_raw = pytz.timezone("America/New_York")
    east_coast = datetime.now(east_coast_raw)
    east_coast_time = east_coast.strftime("%I:%M %p")
    london_raw = pytz.timezone("Europe/London")
    london = datetime.now(london_raw)
    london_time = london.strftime("%I:%M %p")
    berlin_raw = pytz.timezone("Europe/Berlin")
    berlin = datetime.now(berlin_raw)
    berlin_time = berlin.strftime("%I:%M %p")
    tokyo_raw = pytz.timezone("Asia/Tokyo")
    tokyo = datetime.now(tokyo_raw)
    tokyo_time = tokyo.strftime("%I:%M %p")
    dubai_raw = pytz.timezone("Asia/Dubai")
    dubai = datetime.now(dubai_raw)
    dubai_time = dubai.strftime("%I:%M %p")
    embed.description = \
        f'{datetime.now().strftime("%A %B %d %Y")}\n' \
        f'{datetime.now().strftime("%I:%M %p")} - UTC\n\n' \
        f'{west_coast_time}\n - PST' \
        f'{east_coast_time}\n - EST' \
        f'{london_time}\n - GMT' \
        f'{berlin_time}\n - CET' \
        f'{dubai_time}\n - GST' \
        f'{tokyo_time}\n - JST'
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
        f"[Xchange Questions]('https://www.x7finance.org/faq/xchange')\n\n{api.get_quote()}"
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
        f"[Xchange Questions]('https://www.x7finance.org/faq/xchange')\n\n{api.get_quote()}"
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="X7 Magister Holders")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    ])
async def magisters(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    if chain.value == "eth":
        response = api.get_nft(items.magister_ca, "eth")
        magisters = list(map(lambda x: x['owner_of'], response["result"]))
        address = '\n\n'.join(map(str, magisters))
        embed.description = \
            '**X7 Finance Magister Holders (ETH)**\n\n' \
            f'`{address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        response = api.get_nft(items.magister_ca, "bsc")
        magisters = list(map(lambda x: x['owner_of'], response["result"]))
        address = '\n\n'.join(map(str, magisters))
        embed.description = \
            '**X7 Finance Magister Holders (BSC)**\n\n' \
            f'`{address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        response = api.get_nft(items.magister_ca, "arbitrum")
        magisters = list(map(lambda x: x['owner_of'], response["result"]))
        address = '\n\n'.join(map(str, magisters))
        embed.description = \
            '**X7 Finance Magister Holders (ARB)**\n\n' \
            f'`{address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        response = api.get_nft(items.magister_ca, "polygon")
        magisters = list(map(lambda x: x['owner_of'], response["result"]))
        address = '\n\n'.join(map(str, magisters))
        embed.description = \
            '**X7 Finance Magister Holders (POLYGON)**\n\n' \
            f'`{address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="X7 Signers")
@app_commands.choices(chain=[
    app_commands.Choice(name="Ethereum", value="eth"),
    app_commands.Choice(name="Binance", value="bsc"),
    app_commands.Choice(name="Polygon", value="poly"),
    app_commands.Choice(name="Arbitrum", value="arb"),
    ])
async def signers(interaction: discord.Interaction, chain: app_commands.Choice[str]):
    if chain.value == "eth":
        dev_response = api.get_signers(items.dev_multi_eth)
        com_response = api.get_signers(items.com_multi_eth)
        devlist = dev_response["owners"]
        dev_address = '\n\n'.join(map(str, devlist))
        com_list = com_response["owners"]
        com_address = '\n\n'.join(map(str, com_list))
        embed.description = \
            f'**X7 Finance Multi-Sig Singers (ETH)**\n' \
            'Use `/signers [chain-name]` or other chains\n\n' \
            f'**Developer Signers**\n`{dev_address}`\n\n**Community Signers**\n`{com_address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        dev_response = api.get_signers(items.dev_multi_poly)
        com_response = api.get_signers(items.com_multi_poly)
        devlist = dev_response["owners"]
        dev_address = '\n\n'.join(map(str, devlist))
        com_list = com_response["owners"]
        com_address = '\n\n'.join(map(str, com_list))
        embed.description = \
            f'**X7 Finance Multi-Sig Singers (POLYGON)**\n' \
            'Use `/signers [chain-name]` or other chains\n\n' \
            f'**Developer Signers**\n`{dev_address}`\n\n**Community Signers**\n`{com_address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        dev_response = api.get_signers(items.dev_multi_bsc)
        com_response = api.get_signers(items.com_multi_bsc)
        devlist = dev_response["owners"]
        dev_address = '\n\n'.join(map(str, devlist))
        com_list = com_response["owners"]
        com_address = '\n\n'.join(map(str, com_list))
        embed.description = \
            f'**X7 Finance Multi-Sig Singers (BSC)**\n' \
            'Use `/signers [chain-name]` or other chains\n\n' \
            f'**Developer Signers**\n`{dev_address}`\n\n**(Community Signers**\n`{com_address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        dev_response = api.get_signers(items.dev_multi_arb)
        com_response = api.get_signers(items.com_multi_arb)
        devlist = dev_response["owners"]
        dev_address = '\n\n'.join(map(str, devlist))
        com_list = com_response["owners"]
        com_address = '\n\n'.join(map(str, com_list))
        embed.description = \
            f'**X7 Finance Multi-Sig Singers (ARB)**\n' \
            'Use `/signers [chain-name]` or other chains\n\n' \
            f'**Developer Signers**\n`{dev_address}`\n\n**Community Signers**\n`{com_address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        dev_response = api.get_signers(items.dev_multi_opti)
        com_response = api.get_signers(items.com_multi_opti)
        devlist = dev_response["owners"]
        dev_address = '\n\n'.join(map(str, devlist))
        com_list = com_response["owners"]
        com_address = '\n\n'.join(map(str, com_list))
        embed.description = \
            f'**X7 Finance Multi-Sig Singers (OPTI)**\n' \
            'Use `/signers [chain-name]` or other chains\n\n' \
            f'*Developer Signers**\n`{dev_address}`\n\n**Community Signers**\n`{com_address}`\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="X7 Finance Launch Info")
async def launch(interaction: discord.Interaction):
    launch_raw = datetime(2022, 8, 13, 14, 10, 17)
    migration_raw = datetime(2022, 9, 25, 5, 00, 11)
    launch = launch_raw.astimezone(pytz.utc)
    migration = migration_raw.astimezone(pytz.utc)
    now = datetime.now(timezone.utc)
    launch_duration = now - launch
    launch_duration_in_s = launch_duration.total_seconds()
    launch_days = divmod(launch_duration_in_s, 86400)
    launch_hours = divmod(launch_days[1], 3600)
    launch_minutes = divmod(launch_hours[1], 60)
    migration_duration = now - migration
    migration_duration_in_s = migration_duration.total_seconds()
    migration_days = divmod(migration_duration_in_s, 86400)
    migration_hours = divmod(migration_days[1], 3600)
    migration_minutes = divmod(migration_hours[1], 60)
    embed.description = \
        f'**X7 Finance Launch Info**\n\nX7M105 Stealth Launch\n{launch.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n' \
        f'{int(launch_days[0])} days, {int(launch_hours[0])} hours and {int(launch_minutes[0])} minutes ago\n\n' \
        f'V2 Migration\n{migration.strftime("%A %B %d %Y %I:%M %p")} (UTC)\n' \
        f'{int(migration_days[0])} days, {int(migration_hours[0])} hours and ' \
        f'{int(migration_minutes[0])} minutes ago\n\n' \
        f'[X7M105 Launch TX](https://etherscan.io/tx/' \
        f'0x11ff5b6a860170eaac5b33930680bf79dbf0656292cac039805dbcf34e8abdbf)\n' \
        f'[Migration Go Live TX](https://etherscan.io/tx/' \
        f'0x13e8ed59bcf97c5948837c8069f1d61e3b0f817d6912015427e468a77056fe41)\n\n' \
        f'{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="X7 Finance Deployer Info")
async def deployer(interaction: discord.Interaction):
    deployer = api.get_tx(items.deployer, "eth")
    dev = api.get_tx(items.dev_multi_eth, "eth")
    date = deployer["result"][0]["block_timestamp"].split("-")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2][:2])
    then = datetime(year, month, day)
    now = datetime.now()
    duration = now - then
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)
    dev_date = dev["result"][0]["block_timestamp"].split("-")
    dev_year = int(dev_date[0])
    dev_month = int(dev_date[1])
    dev_day = int(dev_date[2][:2])
    dev_then = datetime(dev_year, dev_month, dev_day)
    dev_duration = now - dev_then
    dev_duration_in_s = dev_duration.total_seconds()
    dev_days = divmod(dev_duration_in_s, 86400)
    embed.description = \
        '**X7 Finance DAO Founders**\n\n' \
        '[Deployer Wallet](https://etherscan.io/address/0x7000a09c425abf5173ff458df1370c25d1c58105)\n' \
        f'Last TX -  {int(days[0])} days ago:\n' \
        f'https://etherscan.io/tx/{deployer["result"][0]["hash"]}\n\n' \
        f'[Developer Operations Wallet](https://etherscan.io/address/0x5CF4288Bf373BBe17f76948E39Baf33B9f6ac2e0)\n' \
        f'Last TX -  {int(dev_days[0])} days ago:\n' \
        f'https://etherscan.io/tx/{dev["result"][0]["hash"]}\n\n{api.get_quote()}'
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="On this day in history")
async def today(interaction: discord.Interaction):
    data = api.get_today()
    today = (random.choice(data["data"]["Events"]))
    embed.description = \
        f'`On this day in {today["year"]}:\n\n{today["text"]}`',
    await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="X7 Finance Voting Info")
async def voting(interaction: discord.Interaction):
    embed.description = \
        '**Proposals and Voting**\n\nVoting will occur in multiple phases, each of which has either a minimum or ' \
        'maximum time phase duration.\n\n*Phase 1: Quorum-seeking*\nX7DAO token holders will be able to stake ' \
        'their tokens as X7sDAO, a non-transferable staked version of X7DAO.\n\nA quorum is reached when more ' \
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
        gas_data = api.get_gas("eth")
        embed.description = \
            f'**Eth Gas Prices:**\n' \
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        gas_data = api.get_gas("bsc")
        embed.description = \
            f'**BSC Gas Prices:**\n' \
            f'For other chains use `/gas [chain-name]`\n\n' \
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        gas_data = api.get_gas("poly")
        embed.description = \
            f'**POLYGON Gas Prices:**\n' \
            f'For other chains use `/gas [chain-name]`\n\n' \
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)

@client.tree.command(description="Wei conversion")
@app_commands.describe(eth='amount to convert')
async def wei(interaction: discord.Interaction, eth: Optional[str] = ""):
    wei_raw = float(eth)
    wei = wei_raw * 10 ** 18
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

@client.tree.command(description="X7 Finance Uniswap supply Info")
async def supply(interaction: discord.Interaction):
    prices = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    x7r = api.get_token_balance(items.x7r_pair_eth, "eth", items.x7r_ca)
    x7dao = api.get_token_balance(items.x7dao_pair_eth, "eth", items.x7dao_ca)
    x7101 = api.get_token_balance(items.x7101_pair_eth, "eth", items.x7101_ca)
    x7102 = api.get_token_balance(items.x7102_pair_eth, "eth", items.x7102_ca)
    x7103 = api.get_token_balance(items.x7103_pair_eth, "eth", items.x7103_ca)
    x7104 = api.get_token_balance(items.x7104_pair_eth, "eth", items.x7104_ca)
    x7105 = api.get_token_balance(items.x7105_pair_eth, "eth", items.x7105_ca)
    x7r_dollar = x7r * prices["x7r"]["usd"]
    x7dao_dollar = x7dao * prices["x7dao"]["usd"]
    x7101_dollar = x7101 * prices["x7101"]["usd"]
    x7102_dollar = x7102 * prices["x7102"]["usd"]
    x7103_dollar = x7103 * prices["x7103"]["usd"]
    x7104_dollar = x7104 * prices["x7104"]["usd"]
    x7105_dollar = x7105 * prices["x7105"]["usd"]
    x7r_percent = round(x7r / items.supply * 100, 2)
    x7dao_percent = round(x7dao / items.supply * 100, 2)
    x7101_percent = round(x7101 / items.supply * 100, 2)
    x7102_percent = round(x7102 / items.supply * 100, 2)
    x7103_percent = round(x7103 / items.supply * 100, 2)
    x7104_percent = round(x7104 / items.supply * 100, 2)
    x7105_percent = round(x7105 / items.supply * 100, 2)
    embed.description = \
        f'**X7 Finance Uniswap Supply**\n\n' \
        f'**X7R**\n' \
        f'{"{:0,.0f}".format(x7r)} X7R (${"{:0,.0f}".format(x7r_dollar)}) {x7r_percent}%\n\n' \
        f'**X7DAO**\n' \
        f'{"{:0,.0f}".format(x7dao)} X7DAO (${"{:0,.0f}".format(x7dao_dollar)}) {x7dao_percent}%\n\n' \
        f'**X7101**\n' \
        f'{"{:0,.0f}".format(x7101)} X7101 (${"{:0,.0f}".format(x7101_dollar)}) {x7101_percent}%\n\n' \
        f'**X7102**\n' \
        f'{"{:0,.0f}".format(x7102)} X7102 (${"{:0,.0f}".format(x7102_dollar)}) {x7102_percent}%\n\n' \
        f'**X7103**\n' \
        f'{"{:0,.0f}".format(x7103)} X7103 (${"{:0,.0f}".format(x7103_dollar)}) {x7103_percent}%\n\n' \
        f'**X7104**\n' \
        f'{"{:0,.0f}".format(x7104)} X7104 (${"{:0,.0f}".format(x7104_dollar)}) {x7104_percent}%\n\n' \
        f'**X7105**\n' \
        f'{"{:0,.0f}".format(x7105)} X7105 (${"{:0,.0f}".format(x7105_dollar)}) {x7105_percent}%\n\n' \
        f'{api.get_quote()}\n\n'
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
        holders = api.get_holders(items.x7dao_ca)
        x7dao_liq = api.get_liquidity(items.x7dao_pair_eth)
        x7dao_token = float(x7dao_liq["reserve0"])
        x7dao_weth = float(x7dao_liq["reserve1"]) / 10 ** 18
        x7dao_weth_dollar = float(x7dao_weth) * float(api.get_native_price("eth"))
        x7dao_token_dollar = float(price["x7dao"]["usd"]) * float(x7dao_token) / 10 ** 18
        embed.description =\
            f'**X7DAO (ETH) Info**\n\n' \
            f'X7DAO Price: ${price["x7dao"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7dao"]["usd_24h_change"],1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7dao"]["usd"]*items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7dao"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Liquidity:\n' \
            f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n' \
            f'{x7dao_weth[:5]} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)})\n\n' \
            f'Contract Address:\n`{items.x7dao_ca}`\n\n' \
            f'[Etherscan]({items.ether_token}{items.x7dao_ca})\n' \
            f'[Chart]({items.dex_tools_eth}{items.x7dao_pair_eth})\n' \
            f'[Buy]({items.xchange_buy}{items.x7dao_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description =\
            f'**X7DAO (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7dao_ca}`\n\n' \
            f'[BSCscan]({items.bsc_token}{items.x7dao_ca})\n' \
            f'[Chart]({items.dex_tools_bsc}{items.x7dao_pair_bsc})\n' \
            f'[Buy]({items.xchange_buy}{items.x7dao_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description =\
            f'**X7DAO (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7dao_ca}`\n\n' \
            f'[Polygonscan]({items.poly_token}{items.x7dao_ca})\n' \
            f'[Chart]({items.dex_tools_poly}{items.x7dao_pair_poly})\n' \
            f'[Buy]({items.xchange_buy}{items.x7dao_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7DAO (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7dao_ca}`\n\n' \
            f'[Arbiscan]({items.arb_token}{items.x7dao_ca})\n' \
            f'[Chart]({items.dex_tools_arb}{items.x7dao_pair_arb})\n' \
            f'[Buy]({items.xchange_buy}{items.x7dao_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description =\
            f'**X7DAO (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7dao_ca}`\n\n' \
            f'[Optimistic.etherscan]({items.opti_token}{items.x7dao_ca})\n' \
            f'[Chart]({items.dex_tools_opti}{items.x7dao_pair_opti})\n' \
            f'[Buy]({items.xchange_buy}{items.x7dao_ca})\n\n{api.get_quote()}'
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
        holders = api.get_holders(items.x7r_ca)
        x7r_burn = api.get_token_balance(items.dead, "eth", items.x7r_ca)
        percent = round(((x7r_burn / items.supply) * 100), 6)
        x7r_liq = api.get_liquidity(items.x7r_pair_eth)
        x7r_token = float(x7r_liq["reserve0"])
        x7r_weth = float(x7r_liq["reserve1"]) / 10 ** 18
        x7r_weth_dollar = float(x7r_weth) * float(api.get_native_price("eth"))
        x7r_token_dollar = float(price["x7r"]["usd"]) * float(x7r_token) / 10 ** 18
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
            f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n' \
            f'{x7r_weth[:6]} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)})\n\n' \
            f'Contract Address:\n`{items.x7r_ca}`\n\n' \
            f'[Etherscan]({items.ether_token}{items.x7r_ca})\n' \
            f'[Chart]({items.dex_tools_eth}{items.x7r_pair_eth})\n' \
            f'[Buy]({items.xchange_buy}{items.x7r_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description =\
            f'**X7R (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7r_ca}\n\n`' \
            f'[BSCscan]({items.bsc_token}{items.x7r_ca})\n' \
            f'[Chart]({items.dex_tools_bsc}{items.x7r_pair_bsc})\n' \
            f'[Buy]({items.xchange_buy}{items.x7r_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description =\
            f'**X7R (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7r_ca}\n\n`' \
            f'[Polygonscan]({items.poly_token}{items.x7r_ca})\n' \
            f'[Chart]({items.dex_tools_poly}{items.x7r_pair_poly})\n' \
            f'[Buy]({items.xchange_buy}{items.x7r_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7R (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7r_ca}\n\n`' \
            f'[Arbiscan]({items.arb_token}{items.x7r_ca})\n' \
            f'[Chart]({items.dex_tools_arb}{items.x7r_pair_arb})\n' \
            f'[Buy]({items.xchange_buy}{items.x7r_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description =\
            f'**X7R (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7r_ca}\n\n`' \
            f'[Optimistic.etherscan]({items.opti_token}{items.x7r_ca})\n' \
            f'[Chart]({items.dex_tools_opti}{items.x7r_pair_opti})\n' \
            f'[Buy]({items.xchange_buy}{items.x7r_ca})\n\n{api.get_quote()}'
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
        holders = api.get_holders(items.x7101_ca)
        embed.description =\
            f'**X7101 (ETH) Info**\n\n' \
            f'X7101 Price: ${price["x7101"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7101"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7101"]["usd"] * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7101"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7101_ca}`\n\n' \
            f'[Etherscan]({items.ether_token}{items.x7101_ca})\n' \
            f'[Chart]({items.dex_tools_eth}{items.x7101_pair_eth})\n' \
            f'[Buy]({items.xchange_buy}{items.x7101_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description =\
            f'**X7101 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7101_ca}`\n\n' \
            f'[BSCscan]({items.bsc_token}{items.x7101_ca})\n' \
            f'[Chart]({items.dex_tools_bsc}{items.x7101_pair_bsc})\n' \
            f'[Buy]({items.xchange_buy}{items.x7101_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description =\
            f'**X7101 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7101_ca}`\n\n' \
            f'[Polygonscan]({items.poly_token}{items.x7101_ca})\n' \
            f'[Chart]({items.dex_tools_poly}{items.x7101_pair_poly})\n' \
            f'[Buy]({items.xchange_buy}{items.x7101_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7101 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7101_ca}`\n\n' \
            f'[Arbiscan]({items.arb_token}{items.x7101_ca})\n' \
            f'[Chart]({items.dex_tools_arb}{items.x7101_pair_arb})\n' \
            f'[Buy]({items.xchange_buy}{items.x7101_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7101 (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7101_ca}`\n\n' \
            f'[Optimistic.etherscan]({items.opti_token}{items.x7101_ca})\n' \
            f'[Chart]({items.dex_tools_opti}{items.x7101_pair_opti})\n' \
            f'[Buy]({items.xchange_buy}{items.x7101_ca})\n\n{api.get_quote()}'
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
        holders = api.get_holders(items.x7102_ca)
        embed.description = \
            f'**X7102 (ETH) Info**\n\n' \
            f'X7102 Price: ${price["x7102"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7102"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7102"]["usd"]*items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7102"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7102_ca}`\n\n' \
            f'[Etherscan]({items.ether_token}{items.x7102_ca})\n' \
            f'[Chart]({items.dex_tools_eth}{items.x7102_pair_eth})\n' \
            f'[Buy]({items.xchange_buy}{items.x7102_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description = \
            f'**X7102 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7102_ca}`\n\n' \
            f'[BSCscan]({items.bsc_token}{items.x7102_ca})\n' \
            f'[Chart]({items.dex_tools_bsc}{items.x7102_pair_bsc})\n' \
            f'[Buy]({items.xchange_buy}{items.x7102_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description = \
            f'**X7102 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7102_ca}`\n\n' \
            f'[Polygonscan]({items.poly_token}{items.x7102_ca})\n' \
            f'[Chart]({items.dex_tools_poly}{items.x7102_pair_poly})\n' \
            f'[Buy]({items.xchange_buy}{items.x7102_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description = \
            f'**X7102 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7102_ca}`\n\n' \
            f'[Arbiscan]({items.arb_token}{items.x7102_ca})\n' \
            f'[Chart]({items.dex_tools_arb}{items.x7102_pair_arb})\n' \
            f'[Buy]({items.xchange_buy}{items.x7102_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description = \
            f'**X7102 (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7102_ca}`\n\n' \
            f'[Optimistic.etherscan]({items.opti_token}{items.x7102_ca})\n' \
            f'[Chart]({items.dex_tools_opti}{items.x7102_pair_opti})\n' \
            f'[Buy]({items.xchange_buy}{items.x7102_ca})\n\n{api.get_quote()}'
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
        holders = api.get_holders(items.x7103_ca)
        embed.description = \
            f'**X7103 (ETH) Info**\n\n' \
            f'X7103 Price: ${price["x7103"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7103"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7103"]["usd"] * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7103"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7103_ca}`\n\n' \
            f'[Etherscan]({items.ether_token}{items.x7103_ca})\n' \
            f'[Chart]({items.dex_tools_eth}{items.x7103_pair_eth})\n' \
            f'[Buy]({items.xchange_buy}{items.x7103_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description = \
            f'**X7103 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7103_ca}`\n\n' \
            f'[BSCscan]({items.bsc_token}{items.x7103_ca})\n' \
            f'[Chart]({items.dex_tools_bsc}{items.x7103_pair_bsc})\n' \
            f'[Buy]({items.xchange_buy}{items.x7103_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description = \
            f'**X7103 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7103_ca}`\n\n' \
            f'[Polygonscan]({items.poly_token}{items.x7103_ca})\n' \
            f'[Chart]({items.dex_tools_poly}{items.x7103_pair_poly})\n' \
            f'[Buy]({items.xchange_buy}{items.x7103_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description = \
            f'**X7103 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7103_ca}`\n\n' \
            f'[Arbiscan]({items.arb_token}{items.x7103_ca})\n' \
            f'[Chart]({items.dex_tools_arb}{items.x7103_pair_arb})\n' \
            f'[Buy]({items.xchange_buy}{items.x7103_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description = \
            f'**X7103 (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7103_ca}`\n\n' \
            f'[Optimistic.etherscan]({items.opti_token}{items.x7103_ca})\n' \
            f'[Chart]({items.dex_tools_opti}{items.x7103_pair_opti})\n' \
            f'[Buy]({items.xchange_buy}{items.x7103_ca})\n\n{api.get_quote()}'
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
        holders = api.get_holders(items.x7104_ca)
        embed.description = \
            f'**X7104 (ETH) Info**\n\n' \
            f'X7104 Price: ${price["x7104"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7104"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7104"]["usd"] * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7104"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7104_ca}`\n\n' \
            f'[Etherscan]({items.ether_token}{items.x7104_ca})\n' \
            f'[Chart]({items.dex_tools_eth}{items.x7104_pair_eth})\n' \
            f'[Buy]({items.xchange_buy}{items.x7104_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description =\
            f'**X7104 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7104_ca}`\n\n' \
            f'[BSCscan]({items.bsc_token}{items.x7104_ca})\n' \
            f'[Chart]({items.dex_tools_bsc}{items.x7104_pair_bsc})\n' \
            f'[Buy]({items.xchange_buy}{items.x7104_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description =\
            f'**X7104 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7104_ca}`\n\n' \
            f'[Polygonscan]({items.poly_token}{items.x7104_ca})\n' \
            f'[Chart]({items.dex_tools_poly}{items.x7104_pair_poly})\n' \
            f'[Buy]({items.xchange_buy}{items.x7104_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description =\
            f'**X7104 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7104_ca}`\n\n' \
            f'[Arbiscan]({items.arb_token}{items.x7104_ca})\n' \
            f'[Chart]({items.dex_tools_arb}{items.x7104_pair_arb})\n' \
            f'[Buy]({items.xchange_buy}{items.x7104_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description =\
            f'**X7104 (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7104_ca}`\n\n' \
            f'[Optimistic.etherscan]({items.opti_token}{items.x7104_ca})\n' \
            f'[Chart]({items.dex_tools_opti}{items.x7104_pair_opti})\n' \
            f'[Buy]({items.xchange_buy}{items.x7104_ca})\n\n{api.get_quote()}'
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
        holders = api.get_holders(items.x7105_ca)
        embed.description = \
            f'**X7105 (ETH) Info**\n\n' \
            f'X7105 Price: ${price["x7105"]["usd"]}\n' \
            f'24 Hour Change: {round(price["x7105"]["usd_24h_change"], 1)}%\n' \
            f'Market Cap:  ${"{:0,.0f}".format(price["x7105"]["usd"] * items.supply)}\n' \
            f'24 Hour Volume: ${"{:0,.0f}".format(price["x7105"]["usd_24h_vol"])}\n' \
            f'Holders: {holders}\n\n' \
            f'Contract Address:\n`{items.x7105_ca}`\n\n' \
            f'[Etherscan]({items.ether_token}{items.x7105_ca})\n' \
            f'[Chart]({items.dex_tools_eth}{items.x7105_pair_eth})\n' \
            f'[Buy]({items.xchange_buy}{items.x7105_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "bsc":
        embed.description = \
            f'**X7105 (BSC) Info**\n\n' \
            f'Contract Address:\n`{items.x7105_ca}`\n\n' \
            f'[BSCscan]({items.bsc_token}{items.x7105_ca})\n' \
            f'[Chart]({items.dex_tools_bsc}{items.x7105_pair_bsc})\n' \
            f'[Buy]({items.xchange_buy}{items.x7105_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "poly":
        embed.description = \
            f'**X7105 (POLYGON) Info**\n\n' \
            f'Contract Address:\n`{items.x7105_ca}`\n\n' \
            f'[Polygonscan]({items.poly_token}{items.x7105_ca})\n' \
            f'[Chart]({items.dex_tools_poly}{items.x7105_pair_poly})\n' \
            f'[Buy]({items.xchange_buy}{items.x7105_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "arb":
        embed.description = \
            f'**X7105 (ARBITRUM) Info**\n\n' \
            f'Contract Address:\n`{items.x7105_ca}`\n\n' \
            f'[Arbiscan]({items.arb_token}{items.x7105_ca})\n' \
            f'[Chart]({items.dex_tools_arb}{items.x7105_pair_arb})\n' \
            f'[Buy]({items.xchange_buy}{items.x7105_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)
    if chain.value == "opti":
        embed.description = \
            f'**X7105 (OPTIMISM) Info**\n\n' \
            f'Contract Address:\n`{items.x7105_ca}`\n\n' \
            f'[Optimistic.etherscan]({items.opti_token}{items.x7105_ca})\n' \
            f'[Chart]({items.dex_tools_opti}{items.x7105_pair_opti})\n' \
            f'[Buy]({items.xchange_buy}{items.x7105_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=embed, file=thumb)

@client.tree.command(description='Constellation Info')
async def constellations(interaction: discord.Interaction):
    price = api.get_cg_price("x7101, x7102, x7103, x7104, x7105")
    x7101_mc = price["x7101"]["usd"] * items.supply
    x7102_mc = price["x7102"]["usd"] * items.supply
    x7103_mc = price["x7103"]["usd"] * items.supply
    x7104_mc = price["x7104"]["usd"] * items.supply
    x7105_mc = price["x7105"]["usd"] * items.supply
    const_mc = x7101_mc + x7102_mc + x7103_mc + x7104_mc + x7105_mc
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
        f'For more info use `/x7token-name`\n\n' \
        f'X7101:      ${price["x7101"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7101"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7101_mc)}\n' \
        f'CA: `{items.x7101_ca}`\n\n' \
        f'X7102:      ${price["x7102"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7102"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7102_mc)}\n' \
        f'CA: `{items.x7102_ca}`\n\n' \
        f'X7103:      ${price["x7103"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7103"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7103_mc)}\n' \
        f'CA: `{items.x7103_ca}`\n\n' \
        f'X7104:      ${price["x7104"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7104"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7104_mc)}\n' \
        f'CA: `{items.x7104_ca}`\n\n' \
        f'X7105:      ${price["x7105"]["usd"]}\n' \
        f'24 Hour Change: {round(price["x7105"]["usd_24h_change"],1)}%\n' \
        f'Market Cap:  ${"{:0,.0f}".format(x7105_mc)}\n' \
        f'CA: `{items.x7105_ca}`\n\n' \
        f'Combined Market Cap: ${"{:0,.0f}".format(const_mc)}\n\n' \
        f'{api.get_quote()}'
    await interaction.response.send_message(embed=embed, file=thumb)


@client.tree.command(description="Market Cap Info")
@app_commands.choices(view=[
    app_commands.Choice(name="Text", value="text"),
    app_commands.Choice(name="Image", value="img"),
    ])
async def mcap(interaction: discord.Interaction, view: app_commands.Choice[str]):
    x7r_supply = items.supply - api.get_token_balance(items.dead, "eth", items.x7r_ca)
    price = api.get_cg_price("x7r, x7dao, x7101, x7102, x7103, x7104, x7105")
    x7r_cap = (price["x7r"]["usd"]) * x7r_supply
    x7dao_cap = (price["x7dao"]["usd"]) * items.supply
    x7101_cap = (price["x7101"]["usd"]) * items.supply
    x7102_cap = (price["x7102"]["usd"]) * items.supply
    x7103_cap = (price["x7103"]["usd"]) * items.supply
    x7104_cap = (price["x7104"]["usd"]) * items.supply
    x7105_cap = (price["x7105"]["usd"]) * items.supply
    cons_cap = x7101_cap + x7102_cap + x7103_cap + x7104_cap + x7105_cap
    total_cap = x7r_cap + x7dao_cap + x7101_cap + x7102_cap + x7103_cap + x7104_cap + x7105_cap
    embed.description = \
        f'**X7 Finance Market Cap Info (ETH)**\n\n' \
        f'X7R:          ${"{:0,.0f}".format(x7r_cap)}\n' \
        f'X7DAO:     ${"{:0,.0f}".format(x7dao_cap)}\n' \
        f'X7101:       ${"{:0,.0f}".format(x7101_cap)}\n' \
        f'X7102:       ${"{:0,.0f}".format(x7102_cap)}\n' \
        f'X7103:       ${"{:0,.0f}".format(x7103_cap)}\n' \
        f'X7104:       ${"{:0,.0f}".format(x7104_cap)}\n' \
        f'X7105:       ${"{:0,.0f}".format(x7105_cap)}\n\n' \
        f'Constellations Combined: ' \
        f'${"{:0,.0f}".format(x7101_cap + x7102_cap + x7103_cap + x7104_cap + x7105_cap)}\n' \
        f'Total Token Market-cap:\n' \
        f'    ${"{:0,.0f}".format(total_cap)}' \
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
        dev_eth = api.get_native_balance(items.dev_multi_eth, "eth")
        com_eth = api.get_native_balance(items.com_multi_eth, "eth")
        pioneer_eth = api.get_native_balance(items.pioneer_ca, "eth")
        dev_dollar = float(dev_eth) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("eth")) / 1 ** 18
        pioneer_dollar = float(pioneer_eth) * float(api.get_native_price("eth")) / 1 ** 18
        com_x7r = api.get_token_balance(items.com_multi_eth, "eth", items.x7r_ca)
        com_x7r_price = com_x7r * api.get_cg_price("x7r")["x7r"]["usd"]
        com_x7d = api.get_token_balance(items.com_multi_eth, "eth", items.x7d_ca)
        com_x7d_price = com_x7d * api.get_native_price("eth")
        com_total = com_x7r_price + com_dollar + com_x7d_price
        embed.description = \
            f'**X7 Finance Treasury Info (ETH)**\n\n' \
            f'Pioneer Pool:\n{pioneer_eth[:4]}ETH (${"{:0,.0f}".format(pioneer_dollar)})\n\n' \
            f'[Developer Wallet:]({items.ether_address}{items.dev_multi_eth})\n' \
            f'{dev_eth[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n' \
            f'[Community Wallet:]({items.ether_address}{items.com_multi_eth})\n' \
            f'{com_eth[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n' \
            f'{com_x7r} X7R (${"{:0,.0f}".format(com_x7r_price)})\n' \
            f'{com_x7d} X7D (${"{:0,.0f}".format(com_x7d_price)})\n' \
            f'Total: (${"{:0,.0f}".format(com_total)})\n\n' \
            f'[Treasury Splitter Contract]({items.ether_address}{items.treasury_splitter_ca})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        dev_eth = api.get_native_balance(items.dev_multi_bsc, "bsc")
        com_eth = api.get_native_balance(items.com_multi_bsc, "bsc")
        dev_dollar = float(dev_eth) * float(api.get_native_price("bnb")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("bnb")) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (BSC)**\n\n' \
            f'Developer Wallet:\n{dev_eth[:4]}BNB (${"{:0,.0f}".format(dev_dollar)})\n\n' \
            f'Community Wallet:\n{com_eth[:4]}BNB (${"{:0,.0f}".format(com_dollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.bsc_address}{items.treasury_splitter_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        dev_eth = api.get_native_balance(items.dev_multi_arb, "arb")
        com_eth = api.get_native_balance(items.dev_multi_arb, "arb")
        dev_dollar = float(dev_eth) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (ARB)**\n\n' \
            f'Developer Wallet:\n{dev_eth[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n' \
            f'Community Wallet:\n{com_eth[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.arb_address}{items.treasury_splitter_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        dev_eth = api.get_native_balance(items.dev_multi_opti, "opti")
        com_eth = api.get_native_balance(items.com_multi_opti, "opti")
        dev_dollar = float(dev_eth) * float(api.get_native_price("eth")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (OPTIMISM)**\n\n' \
            f'Developer Wallet:\n{dev_eth[:4]}ETH (${"{:0,.0f}".format(dev_dollar)})\n\n' \
            f'Community Wallet:\n{com_eth[:4]}ETH (${"{:0,.0f}".format(com_dollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.opti_address}{items.treasury_splitter_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        dev_eth = api.get_native_balance(items.dev_multi_poly, "poly")
        com_eth = api.get_native_balance(items.com_multi_poly, "poly")
        dev_dollar = float(dev_eth) * float(api.get_native_price("matic")) / 1 ** 18
        com_dollar = float(com_eth) * float(api.get_native_price("matic")) / 1 ** 18
        embed.description = \
            '**X7 Finance Treasury (POLYGON)**\n\n' \
            f'Developer Wallet:\n{dev_eth[:4]}MATIC (${"{:0,.0f}".format(dev_dollar)})\n\n' \
            f'Community Wallet:\n{com_eth[:4]}MATIC (${"{:0,.0f}".format(com_dollar)})\n\n' \
            f'[Treasury Splitter Contract]({items.poly_address}{items.treasury_splitter_ca})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)


@client.tree.command(description="X7 Finance Token price info")
@app_commands.describe(coin='Coin Name')
async def price(interaction: discord.Interaction, coin: Optional[str] = ""):
    token = api.get_cg_search(coin)
    token_id = token["coins"][0]["api_symbol"]
    token_logo = token["coins"][0]["thumb"]
    symbol = token["coins"][0]["symbol"]
    token_price = api.get_cg_price(token_id)
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
        gas_data = api.get_gas("eth")
        eth_embed = discord.Embed(colour=7419530)
        eth_embed.set_footer(text="Trust no one, Trust code. Long live Defi")
        eth_embed.set_thumbnail(url=token_logo)
        eth_embed.description = \
            f'**{symbol} price**\n\n' \
            f'Eth Price:\n${eth["result"]["ethusd"]}\n' \
            f'24 Hour Change: {round(eth["ethereum"]["usd_24h_change"], 1)}%\n\n' \
            f'Gas Prices:\n' \
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=eth_embed)
    if coin == "bnb":
        bnb = api.get_cg_price("binancecoin")
        gas_data = api.get_gas("bsc")
        bnb_embed = discord.Embed(colour=7419530)
        bnb_embed.set_footer(text="Trust no one, Trust code. Long live Defi")
        bnb_embed.set_thumbnail(url=token_logo)
        bnb_embed.description = \
            f'**{symbol} price**\n\n' \
            f'Price: ${bnb["binancecoin"]["usd"]}\n' \
            f'24 Hour Change: {round(bnb["binancecoin"]["usd_24h_change"], 1)}%\n\n' \
            f'Gas Prices:\n' \
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n{api.get_quote()}'
        await interaction.response.send_message(embed=bnb_embed)
        return
    if coin == "matic" or coin == "poly" or coin == "polygon":
        matic = api.get_cg_price("matic-network")
        gas_data = api.get_gas("poly")
        poly_embed = discord.Embed(colour=7419530)
        poly_embed.set_footer(text="Trust no one, Trust code. Long live Defi")
        poly_embed.set_thumbnail(url=token_logo)
        poly_embed.description = \
            f'**{symbol} price**\n\n' \
            f'Price: ${matic["matic-network"]["usd"]}\n' \
            f'24 Hour Change: {round(matic["matic-network"]["usd_24h_change"], 1)}%\n\n' \
            f'Gas Prices:\n' \
            f'Low: {gas_data["result"]["SafeGasPrice"]} Gwei\n' \
            f'Average: {gas_data["result"]["ProposeGasPrice"]} Gwei\n' \
            f'High: {gas_data["result"]["FastGasPrice"]} Gwei\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(embed=poly_embed)
        return
    else:
        token_embed = discord.Embed(colour=7419530)
        token_embed.set_footer(text="Trust no one, Trust code. Long live Defi")
        token_embed.set_thumbnail(url=token_logo)
        token_embed.description = \
            f'**{symbol} price**\n\n' \
            f'Price:      ${"{:f}".format(float(token_price[token_id]["usd"]))}\n' \
            f'24 Hour Change: {round(token_price[token_id]["usd_24h_change"], 1)}%\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(embed=token_embed)


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
        x7r_price = (price["x7r"]["usd"])
        x7dao_price = (price["x7dao"]["usd"])
        x7101_price = (price["x7101"]["usd"])
        x7102_price = (price["x7102"]["usd"])
        x7103_price = (price["x7103"]["usd"])
        x7104_price = (price["x7104"]["usd"])
        x7105_price = (price["x7105"]["usd"])
        x7r_liq = api.get_liquidity(items.x7r_pair_eth)
        x7dao_liq = api.get_liquidity(items.x7dao_pair_eth)
        x7101_liq = api.get_liquidity(items.x7101_pair_eth)
        x7102_liq = api.get_liquidity(items.x7102_pair_eth)
        x7103_liq = api.get_liquidity(items.x7103_pair_eth)
        x7104_liq = api.get_liquidity(items.x7104_pair_eth)
        x7105_liq = api.get_liquidity(items.x7105_pair_eth)
        x7r_token = float(x7r_liq["reserve0"])
        x7r_weth = float(x7r_liq["reserve1"]) / 10 ** 18
        x7r_weth_dollar = float(x7r_weth) * float(api.get_native_price("eth"))
        x7r_token_dollar = float(x7r_price) * float(x7r_token) / 10 ** 18
        x7dao_token = float(x7dao_liq["reserve0"])
        x7dao_weth = float(x7dao_liq["reserve1"]) / 10 ** 18
        x7dao_weth_dollar = float(x7dao_weth) * float(api.get_native_price("eth"))
        x7dao_token_dollar = float(x7dao_price) * float(x7dao_token) / 10 ** 18
        x7101_token = float(x7101_liq["reserve0"])
        x7101_weth = float(x7101_liq["reserve1"]) / 10 ** 18
        x7101_weth_dollar = float(x7101_weth) * float(api.get_native_price("eth"))
        x7101_token_dollar = float(x7101_price) * float(x7101_token) / 10 ** 18
        x7102_token = float(x7102_liq["reserve0"])
        x7102_weth = float(x7102_liq["reserve1"]) / 10 ** 18
        x7102_weth_dollar = float(x7102_weth) * float(api.get_native_price("eth"))
        x7102_token_dollar = float(x7102_price) * float(x7102_token) / 10 ** 18
        x7103_token = float(x7103_liq["reserve0"])
        x7103_weth = float(x7103_liq["reserve1"]) / 10 ** 18
        x7103_weth_dollar = float(x7103_weth) * float(api.get_native_price("eth"))
        x7103_token_dollar = float(x7103_price) * float(x7103_token) / 10 ** 18
        x7104_token = float(x7104_liq["reserve0"])
        x7104_weth = float(x7104_liq["reserve1"]) / 10 ** 18
        x7104_weth_dollar = float(x7104_weth) * float(api.get_native_price("eth"))
        x7104_token_dollar = float(x7104_price) * float(x7104_token) / 10 ** 18
        x7105_token = float(x7105_liq["reserve0"])
        x7105_weth = float(x7105_liq["reserve1"]) / 10 ** 18
        x7105_weth_dollar = float(x7105_weth) * float(api.get_native_price("eth"))
        x7105_token_dollar = float(x7105_price) * float(x7105_token) / 10 ** 18
        constellations_tokens = x7101_token + x7102_token + x7103_token + x7104_token + x7105_token
        constellations_weth = x7101_weth + x7102_weth + x7103_weth + x7104_weth + x7105_weth
        constellations_weth_dollar = \
            x7101_weth_dollar + x7102_weth_dollar + x7103_weth_dollar + x7104_weth_dollar + x7105_weth_dollar
        constellations_token_dollar = \
            x7101_token_dollar + x7102_token_dollar + x7103_token_dollar + x7104_token_dollar + x7105_token_dollar
        embed.description = \
            f'**X7 Finance Token Liquidity (ETH)**\n\n' \
            f'*X7R*\n' \
            f'{"{:0,.0f}".format(x7r_token)[:4]}M X7R (${"{:0,.0f}".format(x7r_token_dollar)})\n' \
            f'{x7r_weth[:6]} WETH (${"{:0,.0f}".format(x7r_weth_dollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(x7r_weth_dollar + x7r_token_dollar)})\n\n' \
            f'*X7DAO*\n' \
            f'{"{:0,.0f}".format(x7dao_token)[:4]}M X7DAO (${"{:0,.0f}".format(x7dao_token_dollar)})\n' \
            f'{x7dao_weth[:5]} WETH (${"{:0,.0f}".format(x7dao_weth_dollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(x7dao_weth_dollar + x7dao_token_dollar)})\n\n' \
            f'**Constellations**\n' \
            f'{"{:0,.0f}".format(constellations_tokens)[:4]}M' \
            f' X7100 (${"{:0,.0f}".format(constellations_token_dollar)})\n' \
            f'{constellations_weth} WETH' \
            f' (${"{:0,.0f}".format(constellations_weth_dollar)})\n' \
            f'Total Liquidity (${"{:0,.0f}".format(constellations_weth_dollar+constellations_token_dollar)})\n\n' \
            f'{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "bsc":
        x7r_amount = api.get_native_balance(items.x7r_liq_lock_ca, "bsc")
        x7dao_amount = api.get_native_balance(items.x7dao_liq_lock_ca, "bsc")
        x7cons_amount = api.get_native_balance(items.cons_liq_lock_ca, "bsc")
        x7dao_dollar = float(x7dao_amount) * float(api.get_native_price("bnb")) / 1 ** 18
        x7r_dollar = float(x7r_amount) * float(api.get_native_price("bnb")) / 1 ** 18
        x7cons_dollar = float(x7cons_amount) * float(api.get_native_price("bnb")) / 1 ** 18
        embed.description = \
            '**X7 Finance Initial Liquidity (BSC)**\n\n' \
            f'X7R:\n{x7r_amount} BNB (${"{:0,.0f}".format(x7r_dollar)})\n\n' \
            f'X7DAO:\n{x7dao_amount} BNB (${"{:0,.0f}".format(x7dao_dollar)})\n\n' \
            f'X7100:\n{x7cons_amount} BNB (${"{:0,.0f}".format(x7cons_dollar)})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "arb":
        x7r_amount = api.get_native_balance(items.x7r_liq_lock_ca, "arb")
        x7dao_amount = api.get_native_balance(items.x7dao_liq_lock_ca, "arb")
        x7cons_amount = api.get_native_balance(items.cons_liq_lock_ca, "arb")
        x7dao_dollar = float(x7dao_amount) * float(api.get_native_price("eth")) / 1 ** 18
        x7r_dollar = float(x7r_amount) * float(api.get_native_price("eth")) / 1 ** 18
        x7cons_dollar = float(x7cons_amount) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7 Finance Initial Liquidity (ARBITRUM)**\n\n' \
            f'X7R:\n{x7r_amount} ETH (${"{:0,.0f}".format(x7r_dollar)})\n\n' \
            f'X7DAO:\n{x7dao_amount} ETH (${"{:0,.0f}".format(x7dao_dollar)})\n\n' \
            f'X7100:\n{x7cons_amount} ETH (${"{:0,.0f}".format(x7cons_dollar)})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "opti":
        x7r_amount = api.get_native_balance(items.x7r_liq_hub_ca, "opti")
        x7dao_amount = api.get_native_balance(items.x7dao_liq_hub_ca, "opti")
        x7cons_amount = api.get_native_balance(items.cons_liq_ca, "opti")
        x7dao_dollar = float(x7dao_amount) * float(api.get_native_price("eth")) / 1 ** 18
        x7r_dollar = float(x7r_amount) * float(api.get_native_price("eth")) / 1 ** 18
        x7cons_dollar = float(x7cons_amount) * float(api.get_native_price("eth")) / 1 ** 18
        embed.description = \
            '**X7 Finance Initial Liquidity (OPTIMISM)**\n\n' \
            f'X7R:\n{x7r_amount} ETH (${"{:0,.0f}".format(x7r_dollar)})\n\n' \
            f'X7DAO:\n{x7dao_amount} ETH (${"{:0,.0f}".format(x7dao_dollar)})\n\n' \
            f'X7100:\n{x7cons_amount} ETH (${"{:0,.0f}".format(x7cons_dollar)})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)
    if chain.value == "poly":
        x7r_amount = api.get_native_balance(items.x7r_liq_lock_ca, "poly")
        x7dao_amount = api.get_native_balance(items.x7dao_liq_lock_ca, "poly")
        x7cons_amount = api.get_native_balance(items.cons_liq_lock_ca, "poly")
        x7dao_dollar = float(x7dao_amount) * float(api.get_native_price("matic")) / 1 ** 18
        x7r_dollar = float(x7r_amount) * float(api.get_native_price("matic")) / 1 ** 18
        x7cons_dollar = float(x7cons_amount) * float(api.get_native_price("matic")) / 1 ** 18
        embed.description = \
            '**X7 Finance Initial Liquidity (POLYGON)**\n\n' \
            f'X7R:\n{x7r_amount} MATIC (${"{:0,.0f}".format(x7r_dollar)})\n\n' \
            f'X7DAO:\n{x7dao_amount} MATIC (${"{:0,.0f}".format(x7dao_dollar)})\n\n' \
            f'X7100:\n{x7cons_amount} MATIC (${"{:0,.0f}".format(x7cons_dollar)})\n\n{api.get_quote()}'
        await interaction.response.send_message(file=thumb, embed=embed)


# DISCORD COMMANDS
@client.tree.command(description="Report user to moderators")
async def report(interaction: discord.Interaction, username: str, reason: str):
    await interaction.response.send_message(f"Thanks {interaction.user}, Your report has been received", ephemeral=True)
    report_channel = client.get_channel(1028614982000193588)
    await report_channel.send(f'<@&1016659542303580221>\n\n{interaction.user} Has reported {username} for:\n{reason}')


@client.tree.command(description="Join X7Force!")
async def x7force(interaction: discord.Interaction, twitter_handle: str):
    await interaction.response.send_message(f"Thanks {interaction.user}, Your request for x7force has been "
                                            f"received", ephemeral=True)
    report_channel = client.get_channel(1028614982000193588)
    await report_channel.send(f'<@&1016659542303580221>\n\n{interaction.user} Has requested {twitter_handle} '
                              f'to be added to x7force')


# MOD COMMANDS
@client.command(pass_context=True)
@commands.has_any_role("Community Team")
async def say(ctx, *, say_message):
    await ctx.message.delete()
    await ctx.send(f"{say_message}")


@client.command(pass_context=True)
@commands.has_any_role("Community Team")
async def shout(ctx, *, shout_message):
    embed = discord.Embed(colour=7419530)
    embed.set_footer(text="Trust no one, Trust code. Long live Defi")
    thumb = discord.File('X7whitelogo.png')
    embed.set_thumbnail(url='attachment://X7whitelogo.png')
    await ctx.message.delete()
    embed.description = f'GM or GN Wherever you are.\n\n {shout_message}'
    await ctx.send(f"@everyone")
    await ctx.send(file=thumb, embed=embed)


@client.command(pass_context=True)
@commands.has_any_role("Community Team")
async def chain(ctx, *, chain_message):
    embed = discord.Embed(colour=7419530)
    embed.set_footer(text="Trust no one, Trust code. Long live Defi")
    thumb = discord.File('X7whitelogo.png')
    embed.set_thumbnail(url='attachment://X7whitelogo.png')
    await ctx.message.delete()
    link = chain_message.split()[0]
    embed.description = f'**New On Chain Message:**\n\n```{chain_message[91:]}```'
    await ctx.send(f"@everyone\n<{link}>")
    await ctx.send(file=thumb, embed=embed)


@client.command()
async def move(ctx, move_channel: discord.TextChannel, *message_ids: int):
    for message_id in message_ids:
        movemessage = await ctx.channel.fetch_message(message_id)
        if not message:
            return
        if movemessage.embeds:
            move_embed = movemessage.embeds[0]
            move_embed.title = f'Embed by: {movemessage.author}'
        else:
            move_embed = discord.Embed(
                title=f'Message by: {movemessage.author}',
                description=movemessage.content
            )
        await move_channel.send(embed=move_embed)
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
async def on_message(new_message):
    if new_message.author == client.user:
        return
    if new_message.content == 'GM':
        await new_message.channel.send('GM or GN, Where ever you are!')
    if new_message.content == 'Trust no one, Trust code ':
        await new_message.channel.send('Long Live Defi!')
    if new_message.content == 'Trust no one':
        await new_message.channel.send('trust code!')
    await client.process_commands(new_message)


client.run(keys.DISCORD_TOKEN)
