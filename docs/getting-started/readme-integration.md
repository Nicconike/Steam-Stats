---
title: README Integration
description: How to embed Steam Stats cards in your README.md
---

# README Integration

## Insert README Markers

Place these markdown comments in your `README.md` where you want the cards to appear, as Steam Stats inserts cards between these specific comments.

### User Summary & Recently Played Games
```md
<!-- Steam-Stats start -->
<!-- Steam-Stats end -->
```

### Workshop Stats
```md
<!-- Steam-Workshop start -->
<!-- Steam-Workshop end -->
```

!!! warning "Comment Order Matters"

    - Both comment pairs are **mandatory**
    - Workshop comments must follow Steam-Stats comments or the action will fail
