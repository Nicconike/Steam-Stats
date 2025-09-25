---
title: Scheduling Options
description: Configure how often Steam Stats runs via cron expressions
---

# Scheduling Options :material-robot-happy-outline:

Steam Stats uses GitHub Actions’ `schedule` event with cron syntax to run automatically at defined times.

## How Scheduled Events Work

In your workflow YAML, the `schedule` block defines one or more cron expressions. GitHub Actions triggers the workflow when the expression matches the set time.

```yml
on:
    schedule:
        - cron: "<cron-expression>"
```

Cron expressions consist of five space-separated fields:

| Field         | Allowed Values       | Description                |
|---------------|----------------------|----------------------------|
| Minute        | 0–59                 | Minute of the hour         |
| Hour          | 0–23                 | Hour of the day (UTC)      |
| Day of month  | 1–31                 | Day of the month           |
| Month         | 1–12 or JAN–DEC      | Month of the year          |
| Day of week   | 0–6 or SUN–SAT       | Day of the week (0=Sunday) |

!!! info
    All times are in UTC, regardless of your repository or local timezone.

## Common Cron Examples

| Schedule                   | Cron Expression     | Description                         |
|----------------------------|---------------------|-------------------------------------|
| Every minute               | `* * * * *`         | Triggers every minute               |
| Hourly                     | `0 * * * *`         | At minute 0 of every hour           |
| Daily at midnight UTC      | `0 0 * * *`         | Every day at 00:00 UTC              |
| Weekly on Monday 00:00     | `0 0 * * 1`         | Mondays at 00:00 UTC                |
| Weekly on Monday 05:30 IST | `30 18 * * 0`       | Mondays at 00:00 IST (UTC+5:30)     |
| Monthly on 1st at 00:00    | `0 0 1 * *`         | First day of month at 00:00 UTC     |

For more, see [Crontab Guru Examples](https://crontab.guru/examples.html).

## Default Steam Stats Schedule

The default schedule in the Quick Start is:
```yml
on:
    schedule:
        # Runs every Monday at 00:00 IST (18:30 UTC on Sunday)
        - cron: "30 18 * * 0"
```

## Customizing Your Schedule

1. Edit the `cron` expression in `.github/workflows/steam-stats.yml`.
2. Commit and push; GitHub Actions will pick up the change.

### Sample Schedules

- Daily at 12:00 UTC
    ```yml
    on:
        schedule:
            - cron: "0 12 * * *"
    ```

- Every 6 hours
    ```yml
    on:
        schedule:
            - cron: "0 */6 * * *"
    ```

- Weekdays at 08:00 UTC
    ```yml
    on:
        schedule:
            - cron: "0 8 * * 1-5"
    ```

## Advanced Tips

- **Multiple schedules**: You can list multiple cron entries.
- **Comments**: Precede cron entries with comments for clarity.
- **Validation**: Use [Crontab Guru](https://crontab.guru) to test your expressions.
- **GitHub Docs**: Detailed reference at [GitHub Scheduled Events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

---

*Return to the [User Guide](index.md) or continue to [Configuration](config.md).*
