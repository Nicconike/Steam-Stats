---
title: Advanced Troubleshooting
description: Deep-dive solutions for complex Steam Stats issues beyond basic setup
---

# Advanced Troubleshooting :material-tools:

This guide covers complex issues beyond basic setup problems. For first-time setup issues, see [Verification](../getting-started/verification.md).

## GitHub Actions Permission Issues :simple-githubactions:

### Resource not accessible by integration
This error occurs when the GitHub Action lacks proper repository permissions to push commits:

**Solution 1**: Repository Settings

1. Go to **Settings** :material-arrow-right-bold-outline: **Actions** :material-arrow-right-bold-outline: **General**
2. Under **Actions permissions**, select **Allow all actions and reusable workflows**
3. Under **Workflow permissions**, select **Read repository contents and packages permissions**
4. Rerun the failed workflow

**Solution 2**: Workflow-Level Permissions (Recommended)

Add to your workflow YAML:

```yml
permissions:
    contents: read
    actions: read
```

### Organization Restrictions
If your repository is in an organization:

- Organization may have restricted GitHub Actions
- Contact org admin to enable Actions for your repository
- Check if third-party actions are allowed or not

## Steam API Issues & Limitations :octicons-blocked-16:

### Player Summary Endpoint Problems
The Steam Player Summary API endpoint can be unreliable:

- **Rate Limiting (429 Responses)** Steam enforces these API limits:
    - **100,000 calls per day** per API key
    - **1 call per second** sustained rate
    - **Steam Stats** implements automatic retry logic respecting `Retry-After` headers,
    - And retries up to 5 times before failing

- **Server Unresponsiveness**: Requests use a 25s connect and 30s read timeout. If Steam doesn’t respond, retries occur automatically.

### Authentication Failures
If you see a log entry like: `ERROR - HTTP error: 401 Client Error: Unauthorized for url: https://api.steampowered.com/`

This indicates that your Steam Web API key was rejected by Steam. To resolve:

- **Invalid API key**: Verify `STEAM_API_KEY` in your repository secrets
- **Key revoked**: If you regenerated your key, update the secret accordingly
- **[Limited account](https://help.steampowered.com/en/faqs/view/71D3-35C2-AD96-AA3A)**: Ensure your Steam account has atleast $5+ in purchases to generate an API key

### Missing or Incomplete Data
- **Privacy settings**: Fields you’ve set to Private in Steam’s profile privacy will not be returned by the API
- **Regional restrictions**: Some games or data may not appear due to regional blocks
- **Game info**: The `gameextrainfo` field appears only when you’re actively in-game at the time of the API call

## PNG Generation Issues :octicons-image-16:

### Playwright Rendering Challenges
Steam Stats uses Playwright (Chromium) for HTML to PNG conversion. Common issues include:

- **Browser Engine Changes**
    - **Originally used Firefox** for rendering HTML to PNG
    - **Switched to Chromium** for better consistency and performance

- **Screenshot Capture Issues**
    - **Selector path errors**: Changes in card HTML structure can break element targeting
    - **Timing issues**: Screenshots may be captured before the page fully renders; functions are now async to mitigate this
    - **Memory constraints**: Chromium requires approximately 500 MB of RAM in the GitHub Actions container

### Common PNG Problems

**Cards Not Generating**

- **Selector path errors**: HTML structure changes break screenshot capture
- **Async timing**: Screenshots taken before content fully loads
- **Memory constraints**: Playwright requires sufficient container memory

**Visual Quality Problems**

- **Font rendering**: Uses web-safe fonts only
- **Character encoding**: Non-Latin characters may not display correctly
- **Resolution**: High-DPI rendering optimized for GitHub display

### Cards Not Updating in README
- **Browser cache**: Hard refresh (:material-keyboard-f5:) to bypass local cache or reopen browser
- **GitHub CDN**: May take a min or so for images to update
- **File paths**: Confirm PNGs are committed to the correct path (e.g., `assets/`)

## Workshop Statistics Issues :octicons-tools-16:

### Web Scraping Limitations
Workshop stats are obtained by scraping Steam Workshop pages:

- **Page structure changes**: Steam’s HTML updates can break scraping logic
- **Request blocks**: High-frequency scraping may trigger anti-bot measures
- **Custom ID required**: Ensure your `STEAM_CUSTOM_ID` matches your profile URL slug exactly

### Zero or Missing Workshop Data
- **New items**: Statistics may not populate immediately after publishing
- **Visibility settings**: Only public workshop items are counted
- **Content type filtering**: Hidden workshop items might get excluded from totals

## Debugging and Logging :octicons-bug-16:

### Log Levels
Steam Stats uses Python's logging module:

- **INFO**: Normal operation messages *(default)*
- **WARNING**: Rate limiting retries and non-critical issues
- **ERROR**: Failed requests (HTTP errors) and critical issues

### Reviewing Workflow Logs
Look for these success indicators:
```sh
INFO - Retrieved Steam User Data
INFO - Generated Card for Steam User Data
INFO - Retrieved Recently Played Games Data
INFO - Generated Card for Recently Played Games
INFO - Steam Stats updated
```

If Workshop is enabled:
```sh
INFO - Retrieved Workshop Data
INFO - Generated Card for Workshop Stats
```

Missing log entries indicate where the process failed

## Performance Considerations :material-crosshairs-question:

### Slow Execution (>30 seconds)
Normal execution takes around 15 - 20 seconds. Slow performance may indicate:

- **Steam API latency**: Geographic server performance varies
- **Playwright startup**: Container initialization can add a few seconds
- **Retry attempts**: Multiple failed requests add delay

### Memory and Resource Limits

- **GitHub Actions limits**: 7GB RAM, 14GB disk space available (which is irrelevant here ofcourse)
- **Chromium**: Consumes ~500 MB of RAM
- **Sequential API calls**: Calls are made one after another, not in parallel

## Recovery Procedures :material-clover-outline:

### Complete Reset
1. Delete generated PNG files from your repository
2. Remove `.github/workflows/steam-stats.yml`
3. Clear comment markers from README.md
4. Delete repository secrets & variables (`STEAM_API_KEY`, `STEAM_ID`, `STEAM_CUSTOM_ID`)
5. Start fresh with [Quick Start Guide](../setup.md)

### Partial Recovery
1. Cancel any running workflows in the Actions tab
2. Review logs for specific errors
3. Correct secrets or configuration as needed
4. Manually trigger the workflow again

---

*For basic setup issues, see [Verification](../getting-started/verification.md). For configuration questions, see [Configuration](config.md).*
