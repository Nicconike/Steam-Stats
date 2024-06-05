# 🛠️Work in Progress 🚧|🚧 Please come back later⚒️
[![Steam Stats](https://github.com/Nicconike/Steam-Stats/actions/workflows/steam-stats.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/steam-stats.yml)
[![CodeQL](https://github.com/Nicconike/Steam-Stats/actions/workflows/github-code-scanning/codeql/badge.svg?branch=master)](https://github.com/Nicconike/Steam-Stats/actions/workflows/github-code-scanning/codeql)
[![Pylint](https://github.com/Nicconike/Steam-Stats/actions/workflows/pylint.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/pylint.yml)
![pylint](https://img.shields.io/badge/PyLint-10.00-brightgreen?logo=python&logoColor=white)
[![Visitor Badge](https://badges.pufler.dev/visits/nicconike/steam-stats)](https://badges.pufler.dev)

> ### From one Passionate Gamer and Developer to Another 🍻

## Prerequisites
1. **Steam Web API Key:** API key is important to fetch your account details and for that you will require a key which you can create for your account [here](https://steamcommunity.com/dev).
2. **Github API Token:**
   1. Goto your Github profile -> Settings -> Developer Settings -> Personal Access Tokens -> Tokens(Classic) or just click [here](https://github.com/settings/tokens)
   2. Generate new token -> Generate new token(classic)
   3. Select scopes -> repo and workflow ==only==
   4. Set a reasonable expiration date
3. **Steam ID:** You can get your 64-bit Steam id (SteamID64 - 17 digit number) by clicking on your profile name in the top right corner in steam desktop client, select "Account Details" and your Steam ID will be displayed directly under your account name
4. **Steam Custom ID:** Open the Steam desktop application, click on your profile name in the top right corner. Select "View Profile" and your custom URL will be displayed in the URL bar. From this url you will know your Steam Custom ID

### Features
1. Steam Player Summary[^1]
2. Recently Played Games from Steam in the Last 2 Weeks
3. Steam Workshop Stats (If Available)

<!-- Steam-Stats start -->
![Steam Summary](https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_summary.png)
![Steam Summary](https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games.png)
<!-- Steam-Stats end -->

<!-- Steam-Workshop start -->
![Steam Summary](https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_workshop_stats.png)
<!-- Steam-Workshop end -->

[^1]: Unfortunately, Steam API doesn't support Web Sockets so the profile status cannot be updated as soon as it gets updated in steam profile 🥲
