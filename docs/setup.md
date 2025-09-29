---
title: Quick Start Guide
description: Get Steam Stats running in minutes
---

# Quick Start Guide :simple-quicklook:

Steam Stats automatically generates and embeds Steam gaming statistic cards in your GitHub profile README.

## Go Live Immediately

1. Verify your [Prerequisites](getting-started/prerequisites.md)
2. Obtain your [Steam API Key](getting-started/steam-web-api.md)
3. Locate your [Steam IDs](getting-started/steam-id.md)
4. Configure the [GitHub Action](getting-started/github-action.md)
5. Insert the [README markers](getting-started/readme-integration.md) and [Verify](getting-started/verification.md)

Once complete, check out the generated cards in your README and explore the [User Guide](user-guide/index.md) for customization and troubleshooting.

## Step 1: Prerequisites
Before you begin, ensure you have:
- GitHub account with repository access
- Steam account with $5+ purchase history
- Basic familiarity with GitHub Actions

[Detailed Prerequisites](getting-started/prerequisites.md)

## Step 2: Get Steam Web API Key
1. Visit [Steam Developer Portal](https://steamcommunity.com/dev/apikey)
2. Enter your domain (can be anything, e.g., `localhost`)
3. Copy your API key

[Complete API Setup Guide](getting-started/steam-web-api.md)

## Step 3: Find Your Steam IDs
You'll need both your Steam ID and Custom ID:
- **Steam ID**: 17-digit number from Account Details
- **Custom ID**: From your profile URL

[Steam ID Location Guide](getting-started/steam-id.md)

## Step 4: Configure GitHub Secrets
Add these to your repository secrets:

- `STEAM_API_KEY`: Your API key from Step 2
- `STEAM_ID`: Your Steam ID (as variable)
- `STEAM_CUSTOM_ID`: Your Custom ID (as variable)

[GitHub Actions Setup](getting-started/github-action.md)

## Step 5: Add Workflow File
Create `.github/workflows/steam-stats.yml`:

```yml
name: Steam Stats
on:
  workflow_dispatch:
  schedule:
    # Runs every Monday at 12 AM IST (UTC+5:30)
    - cron: "30 18 * * 0"
jobs:
  steam-stats:
    name: Steam Stats
    runs-on: ubuntu-latest
    steps:
      - name: Steam Stats
        uses: nicconike/steam-stats@master
        with:
          STEAM_API_KEY: ${{ secrets.STEAM_API_KEY }}
          STEAM_ID: ${{ vars.STEAM_ID }}
          STEAM_CUSTOM_ID: ${{ vars.STEAM_CUSTOM_ID }}
          WORKSHOP_STATS: True # Optional
          LOG_SCALE: True # Optional
```

## Step 6: Add README Markers
In your `README.md`, add:
```md
<!-- Steam-Stats start -->
<!-- Steam-Stats end -->

<!-- Steam-Workshop start -->
<!-- Steam-Workshop end -->
```

[README Integration Guide](getting-started/readme-integration.md)

## Verification
Run your workflow manually to test. Check:

- [ ] Workflow completes successfully
- [ ] PNG files appear in your repository
- [ ] README displays the generated cards

[Troubleshooting Guide](user-guide/troubleshooting.md)
