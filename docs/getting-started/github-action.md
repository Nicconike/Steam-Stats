---
title: GitHub Action Setup
description: Configure the Steam Stats GitHub Action in your repository
---

# GitHub Action Workflow

## Create the Workflow File

In your repository, create the workflow directory and file:

1. **Navigate to your repository** on GitHub
2. **Create a new file** at: `.github/workflows/steam-stats.yml`
3. **Add the following content**:
    ```yml
    name: Steam Stats
    permissions: # Least privilege for GitHub Actions
      contents: read
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

## Enable Log Scale for Recently Played Games

By default, the Recently Played Games chart uses a linear Y-axis. To visualize games with vastly different playtimes more effectively, enable logarithmic scaling:

1. Add `LOG_SCALE: True` under your `with:` inputs (as shown above).
2. Commit and push your workflow file.

Linear Scale Example:

![Linear Scale Example](../assets/recently_played_games(linear).png)

Log Scale Example:

![Log Scale Example](../assets/recently_played_games(log).png)

## Workflow Explanation

- **`schedule`**: Automatically runs weekly every Monday midnight at 12 AM IST *(default)*
- **`workflow_dispatch`**: Allows you to manually trigger the workflow
- **`uses: Nicconike/Steam-Stats@master`**: Runs the Steam Stats action which fetches data, generates cards and commits them
- **Inputs**:
    - **`STEAM_API_KEY`**: Your Steam Web API key (from repository secrets)
    - **`STEAM_ID`** and **`STEAM_CUSTOM_ID`**: Your numeric SteamID64 and custom ID
    - **`WORKSHOP_STATS`**: `True` to enable Workshop stats *(optional)*
    - **`LOG_SCALE`**: `True` to use logarithmic scale on the Recently Played Games chart *(optional)*
---

No additional commit steps are required, Steam Stats automatically updates your README
