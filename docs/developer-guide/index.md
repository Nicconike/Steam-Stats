---
title: Developer Guide
description: Contributing to Steam Stats - development setup, guidelines and project structure
---

# Developer Guide :book:

Welcome to the Steam Stats developer documentation! This section is for contributors, maintainers, and anyone interested in understanding how Steam Stats works under the hood.

## Quick Start for Developers :simple-rocket:

1. **[Project Layout](project-layout.md)** - Understand the codebase structure
2. **[Local Development](local-development.md)** - Set up your development environment
3. **[Contributing](contributing.md)** - Coding standards and PR workflow
4. **[Testing](testing.md)** - Running and writing tests

## Contribution Areas :material-target:

| Area | Skills Needed | Getting Started |
|------|---------------|-----------------|
| **Core Features** | Python, Steam API | Check [open issues](https://github.com/Nicconike/Steam-Stats/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) |
| **Documentation** | Markdown, MkDocs | See [documentation issues](https://github.com/Nicconike/Steam-Stats/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation) |
| **Testing** | Python, Pytest | Review [testing guidelines](testing.md) |
| **DevOps** | Docker, GitHub Actions | Check workflow files in `.github/workflows/` |

## Understanding the Codebase :material-note-search:

Steam Stats is built with:

- **[Python 3.12+](https://docs.python.org/3.12/)**: Core application logic
- **[Playwright](https://playwright.dev/python/docs/intro)**: Rendered HTML to PNG conversion
- **[Docker](https://docs.docker.com/)**: Containerized execution environment
- **[GitHub Actions](https://docs.github.com/en/actions)**: CI/CD and user workflow automation

## Additional Resources :simple-bookstack:

- **[API Reference](../reference/index.md)**: Complete code documentation
- **[User Guide](../user-guide/index.md)**: End-user documentation
- **[Examples](../examples/index.md)**: Real-world usage examples

---

Ready to contribute? Start with the [Project Layout](project-layout.md) to understand how everything fits together!
