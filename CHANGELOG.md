# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepa.changelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org).

<!-- CHANGELOG -->

## v1.4.0 (2025-09-26)


### Bug Fixes

- **ci**: Update GitHub Actions workflows for MkDocs deployment and release process
  ([`165e764`](https://github.com/Nicconike/Steam-Stats/commit/165e76469ed498c44504d5dbc8dd197c42e20580))

### Documentation

- Improve README badges
  ([`fca12e0`](https://github.com/Nicconike/Steam-Stats/commit/fca12e0d25c92f1f429f56800f8c6f73f8e174cf))

### Features

- **api, docs, ci, assets**: Rename internal function, add MkDocs docs, update CI and release
  workflows
  ([`03b4087`](https://github.com/Nicconike/Steam-Stats/commit/03b4087942486aa6f949939c7c2db89ddc2fc4d3))


## v1.3.2 (2025-06-26)


### Bug Fixes

- **card**: Improve screenshot mechanism to avoid any clippings of the generated cards
  ([`f9917ea`](https://github.com/Nicconike/Steam-Stats/commit/f9917ea66ac8ad4316fbea382f3c48e2a243de50))

- **template**: Improve date formatting in changelog and release notes jinja templates
  ([`484aa88`](https://github.com/Nicconike/Steam-Stats/commit/484aa88ab88d584823426d8e7e16b022f9f368db))

### Build System

- Add pytest.ini to resolve PytestDeprecationWarning
  ([`144becf`](https://github.com/Nicconike/Steam-Stats/commit/144becff6b2e81b79e3a4cc1e7d3bab258488e51))

- Update dependencies and project metadata in 'pyproject.toml'
  ([`8b02754`](https://github.com/Nicconike/Steam-Stats/commit/8b0275402a7164e64914febdce58997c56e46fbb))

### Documentation

- Improve changelog structure
  ([`f9917ea`](https://github.com/Nicconike/Steam-Stats/commit/f9917ea66ac8ad4316fbea382f3c48e2a243de50))

- Update changelog and templates for versioning
  ([`8b02754`](https://github.com/Nicconike/Steam-Stats/commit/8b0275402a7164e64914febdce58997c56e46fbb))

- **template**: Update changelog_update template to use date correctly
  ([`250695a`](https://github.com/Nicconike/Steam-Stats/commit/250695a1eef994a477a01347bb83f0b4b3b8d21a))


## v1.3.1 (2025-05-23)


### Bug Fixes

- Squashed a bug where the asset path was getting created incorrectly which broke the markdown embed
  ([`ae4e33c`](https://github.com/Nicconike/Steam-Stats/commit/ae4e33c984e08902ae42bac4a600b56a820cc300))


## v1.3.0 (2025-05-22)


### Bug Fixes

- Update assets path to resolve a bug where it was unable to find the api module
  ([`fa2afd7`](https://github.com/Nicconike/Steam-Stats/commit/fa2afd726b99526532718c65a3e6daa58dbaf870))

### Build System

- Update API URLs to use HTTPS and modify configuration files
  ([`39527ee`](https://github.com/Nicconike/Steam-Stats/commit/39527ee1b6ab6b30fe8967edf9274aa9ba8f9435))

- **deps**: Update dependabot config
  ([`19dd504`](https://github.com/Nicconike/Steam-Stats/commit/19dd50470f8a7e71b9e4500513d947fd7b61aac4))

### Documentation

- Add openssf badge
  ([`0c36f3b`](https://github.com/Nicconike/Steam-Stats/commit/0c36f3b23bfde59297022c85a1e906ce6d577f17))

### Features

- **api**: Upgrade Playwright to v1.52.0 and refactor Dockerfile
  ([`fa2afd7`](https://github.com/Nicconike/Steam-Stats/commit/fa2afd726b99526532718c65a3e6daa58dbaf870))


## v1.2.1 (2025-01-01)


### Bug Fixes

- **api**: Patch the bug for incomplete card generation for recently played games
  ([`1e306f8`](https://github.com/Nicconike/Steam-Stats/commit/1e306f8fc7e1e9f89076534202403913afde5870))

### Build System

- Update ENTRYPOINT
  ([`13508da`](https://github.com/Nicconike/Steam-Stats/commit/13508dad973bb75a72890a2917cde3ad93aa6a98))

### Documentation

- Update readme
  ([`a391a9a`](https://github.com/Nicconike/Steam-Stats/commit/a391a9aeffa7871880ca8826cbb998812241d55e))


## v1.2.0 (2024-12-16)


### Build System

- Update Dockerfile
  ([`1aee391`](https://github.com/Nicconike/Steam-Stats/commit/1aee3919d8e9cf5eb99d83252eede51adaa0e6e7))

- **deps**: Bump playwright/python ([#46](https://github.com/Nicconike/Steam-Stats/pull/46),
  [`e802e10`](https://github.com/Nicconike/Steam-Stats/commit/e802e101098a8b18bd3634c3f9bd93cef3726602))

- **deps**: Bump playwright/python from v1.46.0-jammy to v1.47.0-jammy
  ([#28](https://github.com/Nicconike/Steam-Stats/pull/28),
  [`5dd257c`](https://github.com/Nicconike/Steam-Stats/commit/5dd257c724c18c42a740455ddd88ed4b3d874e05))

- **deps**: Bump playwright/python in the docker group
  ([#39](https://github.com/Nicconike/Steam-Stats/pull/39),
  [`9863d91`](https://github.com/Nicconike/Steam-Stats/commit/9863d91117a4640936b9512a7b13e682ef4b544f))

### Documentation

- Update readme
  ([`016ee37`](https://github.com/Nicconike/Steam-Stats/commit/016ee379c0b8d3907f31ebe3f37d6cf87879d1ec))

### Features

- **card**: Add dynamic sizing for card generation for games played
  ([`9a31749`](https://github.com/Nicconike/Steam-Stats/commit/9a31749efab2fa1b9cb88a31c700bd62651d4002))


## v1.1.1 (2024-08-29)


### Bug Fixes

- Correctly display time if it is 1 min
  ([`18f7216`](https://github.com/Nicconike/Steam-Stats/commit/18f721648061f8b1c37f327a41241aa3d24c5fcb))

### Documentation

- Update changelog
  ([`effd204`](https://github.com/Nicconike/Steam-Stats/commit/effd2049c65219ef0a058e5850e723d3d2eea2c8))


## v1.1.0 (2024-08-27)


### Build System

- **deps**: Bump playwright/python from v1.44.0-jammy to v1.45.0-jammy
  ([#11](https://github.com/Nicconike/Steam-Stats/pull/11),
  [`b921e49`](https://github.com/Nicconike/Steam-Stats/commit/b921e49e248a01a9ed78b02d17dd29a888751270))

- **deps**: Bump playwright/python from v1.45.0-jammy to v1.45.1-jammy
  ([#17](https://github.com/Nicconike/Steam-Stats/pull/17),
  [`11b4aa1`](https://github.com/Nicconike/Steam-Stats/commit/11b4aa16c43545081904e2a53546a997c10e885e))

- **deps**: Bump playwright/python from v1.45.1-jammy to v1.46.0-jammy
  ([#21](https://github.com/Nicconike/Steam-Stats/pull/21),
  [`0c95106`](https://github.com/Nicconike/Steam-Stats/commit/0c951062dfc3f4325feda36bbb810f833208eb20))

### Documentation

- Fix issue templates
  ([`6a5131c`](https://github.com/Nicconike/Steam-Stats/commit/6a5131c8de26e64ab6f63f0117193cc10b7df375))

- Update readme
  ([`97d29f7`](https://github.com/Nicconike/Steam-Stats/commit/97d29f75d3fdf084b5c93825ee751282b59398c9))

- Update readme
  ([`7e8df83`](https://github.com/Nicconike/Steam-Stats/commit/7e8df8301926c1915911d0689c61f41086ab6f41))

### Features

- Update deps
  ([`89d19e7`](https://github.com/Nicconike/Steam-Stats/commit/89d19e7b4bcc0268654a7e342ac13f108c834760))


## v1.0.2 (2024-07-11)


### Bug Fixes

- Update code to gracefully handle loccountrycode var
  ([`e50ca76`](https://github.com/Nicconike/Steam-Stats/commit/e50ca76e1b6bb9582b41a347f163d84cfb26c425))


## v1.0.1 (2024-07-10)


### Bug Fixes

- Add INPUT_GH_TOKEN as a token env var
  ([`a50764c`](https://github.com/Nicconike/Steam-Stats/commit/a50764c3ecc3df05187bfce3eefbeaa0ac0178f9))


## v1.0.0 (2024-07-09)


### Documentation

- Correct changelog & pyproject
  ([`a84f81c`](https://github.com/Nicconike/Steam-Stats/commit/a84f81c82180caf45233b399799cc78125fe4a26))

### Performance Improvements

- Improve Card generation & Main Runner Script Code
  ([`1e35e04`](https://github.com/Nicconike/Steam-Stats/commit/1e35e0431dd8d8742c7c566a81ebf0f3ff29af15))

### Breaking Changes

- Major Release 🚀


## v0.1.5 (2024-06-28)


### Bug Fixes

- Correct the assertion error
  ([`16e7217`](https://github.com/Nicconike/Steam-Stats/commit/16e7217e93a8c2529b7464c91c1a12f06b9e4871))

- **card**: This commit fixes the bug to handle the scenario where the player has not played any
  games in last 2 weeks ([#6](https://github.com/Nicconike/Steam-Stats/pull/6),
  [`dee3c45`](https://github.com/Nicconike/Steam-Stats/commit/dee3c4568f4e626847f3fd9090505de7fa7956f2))

### Build System

- Missed dockerfile change
  ([`1de324b`](https://github.com/Nicconike/Steam-Stats/commit/1de324b9d28883ae0ce967c149c954a49b35cac6))

- Update dockerfile ([#6](https://github.com/Nicconike/Steam-Stats/pull/6),
  [`dee3c45`](https://github.com/Nicconike/Steam-Stats/commit/dee3c4568f4e626847f3fd9090505de7fa7956f2))

### Documentation

- Add security.md
  ([`cb5d35b`](https://github.com/Nicconike/Steam-Stats/commit/cb5d35b2f9d041651949e7d4c526c863b636a7b4))

- Move the doc files to .github
  ([`68e64f1`](https://github.com/Nicconike/Steam-Stats/commit/68e64f171877a41ea5da21f0a42afd4f14b9162e))

- Update issue templates
  ([`dc23769`](https://github.com/Nicconike/Steam-Stats/commit/dc23769b0e7f3283bb90294f67aac282c504055d))

- Update readme
  ([`94a89a3`](https://github.com/Nicconike/Steam-Stats/commit/94a89a3a023599a205ce3f2f0f7da6026551d534))

- Update readme
  ([`49c1723`](https://github.com/Nicconike/Steam-Stats/commit/49c1723637dd6414454b279004cd56e537e2c5e6))

- Update readme
  ([`3b0cdbb`](https://github.com/Nicconike/Steam-Stats/commit/3b0cdbbdcdb85b8a5d4108e0ccf17191332ac844))

### Features

- Add logging for the python scripts ([#6](https://github.com/Nicconike/Steam-Stats/pull/6),
  [`dee3c45`](https://github.com/Nicconike/Steam-Stats/commit/dee3c4568f4e626847f3fd9090505de7fa7956f2))


## v0.1.4 (2024-06-20)


### Bug Fixes

- Update main python script to remvoe setup
  ([`ebfd9e0`](https://github.com/Nicconike/Steam-Stats/commit/ebfd9e01ac097efba2f507f8948084888da51a91))

### Documentation

- Add issue templates
  ([`cffa8f9`](https://github.com/Nicconike/Steam-Stats/commit/cffa8f9e6b02afab0593c3aa86bf7c79e47d56e0))


## v0.1.3 (2024-06-19)


### Bug Fixes

- **workflow**: Test release
  ([`e8c3ddb`](https://github.com/Nicconike/Steam-Stats/commit/e8c3ddba57368f21e9c29207fcb2eb9029ef99db))


## v0.1.2 (2024-06-17)


### Bug Fixes

- Update action.yml to pull docker image
  ([`130bc91`](https://github.com/Nicconike/Steam-Stats/commit/130bc91bcc9fcc4d229f5d87fc2b05bc1472ce18))

### Build System

- Addressing the autobuild warning to use v3 for CodeQL
  ([`abc130a`](https://github.com/Nicconike/Steam-Stats/commit/abc130a2641fb29f5b3fb4ef231d059d788b7e35))


## v0.1.1 (2024-06-16)


### Bug Fixes

- Modify update_readme func to fix the bug to update readme correctly
  ([#2](https://github.com/Nicconike/Steam-Stats/pull/2),
  [`33c38a7`](https://github.com/Nicconike/Steam-Stats/commit/33c38a7d1ce619873caf828e34a62f23e5a13e5c))

### Documentation

- Update Readme
  ([`2a9d8f3`](https://github.com/Nicconike/Steam-Stats/commit/2a9d8f347bcab6d0b9746ecb9e4f3a0a65bcbf5b))

### Performance Improvements

- Remove redundancy
  ([`64cbf13`](https://github.com/Nicconike/Steam-Stats/commit/64cbf13cb3af82c3b1d2e150f3e572a6964d91ff))


## v0.1.0 (2024-06-14)


### Bug Fixes

- **workflow**: Correctly setup gpg sign
  ([`8046a1b`](https://github.com/Nicconike/Steam-Stats/commit/8046a1b6ef88048101fddf9a39ff82977afc4b02))

- **workflow**: Refactor all github workflows
  ([`effac0b`](https://github.com/Nicconike/Steam-Stats/commit/effac0b087ede665edf4c8fd3d308aca677e8353))

- **workflow**: Sign Commit
  ([`74ee9fb`](https://github.com/Nicconike/Steam-Stats/commit/74ee9fb0ca888b9c5a3be42936da3ec610596079))

- **workflow**: Update steps in workflow
  ([`143d3dc`](https://github.com/Nicconike/Steam-Stats/commit/143d3dcc246c498c3ef7b69008cd2cf654698bb5))

### Features

- **docker**: Update dockerfile & workflow
  ([`9e04f61`](https://github.com/Nicconike/Steam-Stats/commit/9e04f61fa42c44f92e4604cf0e8a7c7993174c51))

- **workflow**: Add release action & update docker
  ([`baf85c6`](https://github.com/Nicconike/Steam-Stats/commit/baf85c6f89eb2f9e8cb48163b6ce9cff40a70ea5))


## v0.0.1 (2024-06-12)
- Initial Release
