# 🛠️Work in Progress 🚧|🚧 Please come back later⚒️
[![Steam Stats](https://github.com/Nicconike/Steam-Stats/actions/workflows/steam-stats.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/steam-stats.yml)
[![Release](https://github.com/Nicconike/Steam-Stats/actions/workflows/release.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/release.yml)
[![Code Analysis](https://github.com/Nicconike/Steam-Stats/actions/workflows/codeql.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/codeql.yml)
![pylint](https://img.shields.io/badge/PyLint-9.91-yellow?logo=python&logoColor=white)
[![codecov](https://codecov.io/gh/Nicconike/Steam-Stats/graph/badge.svg?token=SC5P7CS1BW)](https://codecov.io/gh/Nicconike/Steam-Stats)
![Docker Image Size](https://img.shields.io/docker/image-size/nicconike/steam-stats?logo=docker&label=Docker%20Image&link=https%3A%2F%2Fhub.docker.com%2Fr%2Fnicconike%2Fsteam-stats)
![Docker Pulls](https://img.shields.io/docker/pulls/nicconike/steam-stats?logo=docker&label=Docker%20Pulls&link=https%3A%2F%2Fhub.docker.com%2Fr%2Fnicconike%2Fsteam-stats)
![GitHub Release](https://img.shields.io/github/v/release/nicconike/steam-stats)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fgithub.com%2FNicconike%2FSteam-Stats%2Fblob%2Fmaster%2Fpyproject.toml%3Fraw%3Dtrue)
![GitHub repo size](https://img.shields.io/github/repo-size/nicconike/steam-stats?logo=github&label=Repo%20Size)
![GitHub License](https://img.shields.io/github/license/nicconike/Steam-Stats)
[![Visitor Badge](https://badges.pufler.dev/visits/nicconike/steam-stats)](https://badges.pufler.dev)

> ### From one Passionate Gamer and Developer to Another 🍻

## Prerequisites
1. **Steam Web API Key:** API key is important to fetch your account details and for that you will require a key which you can create for your account [here](https://steamcommunity.com/dev)
2. **Github API Token:**
	1. Goto your Github profile -> Settings -> Developer Settings -> Personal Access Tokens -> Tokens(Classic) or just click [here](https://github.com/settings/tokens)
	2. Generate new token -> Generate new token(classic)
	3. Select scopes -> repo and workflow only
	4. Set a reasonable expiration date
3. **Markdown Comments:** Update the markdown file by adding the comments where the Steam Stats will be embedded to. Refer [here](#Update-Readme) to learn more.
4. **Steam ID:** You can get your 64-bit Steam id (SteamID64 - 17 digit number) by clicking on your profile name in the top right corner in steam desktop client, select "Account Details" and your Steam ID will be displayed directly under your account name
5. **Steam Custom ID:** Open the Steam desktop application, click on your profile name in the top right corner. Select _View Profile_ and your custom URL will be displayed in the URL bar. From this url you will know your Steam Custom ID

The Github Actions is set to run on every Monday 12 AM IST (UTC+5:30) which you can modify to your own time as per your liking by updating it in the workflow file

```yml
schedule:
        - cron: "30 18 * * 0"
```
> [!IMPORTANT]
> Please don't forget any of the steps mentioned in the prerequisites else the Github Action will not work.
>
> You can refer the [Steam Stats Wiki](https://github.com/Nicconike/Steam-Stats/wiki) if you have any questions related to any of the steps mentioned in [Prerequisites](#Prerequisites).

## Samples (From my [Steam Account](https://steamcommunity.com/id/nicconike/))
**Example for Steam User Stats**
<!-- Steam-Stats start -->
![Steam Summary](https://github.com/nicconike/steam-stats/blob/master/assets/steam_summary.png)
<div class='recently-played-games'><p>No games played recently</p></div>
<!-- Steam-Stats end -->

**Example for Steam Workshop Stats**
<!-- Steam-Workshop start -->
![Steam Workshop Stats](https://github.com/nicconike/steam-stats/blob/master/assets/steam_workshop_stats.png)
<!-- Steam-Workshop end -->

## Update README
1. Add below comment in your markdown file for Steam User Stats
	```md
	<!-- Steam-Stats start -->
	<!-- Steam-Stats end -->
	```
2. Add below comment for Steam Workshop Stats (Optional)
	```md
	<!-- Steam-Workshop start -->
	<!-- Steam-Workshop end -->
	```
3. Don't forget to add these comments in your readme file or wherever you want to display your steam stats, because without the comments the readme will not get updated

## Features
1. Steam Player Summary[^*]
2. Recently Played Games from Steam in the Last 2 Weeks
3. Steam Workshop Stats (If Available)

### Feature Flags
1. Steam User Stats (Required | Default)
	1. Steam Player Summary
	2. Steam's Recently Played Games in the last 2 weeks
		1. The Graph plot for recently played games is by default implemented in a fixed scale but if you want you can update it to be in a logarithmic scale by using this flag: `LOG_SCALE: True`
		2. When `LOG_SCALE` is `False`

			![Recently Played Games](https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games(linear).png)
		3. When `LOG_SCALE` is `True`

			![Recently Played Games](https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games(logarithmic).png)
2. Steam Workshop Stats (Optional)
	1. Workshop Stats Module can be activated/used by adding this flag in the workflow file in the environment variables: `WORKSHOP_STATS: True`
	2. This module displays the total number of Unique Visitors, Subscribers and Favorites for your Steam Workshop Items

## Setup with Example
After completing the steps mentioned in the [Prerequisites](#Prerequisites), you have to save all the mentioned keys(except markdown comments) like Github Token,API Key, Steam-ID, Custom-ID as Secrets in your Github repo's settings.

> Repo Settings -> Security -> Secrets and Variables -> Actions -> Add in Repository Secrets

If you are new to **Github Secrets** then you can checkout this doc [here](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions). And from [here](https://docs.github.com/en/actions/security-guides/automatic-token-authentication) you can learn about **Github Tokens**.

**Sample Workflow File**

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
                STEAM_ID: ${{ vars.STEAM_ID }}
                STEAM_CUSTOM_ID: ${{ vars.STEAM_CUSTOM_ID }}
```

## Contributing

Please refer [Contributing.md](https://github.com/Nicconike/Steam-Stats/blob/master/.github/CONTRIBUTING.md) to get to know how to contribute to this project.
And thank you for considering to contribute.

## Credits

- **GitHub Actions**
	- [Checkout](https://github.com/actions/checkout)
	- [Setup-Python](https://github.com/actions/setup-python)
	- [Cache](https://github.com/actions/cache)
	- [Upload-Artifact](https://github.com/actions/upload-artifact)
	- [Create-Github-App-Token](https://github.com/actions/create-github-app-token)
	- [CodeQL-Action](https://github.com/github/codeql-action)
	- [Pylint-Github-Action](https://github.com/Silleellie/pylint-github-action)
	- [Python-Semantic-Release](https://github.com/python-semantic-release/python-semantic-release)
	- [Setup-Buildx-Action](https://github.com/docker/setup-buildx-action)
	- [Login-Action](https://github.com/docker/login-action)
	- [Metadata-Action](https://github.com/docker/metadata-action)
	- [Build-Push-Action](https://github.com/docker/build-push-action)
	- [Scout-Action](https://github.com/docker/scout-action)
- **Styles**
	- [Progress Bar Design](https://github.com/Nicconike/Steam-Stats/blob/master/assets/style.css) - [Ana Tudor](https://codepen.io/thebabydino)



Created with Game Sense & ❤️ by [Nicco](https://github.com/Nicconike)

[^*]: Unfortunately, Steam Web API doesn't support Web Sockets so the profile status cannot be updated in real time as it gets updated in steam profile 🥲
