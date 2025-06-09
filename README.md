# Steam Stats📶
[![Steam Stats](https://github.com/Nicconike/Steam-Stats/actions/workflows/steam-stats.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/steam-stats.yml)
[![Release](https://github.com/Nicconike/Steam-Stats/actions/workflows/release.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/release.yml)
[![CodeQL & Pylint](https://github.com/Nicconike/Steam-Stats/actions/workflows/codeql.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/codeql.yml)
[![Bandit](https://github.com/Nicconike/Steam-Stats/actions/workflows/bandit.yml/badge.svg)](https://github.com/Nicconike/Steam-Stats/actions/workflows/bandit.yml)
![Pylint](https://img.shields.io/badge/Pylint-9.99-greenyellow?logo=python)
[![codecov](https://codecov.io/gh/Nicconike/Steam-Stats/graph/badge.svg?token=SC5P7CS1BW)](https://codecov.io/gh/Nicconike/Steam-Stats)
![Docker Image Size](https://img.shields.io/docker/image-size/nicconike/steam-stats?logo=docker&label=Docker%20Image&link=https%3A%2F%2Fhub.docker.com%2Fr%2Fnicconike%2Fsteam-stats)
![Docker Pulls](https://img.shields.io/docker/pulls/nicconike/steam-stats?logo=docker&label=Docker%20Pulls&link=https%3A%2F%2Fhub.docker.com%2Fr%2Fnicconike%2Fsteam-stats)
![GitHub Release](https://img.shields.io/github/v/release/nicconike/steam-stats)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fgithub.com%2FNicconike%2FSteam-Stats%2Fblob%2Fmaster%2Fpyproject.toml%3Fraw%3Dtrue)
![PyPI - Version](https://img.shields.io/pypi/v/steam-stats)
![GitHub License](https://img.shields.io/github/license/nicconike/Steam-Stats)
[![Visitor Badge](https://badges.pufler.dev/visits/nicconike/steam-stats)](https://badges.pufler.dev)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/9965/badge)](https://www.bestpractices.dev/projects/9965)
[![wakatime](https://wakatime.com/badge/user/018e538b-3f55-4e8e-95fa-6c3225418eed/project/018e62a4-056d-49fd-babd-b079ee94859f.svg)](https://wakatime.com/badge/user/018e538b-3f55-4e8e-95fa-6c3225418eed/project/018e62a4-056d-49fd-babd-b079ee94859f)

> ### From one Passionate Gamer and Developer to Another 🍻
***
## Prerequisites
1. **Steam Web API Key:** API key is important to fetch your account details and for that you will require a key which you can create for your account [here](https://steamcommunity.com/dev)
2. **Markdown Comments:** Update the markdown file by adding the comments where the Steam Stats will be embedded to. Refer [here](#Update-Readme) to learn more.
3. **Steam ID:** You can get your 64-bit Steam id (SteamID64 - 17 digit number) by clicking on your profile name in the top right corner in steam desktop client, select "Account Details" and your Steam ID will be displayed directly under your account name
4. **Steam Custom ID:** Open the Steam desktop application, click on your profile name in the top right corner. Select _View Profile_ and your custom URL will be displayed in the URL bar. From this url you will know your Steam Custom ID

The Github Actions is set to run on every Monday 12 AM IST (UTC+5:30) which you can modify to your own time as per your liking by updating it in the workflow file

```yml
schedule:
        - cron: "30 18 * * 0"
```
> [!IMPORTANT]
> Please don't forget any of the steps mentioned in the prerequisites else the Github Action will not work.
> Also, make sure that you have set the country correctly in your Steam Account.
>
> You can refer the [Steam Stats Wiki](https://github.com/Nicconike/Steam-Stats/wiki) if you have any questions related to any of the steps mentioned in [Prerequisites](#Prerequisites).
***
## Samples (From my [Steam Account](https://steamcommunity.com/id/nicconike/))
**Example for Steam User Stats**
<!-- Steam-Stats start -->
![Steam Summary](https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_summary.png)
![Recently Played Games](https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games.png)
<!-- Steam-Stats end -->

**Example for Steam Workshop Stats**
<!-- Steam-Workshop start -->
![Steam Workshop Stats](https://github.com/Nicconike/Steam-Stats/blob/master/assets/steam_workshop_stats.png)
<!-- Steam-Workshop end -->
***
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

> [!CAUTION]
> The `Steam-Stats` marker should be placed before the `Steam-Workshop` markers if you are using both.
***
## Features
1. Steam Player Summary[^1]
2. Recently Played Games from Steam in the Last 2 Weeks
3. Steam Workshop Stats (If Applicable)

### Feature Flags
1. Steam User Stats (Required | Default)
	1. Steam Player Summary
	2. Steam's Recently Played Games in the last 2 weeks
		1. The Graph plot for recently played games is by default implemented in a fixed linear scale but if you want you can update it to be in a logarithmic scale by using this flag in your workflow: `LOG_SCALE: True`
		2. When `LOG_SCALE` is `False`

			![Recently Played Games](https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games(linear).png)
		3. When `LOG_SCALE` is `True`

			![Recently Played Games](https://github.com/Nicconike/Steam-Stats/blob/master/assets/recently_played_games(logarithmic).png)
2. Steam Workshop Stats (Optional)
	1. Workshop Stats Module can be used by adding this flag in your workflow file in the environment variables: `WORKSHOP_STATS: True`
	2. This module displays the total number of Unique Visitors, Subscribers and Favorites for your Steam Workshop Items
***
## Setup with Example
After completing the steps mentioned in the [Prerequisites](#Prerequisites), you have to save all the mentioned keys(except markdown comments) like Steam API Key, Steam-ID, Custom-ID as Secrets in your Github repo's settings.

> Repo Settings -> Security -> Secrets and Variables -> Actions -> Add in Repository Secrets

If you are new to **Github Secrets** then you can checkout this official doc [here](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).

**Sample Workflow File**

`steam-stats.yml`

```yaml
name: Steam Stats

on:
  push:
    branches: master
    schedule:
      # Runs every Monday at 12AM IST (UTC+5:30)
      - cron: "30 18 * * 0"
    workflow_dispatch:

jobs:
  steam-stats:
    name: Steam Stats
    runs-on: ubuntu-latest
    steps:
      - uses: nicconike/steam-stats@master
        with:
          STEAM_API_KEY: ${{ secrets.STEAM_API_KEY }} # Created Steam API key env var
          STEAM_ID: ${{ vars.STEAM_ID }} # Steam ID env var
          STEAM_CUSTOM_ID: ${{ vars.STEAM_CUSTOM_ID }} # Custom ID env var
          WORKSHOP_STATS: True # Optional
          LOG_SCALE: True # Optional
```

Checkout this real time usage example in a github repo from [here](https://github.com/Nicconike/Nicconike?tab=readme-ov-file#gaming-) and also the github actions [workflow file](https://github.com/Nicconike/Nicconike/blob/master/.github/workflows/steam-stats.yml).

***
## Contributions

Star⭐ and Fork🍴 the Repo to start with your feature request(or bug) and experiment with the project to implement whatever Idea you might have and sent the Pull Request through 🤙

Please refer [Contributing.md](https://github.com/Nicconike/Steam-Stats/blob/master/.github/CONTRIBUTING.md) to get to know how to contribute to this project.
And thank you for considering to contribute.

***
## Credits

- **Actions**
	- **[GitHub Actions](https://github.com/actions)**
	- **[Python Semantic Release](https://github.com/python-semantic-release/python-semantic-release)**
	- **[Docker](https://github.com/docker)**
	- **[CodeQL](https://github.com/github/codeql-action)**
	- **[Codecov](https://github.com/codecov/codecov-action)**

***
## Support💙
If you are using this project and are really happy with it, then there are few ways to support me so that I can keep doing what I like doing:
- Credit in your readme where you use this action
- Drop a follow!😁
- Starring and Sharing the project
- Donations through [GitHub Sponsers](https://github.com/sponsors/Nicconike) or whichever platform you like. So, that I can create more projects like these and play more games🎮🎧

#### **Thanks!🫡**
***
Created with 🐍 & ❤️ by [Nicco](https://x.com/Nicco_nike)

[^1]: Unfortunately, Steam Web API doesn't support Web Sockets so the profile status cannot be updated in real time as it gets updated in steam profile 🥲
