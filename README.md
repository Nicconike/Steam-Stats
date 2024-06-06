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
	3. Select scopes -> repo and workflow only
	4. Set a reasonable expiration date
3. **Markdown Comments:** Update the markdown file by adding the comments where the Steam Stats will be embedded to. Refer [here](#Update-Readme) to learm more.
4. **Steam ID:** You can get your 64-bit Steam id (SteamID64 - 17 digit number) by clicking on your profile name in the top right corner in steam desktop client, select "Account Details" and your Steam ID will be displayed directly under your account name
5. **Steam Custom ID:** Open the Steam desktop application, click on your profile name in the top right corner. Select "View Profile" and your custom URL will be displayed in the URL bar. From this url you will know your Steam Custom ID

The Github Actions is set to run on every Monday 12 AM IST (UTC+5:30) which you can modify to your own time as per your liking by updating it in the workflow file

```yml
schedule:
        - cron: "30 18 * * 0"
```

## Update Readme
1. Add this comment in your markdown file(Readme.md) which is for Steam User Stats
	```md
	<!-- Steam-Stats start -->
	<!-- Steam-Stats end -->
	```
2. Add below comment for Steam Workshop Stats (Optional)
	```md
	<!-- Steam-Workshop start -->
	<!-- Steam-Workshop end -->
	```

## Features
1. Steam Player Summary[^*]
2. Recently Played Games from Steam in the Last 2 Weeks
3. Steam Workshop Stats (If Available)

### Feature Flags
1. Steam User Stats (Required | Default)
	1. Steam Player Summary
	2. Steam's Recently Played Games in the last 2 weeks
		1. The Graph plot for recently played games is by default implemented in a fixed scale but if you want you can update it to be in a logarithmic scale by using this flag

			`LOG_SCALE: True`

**Example for Steam User Stats**
<!-- Steam-Stats start -->
![Steam Summary](https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_summary.png)
![Steam Summary](https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games.png)
<!-- Steam-Stats end -->

1. Steam Workshop Stats (Optional)
	1. Workshop Stats Module can be activated/used by adding this flag in the workflow file in the environment variables

		`WORKSHOP_STATS: True`

	2. This module displays the total number of Unique Visitors, Subscribers and Favorites

**Example for Steam Workshop Stats**
<!-- Steam-Workshop start -->
![Steam Summary](https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_workshop_stats.png)
<!-- Steam-Workshop end -->

## Setup with Example
After completing the steps mentioned in the [Prerequisites](#Prerequisites), you have to save all the mentioned keys(except markdown comments) like github token,api key, steamid, customid as Secrets in your Github repo's settings.

> Repo Settings -> Security -> Secrets and Variables -> Actions -> Add in Repository Secrets

If you are new to github secrets then you can checkout this doc [here](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions). And from [here](https://docs.github.com/en/actions/security-guides/automatic-token-authentication) you can learn about Github Tokens.

Sample Workflow File
```yml
name: Steam Stats

on:
    schedule:
        # Runs every Monday at 12AM IST (UTC+5:30)
        - cron: "30 18 * * 0"
    workflow_dispatch:

jobs:
    update-readme:
        name: Steam Stats
        runs-on: ubuntu-latest
        steps:
          - uses: nicconike/steam-stats@master
            with:
                STEAM_API_KEY: ${{ secrets.STEAM_API_KEY }}
                STEAM_ID: ${{ secrets.STEAM_ID }}
                STEAM_CUSTOM_ID: ${{ secrets.STEAM_CUSTOM_ID }}
```

[^*]: Unfortunately, Steam API doesn't support Web Sockets so the profile status cannot be updated as soon as it gets updated in steam profile 🥲
