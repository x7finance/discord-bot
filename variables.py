from datetime import datetime
# VARIABLES

# SPACES                Y   M   D   H   M  S
spacestime = datetime(2023, 2, 3, 19, 00, 00)
spaceslink = "https://twitter.com/i/spaces/1YqKDojbAoQxV"

# AUTO     H
autotime = 2
twittertime = 1

# GIVEAWAY               Y   M   D   H   M  S
giveawaytime = datetime(2023, 3, 10, 20, 30, 00)
snapshot1 = datetime(2023, 2, 9, 20, 30, 00)
snapshot2 = datetime(2023, 3, 9, 20, 30, 00)
giveawaytitle = "X7 Finance 20,000 X7R Giveaway!"
giveawayinfo = "To get your name in the draw for the 20,000 X7R Giveaway, Simply mint and hold 0.1 X7D for 30 " \
               "days!\n\n" \
               "For every 0.1 X7D minted you will receive 1 entry!\n\n" \
               f"A Snapshot of minters will be taken at {snapshot1} (UTC) and again at {snapshot2} (UTC)\n\n" \
               f"The Diamond hands that have held for the entire duration will be in the draw! The more you mint," \
               " the better your chance!\n\n" \
               f"The draw will be made at {giveawaytime} (UTC)\n\nCredit: Defi Dipper!"
entryupdate = "07/01/23 17:40 UTC"
entries = [""]
tweetid = 1618166216706646018
tweetlink = "https://twitter.com/X7_Finance/status/1617660521431576576?s=20&t=pJLH-p73Qcjwz7dRuE5MCw"

# COMMANDS
modsonly = "You do not have permission from the X7 Mods to do this. #trustnoone"

commands = '**Available X7 Finance commands:**\n\n' \
        '<@1018221723650379936>\n' \
        '```/roadmap - Whats coming next' \
        '/contract - Token Contract Addresses\n' \
        '/chart - Chart Links\n' \
        '/price [token] - Coin Gecko Prices\n' \
        '/buy - Buy Links/xchange - XChange DEX Info\n' \
        '/wp - Whitepaper\n' \
        '/discount - Discount Info' \
        '/x7r - X7R Info\n' \
        '/x7dao - X7DAO Info\n' \
        '/x7101 - X7101 Info\n' \
        '/x7102 - X7102 Info\n' \
        '/x7103 - X7103 Info\n' \
        '/x7104 - X7104 Info\n' \
        '/x7105 - X7105 Info\n' \
        '/constellations - X7 Constellation Info\n' \
        '/x7d - X7Deposit Info\n' \
        '/buyevenly - A Guide to buying constellation series evenly\n' \
        '/tax - Token Tax Info\n' \
        '/mcap  - Market Cap Info\n' \
        'spaces - Twitter space Info\n' \
        '/listings - Token Listing Info\n' \
        '/swap - Xchange Details\n' \
        '/nft - NFT Details\n' \
        '/opensea - Opensea Links\n' \
        '/pioneer [id#]\n' \
        '/treasury - Treasury Details\n' \
        '/pool - Lending Pool Info\n' \
        '/loans - Loan Term Info\n' \
        '/burn - Burnt Tokens Info\n' \
        '/holders - Token Holder Info\n' \
        '/giveaway - Current Giveaway Info\n' \
        '/report [@user] [reason]\n' \
        '/x7force - Submit your twitter ID for X7Force channel```\n' \
        '<@704521096837464076>\n```/join ```\n<@159985870458322944>\n```/levels\n/rank```\n<@617037497574359050>' \
        '** - Server Currency is X7R**\n```/balance\n/withdraw\n/deposit\n/tip [@user] [$# / #x7r]```'
