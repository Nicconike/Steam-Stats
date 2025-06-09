# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- version list -->

## v1.3.1 (2025-05-23)

### Bug Fixes

- Squashed a bug where the asset path was getting created incorrectly which broke the markdown embed ([`ae4e33c`](https://github.com/Nicconike/Steam-Stats/commit/ae4e33c984e08902ae42bac4a600b56a820cc300))

refactor: Implement utility functions for GitHub interactions and asset path management

test: Add unit test functions for utils helper functions

### Refactoring

- Update changelog configuration and templates ([`01dd95c`](https://github.com/Nicconike/Steam-Stats/commit/01dd95c920b1e6c3764d5252274ddbf19094fe3b))
- Modified the changelog settings in `pyproject.toml` to include new options for templates and insertion flags.
- Enhanced test cases in `test_card.py` and `test_steam_workshop.py` to improve error handling and logging assertions.
- Added a new changelog template in `templates/CHANGELOG.md.j2` to standardize the format of release notes.

### Chores

- Update Pylint Badge ([`c827595`](https://github.com/Nicconike/Steam-Stats/commit/c82759562764affbcf0803100e286952d898a427))
- Update Steam Stats ([`a18d0a6`](https://github.com/Nicconike/Steam-Stats/commit/a18d0a6406a25bff4af0dae24bcb44f92464b325))
- Update Steam Stats ([`900825a`](https://github.com/Nicconike/Steam-Stats/commit/900825af8c368588ea8f4733b3bd48b17c68a5f6))

## v1.3.0 (2025-05-22)

### Features

- **api**: Upgrade Playwright to v1.52.0 and refactor Dockerfile
  ([`fa2afd7`](https://github.com/Nicconike/Steam-Stats/commit/fa2afd726b99526532718c65a3e6daa58dbaf870))

- Updated Dockerfile to use Playwright v1.52.0 with pinned digest. - Refactored environment variable
  settings and user creation in Dockerfile. - Simplified installation of Python dependencies and
  removed unnecessary asset directory creation.

fix: Update assets path to resolve a bug where it was unable to find the api module

- Updated asset paths to reflect new directory structure. - Changed browser launch from Firefox to
  Chromium for consistency. - Adjusted test cases to cover new error handling scenarios and ensure
  robustness.

refactor: Enhance card generation logic and error handling

- Introduced `format_playtime` function to format playtime into a human-readable format. - Added
  `generate_progress_bar` function to create HTML for game progress bars. - Improved error handling
  in `get_element_bounding_box` and `html_to_png` functions. - Updated card generation functions to
  utilize new asset directory structure.

chore: Update dependencies and improve test coverage

- Updated dependencies in pyproject.toml and requirements.txt for compatibility. - Enhanced test
  coverage for card generation and workshop fetching functions. - Added new tests for error handling
  and edge cases in workshop stats fetching. - Refactored tests to improve readability and
  maintainability.

### Continuous Integration

- Bump python-semantic-release/python-semantic-release
  ([#52](https://github.com/Nicconike/Steam-Stats/pull/52),
  [`002cee5`](https://github.com/Nicconike/Steam-Stats/commit/002cee559910821d76c0b6a11efffcebc27dc2ff))

Bumps the github-actions group with 1 update:
  [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release).

Updates `python-semantic-release/python-semantic-release` from 9.15.2 to 9.16.1

- Bump python-semantic-release/python-semantic-release
  ([#53](https://github.com/Nicconike/Steam-Stats/pull/53),
  [`8f7efb9`](https://github.com/Nicconike/Steam-Stats/commit/8f7efb9740e76b5f43b66ba7ccb0c02027b43510))

Bumps the github-actions group with 1 update:
Updates `python-semantic-release/python-semantic-release` from 9.16.1 to 9.17.0

- Bump the github-actions group across 1 directory with 3 updates
  ([#60](https://github.com/Nicconike/Steam-Stats/pull/60),
  [`e0f7aaf`](https://github.com/Nicconike/Steam-Stats/commit/e0f7aaf98084855597e75ea6ee13312d3143054c))

Bumps the github-actions group with 3 updates in the / directory:
Updates `python-semantic-release/python-semantic-release` from 9.19.0 to 9.21.0
Updates `sigstore/cosign-installer` from 3.8.0 to 3.8.1
Updates `docker/scout-action` from 1.16.1 to 1.16.3

- Bump the github-actions group with 2 updates
  ([#55](https://github.com/Nicconike/Steam-Stats/pull/55),
  [`7886706`](https://github.com/Nicconike/Steam-Stats/commit/7886706a5b6005572519ff0b8a5d76509c49a147))

Bumps the github-actions group with 2 updates:
Updates `python-semantic-release/python-semantic-release` from 9.17.0 to 9.19.0
Updates `sigstore/cosign-installer` from 3.7.0 to 3.8.0

- Update pylint workflow
  ([`f55040f`](https://github.com/Nicconike/Steam-Stats/commit/f55040fdad59f2b002d256eb20c5fa130a188c65))

### Build System

- Update API URLs to use HTTPS and modify configuration files
  ([`39527ee`](https://github.com/Nicconike/Steam-Stats/commit/39527ee1b6ab6b30fe8967edf9274aa9ba8f9435))

- **deps**: Update dependabot config
  ([`19dd504`](https://github.com/Nicconike/Steam-Stats/commit/19dd50470f8a7e71b9e4500513d947fd7b61aac4))

### Chores

- Update Pylint Badge
  ([`90608b8`](https://github.com/Nicconike/Steam-Stats/commit/90608b804e7cdd5e68a7c8ebf47544d0e16d226d))

- Update Pylint Badge
  ([`5f85685`](https://github.com/Nicconike/Steam-Stats/commit/5f856852db6758c7f2a1f180ff9de03806b1c2c9))

- Update Pylint Badge
  ([`470b845`](https://github.com/Nicconike/Steam-Stats/commit/470b845d9027acee503ba770ea60a0b9644305b1))

- Update Pylint Badge
  ([`4163886`](https://github.com/Nicconike/Steam-Stats/commit/4163886f3e03f7190651d28c977dbe52f57b3794))

- Update Steam Stats
  ([`e22f0fa`](https://github.com/Nicconike/Steam-Stats/commit/e22f0fa6733337dfac0b81b195ed752d3ace532f))

- Update Steam Stats
  ([`a1bd732`](https://github.com/Nicconike/Steam-Stats/commit/a1bd732b2bad64c907718173f61d5f3bea16f994))

- Update Steam Stats
  ([`a2669b3`](https://github.com/Nicconike/Steam-Stats/commit/a2669b3a5618e48b89de68263d54d425270048a9))

- Update Steam Stats
  ([`49b0274`](https://github.com/Nicconike/Steam-Stats/commit/49b02747c13bec2fe15ab383dc6225f6becbccbb))

- Update Steam Stats
  ([`d66f783`](https://github.com/Nicconike/Steam-Stats/commit/d66f783b887b265415bbffb7fe85b3e5b142a3ce))

- Update Steam Stats
  ([`2175e57`](https://github.com/Nicconike/Steam-Stats/commit/2175e57c1f9bc1a2c75c66e3c91ae1626f82517d))

- Update Steam Stats
  ([`75f640f`](https://github.com/Nicconike/Steam-Stats/commit/75f640fb827ef71dad821d1d1d25a35791eb4a12))

- Update Steam Stats
  ([`debba3f`](https://github.com/Nicconike/Steam-Stats/commit/debba3f280500918f4206220931692c65a9d9e83))

- Update Steam Stats
  ([`b15953a`](https://github.com/Nicconike/Steam-Stats/commit/b15953a2706587904a11efc09c0f0503a39245a0))

- Update Steam Stats
  ([`b1bbc75`](https://github.com/Nicconike/Steam-Stats/commit/b1bbc759b2835d81301e5e32fbd180badf4dd387))

- Update Steam Stats
  ([`33ed342`](https://github.com/Nicconike/Steam-Stats/commit/33ed342d4713462f00a0f96010fa63d5d022c109))

- Update Steam Stats
  ([`53a0805`](https://github.com/Nicconike/Steam-Stats/commit/53a08054e0a3bd901c1a068aeacecfee13adacf7))

- Update Steam Stats
  ([`739bba0`](https://github.com/Nicconike/Steam-Stats/commit/739bba015108664d1137b97ecd0fae94a3809ec7))

- Update Steam Stats
  ([`e44ae22`](https://github.com/Nicconike/Steam-Stats/commit/e44ae22f46a55a3ae34f1dedd11a406fad547121))

- Update Steam Stats
  ([`b0b4fc0`](https://github.com/Nicconike/Steam-Stats/commit/b0b4fc0eb39d2a018ab5c449b72fbc1cf0e2c5ad))

- Update Steam Stats
  ([`ebd3aca`](https://github.com/Nicconike/Steam-Stats/commit/ebd3acaada7fc8cd8c895ef3392618aca1136aef))

- Update Steam Stats
  ([`7878200`](https://github.com/Nicconike/Steam-Stats/commit/787820079b9a934e4e52fe14f84a957a09be448f))

- Update Steam Stats
  ([`1dd8b55`](https://github.com/Nicconike/Steam-Stats/commit/1dd8b55f3fe7468ad86279b58966a1409f567221))

- Update Steam Stats
  ([`1266863`](https://github.com/Nicconike/Steam-Stats/commit/1266863b0cfa7a5df3dcc1e46f6782ceb945d78f))

- Update Steam Stats
  ([`4f9398f`](https://github.com/Nicconike/Steam-Stats/commit/4f9398f7aa4b67e287c5d80dc66837ff48c55c1a))

- Update Steam Stats
  ([`54104ff`](https://github.com/Nicconike/Steam-Stats/commit/54104ff559fb2c343c1b20f49b7e9c4c15d3c0d0))


### Documentation

- Add openssf badge
  ([`0c36f3b`](https://github.com/Nicconike/Steam-Stats/commit/0c36f3b23bfde59297022c85a1e906ce6d577f17))

Signed-off-by: Nicco <38905025+Nicconike@users.noreply.github.com>


### Refactoring

- Resolve pylint warning and refactor unit tests code
  ([`e626afb`](https://github.com/Nicconike/Steam-Stats/commit/e626afb6e76a704e794d5591833f353b841007bc))


## v1.2.1 (2025-01-01)

### Bug Fixes

- **api**: Patch the bug for incomplete card generation for recently played games
  ([`1e306f8`](https://github.com/Nicconike/Steam-Stats/commit/1e306f8fc7e1e9f89076534202403913afde5870))

### Build System

- Update ENTRYPOINT
  ([`13508da`](https://github.com/Nicconike/Steam-Stats/commit/13508dad973bb75a72890a2917cde3ad93aa6a98))

### Chores

- Update Pylint Badge
  ([`7dbcb74`](https://github.com/Nicconike/Steam-Stats/commit/7dbcb744e5d64e55cae99ab1f72793be271c1b6e))

- Update Steam Stats
  ([`be45d6b`](https://github.com/Nicconike/Steam-Stats/commit/be45d6b1e19f39c144a5287091a6b73505a958d6))

- Update Steam Stats
  ([`80c5c63`](https://github.com/Nicconike/Steam-Stats/commit/80c5c632d2bfed7ecd8ac6d273567b4b8a964fb3))

- Update Steam Stats
  ([`666037e`](https://github.com/Nicconike/Steam-Stats/commit/666037e92073127fecabf5ced9d393ccffcaab9d))

### Continuous Integration

- Bump the github-actions group with 2 updates
  ([#48](https://github.com/Nicconike/Steam-Stats/pull/48),
  [`ed2359a`](https://github.com/Nicconike/Steam-Stats/commit/ed2359a7ec9176ca82ab38b8a5df2d7d8e5aacdb))

Bumps the github-actions group with 2 updates:
- Updates `python-semantic-release/python-semantic-release` from 9.15.1 to 9.15.2
- Updates `docker/scout-action` from 1.15.1 to 1.16.1

- Fix docker workflow for signing published docker images
  ([`fd1536b`](https://github.com/Nicconike/Steam-Stats/commit/fd1536bbc34dc99212e2f8548cb1ba926445e4a9))

- Trigger docker workflow
  ([`12ffc28`](https://github.com/Nicconike/Steam-Stats/commit/12ffc2858c5d4e0fc702be84338baef75e7e4ed1))

- Update docker step for release
  ([`4aaf432`](https://github.com/Nicconike/Steam-Stats/commit/4aaf43249572cb931d55b054e810cb42870692fa))

### Documentation

- Update readme
  ([`a391a9a`](https://github.com/Nicconike/Steam-Stats/commit/a391a9aeffa7871880ca8826cbb998812241d55e))


## v1.2.0 (2024-12-16)

### Build System

- **deps**: Bump playwright/python ([#46](https://github.com/Nicconike/Steam-Stats/pull/46),
  [`e802e10`](https://github.com/Nicconike/Steam-Stats/commit/e802e101098a8b18bd3634c3f9bd93cef3726602))

Bumps the docker group with 1 update in the / directory:
Updates `playwright/python` from v1.48.0-jammy to v1.49.1-jammy

- **deps**: Bump playwright/python from v1.46.0-jammy to v1.47.0-jammy
  ([#28](https://github.com/Nicconike/Steam-Stats/pull/28),
  [`5dd257c`](https://github.com/Nicconike/Steam-Stats/commit/5dd257c724c18c42a740455ddd88ed4b3d874e05))

Bumps playwright/python from v1.46.0-jammy to v1.47.0-jammy

- **deps**: Bump playwright/python in the docker group
  ([#39](https://github.com/Nicconike/Steam-Stats/pull/39),
  [`9863d91`](https://github.com/Nicconike/Steam-Stats/commit/9863d91117a4640936b9512a7b13e682ef4b544f))

Bumps the docker group with 1 update:
Updates `playwright/python` from v1.47.0-jammy to v1.48.0-jammy

### Chores

- Add code time
  ([`993e03a`](https://github.com/Nicconike/Steam-Stats/commit/993e03a8c7cf299b1f93469cd3bf4376c0c48622))

- Update dependabot labelling
  ([`d996556`](https://github.com/Nicconike/Steam-Stats/commit/d9965561ffc6c02389d9479190f743ff35b3958c))

- Update Dockerfile
  ([`88a03d2`](https://github.com/Nicconike/Steam-Stats/commit/88a03d2dadc5f81029b2dfad303f72e403c15960))

Signed-off-by: Nicco <38905025+Nicconike@users.noreply.github.com>

- Update encoding to utf-8
  ([`1a4ed62`](https://github.com/Nicconike/Steam-Stats/commit/1a4ed628e452861f8ff62e447c19d00478e8112e))

- Update requirements.txt
  ([`ca3957f`](https://github.com/Nicconike/Steam-Stats/commit/ca3957f601f2d8fffb1d9f126be5d4a521313634))

Signed-off-by: Nicco <38905025+Nicconike@users.noreply.github.com>

- Update Steam Stats
  ([`7bb2318`](https://github.com/Nicconike/Steam-Stats/commit/7bb23182bbf5a972c197dbd12041c2f1688fdbe1))

- Update Steam Stats
  ([`04817ea`](https://github.com/Nicconike/Steam-Stats/commit/04817ea0bce56ba6245ae49ecae041d69f27c5c8))

- Update Steam Stats
  ([`003833d`](https://github.com/Nicconike/Steam-Stats/commit/003833d28ab9e45ce9d20c7cc1bf9bc0cd833e2d))

- Update Steam Stats
  ([`1e201dd`](https://github.com/Nicconike/Steam-Stats/commit/1e201dde9ac5750dda6fb08ce58074a4335b37dd))

- Update Steam Stats
  ([`011d122`](https://github.com/Nicconike/Steam-Stats/commit/011d122b657de1c9827befd4edfd7e8d09fb55f7))

- Update Steam Stats
  ([`00f67b7`](https://github.com/Nicconike/Steam-Stats/commit/00f67b79eebcc9f4d97314043bdefa4b3478463c))

- Update Steam Stats
  ([`5d90fee`](https://github.com/Nicconike/Steam-Stats/commit/5d90fee70240026278e13344586c113c94fdf59d))

- Update Steam Stats
  ([`4c5d4e4`](https://github.com/Nicconike/Steam-Stats/commit/4c5d4e4366ac6fdc9288cce5001e418dfd5eb0db))

- Update Steam Stats
  ([`b4632cf`](https://github.com/Nicconike/Steam-Stats/commit/b4632cfc68f4c337f4f3a6595d2f4b0d37d27f20))

- Update Steam Stats
  ([`a1d2684`](https://github.com/Nicconike/Steam-Stats/commit/a1d268494ff486dd273e443947d7c5656335d88a))

- Update Steam Stats
  ([`29538f1`](https://github.com/Nicconike/Steam-Stats/commit/29538f1d6a7064fc344b9113ae3a81a6ef2641db))

- Update Steam Stats
  ([`ca8d621`](https://github.com/Nicconike/Steam-Stats/commit/ca8d6214a7eb9db51a2325e11e9f1a4cab70d243))

- Update Steam Stats
  ([`2106a0c`](https://github.com/Nicconike/Steam-Stats/commit/2106a0c5cf0005f7e227103445f19f52b8a00350))

- Update Steam Stats
  ([`543f270`](https://github.com/Nicconike/Steam-Stats/commit/543f270192df07bfbadb5e22090e4e860004910c))

- Update Steam Stats
  ([`2ad7a40`](https://github.com/Nicconike/Steam-Stats/commit/2ad7a4080647400d7d677cbcd852a3d4daee8368))

- Update Steam Stats
  ([`5eda95a`](https://github.com/Nicconike/Steam-Stats/commit/5eda95a3d810780472a12728d31b0085afc5946c))

- Update Steam Stats
  ([`07bc6db`](https://github.com/Nicconike/Steam-Stats/commit/07bc6dbda9350ae43c6a049e4f97a2e006de33c6))

- Update Steam Stats
  ([`6c0aa5d`](https://github.com/Nicconike/Steam-Stats/commit/6c0aa5d6f5a19832e55e3302a568bf148871d1f4))

- **deps**: Bump pipdeptree in the python-packages group
  ([#26](https://github.com/Nicconike/Steam-Stats/pull/26),
  [`3746a3e`](https://github.com/Nicconike/Steam-Stats/commit/3746a3e33a2af13daf8f6c614fbe4149bce1aa78))

Bumps the python-packages group with 1 update:
Updates `pipdeptree` from 2.23.1 to 2.23.3

- **deps**: Bump playwright in the python-packages group
  ([#29](https://github.com/Nicconike/Steam-Stats/pull/29),
  [`88b80f7`](https://github.com/Nicconike/Steam-Stats/commit/88b80f72656f5f239cec9c43196fc3530b9e6b37))

Bumps the python-packages group with 1 update:
Updates `playwright` from 1.46.0 to 1.47.0

- **deps**: Bump pytest-cov in the python-packages group
  ([#40](https://github.com/Nicconike/Steam-Stats/pull/40),
  [`ac7b580`](https://github.com/Nicconike/Steam-Stats/commit/ac7b580d8de5897b04c4bdf7752b74f0d9f461d4))

Bumps the python-packages group with 1 update:
Updates `pytest-cov` from 5.0.0 to 6.0.0

- **deps**: Bump the python-packages group across 1 directory with 2 updates
  ([#38](https://github.com/Nicconike/Steam-Stats/pull/38),
  [`7a4f10a`](https://github.com/Nicconike/Steam-Stats/commit/7a4f10a75fba71205d9b33c955e139bf5b3c3d26))

Bumps the python-packages group with 2 updates in the / directory:
  [playwright](https://github.com/Microsoft/playwright-python) and
  [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release).

Updates `playwright` from 1.47.0 to 1.48.0
Updates `python-semantic-release` from 9.9.0 to 9.12.0

- **deps**: Bump the python-packages group with 2 updates
  ([#24](https://github.com/Nicconike/Steam-Stats/pull/24),
  [`bf9a9ad`](https://github.com/Nicconike/Steam-Stats/commit/bf9a9ad934ede9466ebf0e0f7ec8706bd03eb9b4))

Bumps the python-packages group with 2 updates:
Updates `python-semantic-release` from 9.8.7 to 9.8.8
Updates `pylint` from 3.2.6 to 3.2.7

- **deps**: Bump the python-packages group with 2 updates
  ([#30](https://github.com/Nicconike/Steam-Stats/pull/30),
  [`176857e`](https://github.com/Nicconike/Steam-Stats/commit/176857e500805a83b336753549b926e90ca977eb))

Bumps the python-packages group with 2 updates:
Updates `pipdeptree` from 2.23.3 to 2.23.4
Updates `pylint` from 3.2.7 to 3.3.0

- **deps**: Bump the python-packages group with 2 updates
  ([#32](https://github.com/Nicconike/Steam-Stats/pull/32),
  [`d0ea93b`](https://github.com/Nicconike/Steam-Stats/commit/d0ea93bcb2672574b0540cf41650233cec7a034f))

Bumps the python-packages group with 2 updates:
Updates `python-semantic-release` from 9.8.8 to 9.9.0
Updates `pylint` from 3.3.0 to 3.3.1

### Continuous Integration

- Bump docker/scout-action in the github-actions group
  ([#27](https://github.com/Nicconike/Steam-Stats/pull/27),
  [`b6cbdcd`](https://github.com/Nicconike/Steam-Stats/commit/b6cbdcd11566b03a1da3dbca776d1e241dced546))

Bumps the github-actions group with 1 update:
Updates `docker/scout-action` from 1.13.0 to 1.14.0

- Bump python-semantic-release/python-semantic-release
  ([#25](https://github.com/Nicconike/Steam-Stats/pull/25),
  [`cdf9ee1`](https://github.com/Nicconike/Steam-Stats/commit/cdf9ee1d149a59720d4174158cc970069a018bd5))

Bumps the github-actions group with 1 update:
Updates `python-semantic-release/python-semantic-release` from 9.8.7 to 9.8.8

- Bump python-semantic-release/python-semantic-release
  ([#31](https://github.com/Nicconike/Steam-Stats/pull/31),
  [`e6a9601`](https://github.com/Nicconike/Steam-Stats/commit/e6a96018f8fa84fbce78d3f1e535c0861666976d))

Bumps the github-actions group with 1 update:
Updates `python-semantic-release/python-semantic-release` from 9.8.8 to 9.9.0

- Bump python-semantic-release/python-semantic-release
  ([#33](https://github.com/Nicconike/Steam-Stats/pull/33),
  [`92099f7`](https://github.com/Nicconike/Steam-Stats/commit/92099f7bc18519bf0c1e8fb705a345fcd2f89b95))

Bumps the github-actions group with 1 update:
Updates `python-semantic-release/python-semantic-release` from 9.9.0 to 9.10.0

- Bump the github-actions group across 1 directory with 2 updates
  ([#36](https://github.com/Nicconike/Steam-Stats/pull/36),
  [`299ff5e`](https://github.com/Nicconike/Steam-Stats/commit/299ff5ebb4efe0fb29e189126733ebbf283df4f4))

Bumps the github-actions group with 2 updates in the / directory:
Updates `python-semantic-release/python-semantic-release` from 9.10.0 to 9.12.0
Updates `docker/scout-action` from 1.14.0 to 1.15.0

- Bump the github-actions group across 1 directory with 3 updates
  ([#45](https://github.com/Nicconike/Steam-Stats/pull/45),
  [`5cca0a4`](https://github.com/Nicconike/Steam-Stats/commit/5cca0a40250d69d031c801d7ee0e1a7ecc203cc1))

Bumps the github-actions group with 3 updates in the / directory:
Updates `codecov/codecov-action` from 4 to 5
Updates `python-semantic-release/python-semantic-release` from 9.12.0 to 9.15.1
Updates `docker/scout-action` from 1.15.0 to 1.15.1

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

### Chores

- Update Pylint Badge
  ([`5069ff6`](https://github.com/Nicconike/Steam-Stats/commit/5069ff69ceef51ce495c61d929d9a27a11596fb5))

- Update Steam Stats
  ([`a87541f`](https://github.com/Nicconike/Steam-Stats/commit/a87541f58d6a67e350e2843e08e8504f0963d049))

### Continuous Integration

- Update release action workflow
  ([`6ec2fb7`](https://github.com/Nicconike/Steam-Stats/commit/6ec2fb7de459205e944d6c0b94de8aaacf127ed2))

### Documentation

- Update changelog
  ([`effd204`](https://github.com/Nicconike/Steam-Stats/commit/effd2049c65219ef0a058e5850e723d3d2eea2c8))


## v1.1.0 (2024-08-27)

### Build System

- **deps**: Bump playwright/python from v1.44.0-jammy to v1.45.0-jammy
  ([#11](https://github.com/Nicconike/Steam-Stats/pull/11),
  [`b921e49`](https://github.com/Nicconike/Steam-Stats/commit/b921e49e248a01a9ed78b02d17dd29a888751270))

Bumps playwright/python from v1.44.0-jammy to v1.45.0-jammy.

- **deps**: Bump playwright/python from v1.45.0-jammy to v1.45.1-jammy
  ([#17](https://github.com/Nicconike/Steam-Stats/pull/17),
  [`11b4aa1`](https://github.com/Nicconike/Steam-Stats/commit/11b4aa16c43545081904e2a53546a997c10e885e))

Bumps playwright/python from v1.45.0-jammy to v1.45.1-jammy.

- **deps**: Bump playwright/python from v1.45.1-jammy to v1.46.0-jammy
  ([#21](https://github.com/Nicconike/Steam-Stats/pull/21),
  [`0c95106`](https://github.com/Nicconike/Steam-Stats/commit/0c951062dfc3f4325feda36bbb810f833208eb20))

Bumps playwright/python from v1.45.1-jammy to v1.46.0-jammy.

### Chores

- Add codecov.yml
  ([`d3162d2`](https://github.com/Nicconike/Steam-Stats/commit/d3162d2531c4e71271f5a11a854865d68f56b17a))

- Add deps
  ([`5332ac7`](https://github.com/Nicconike/Steam-Stats/commit/5332ac79797cc124ecbfd2581a74e07704deb1ca))

- Update Pylint Badge
  ([`a10a3e4`](https://github.com/Nicconike/Steam-Stats/commit/a10a3e405854d309820a23179ff69306138bbf0d))

- Update Pylint Badge
  ([`d8569b5`](https://github.com/Nicconike/Steam-Stats/commit/d8569b56822c7449d485cbb108ac36326bb5f2bf))

- Update Pylint Badge
  ([`7e0d189`](https://github.com/Nicconike/Steam-Stats/commit/7e0d189e39428b62863a1452a40ba568bbdd2a9b))

- Update Steam Stats
  ([`be667aa`](https://github.com/Nicconike/Steam-Stats/commit/be667aa7930561a89ce2b533e3bfd07116795641))

- Update Steam Stats
  ([`49c5cd3`](https://github.com/Nicconike/Steam-Stats/commit/49c5cd30d85d867585837a33abb8962ae77a86c8))

- Update Steam Stats
  ([`3b789e8`](https://github.com/Nicconike/Steam-Stats/commit/3b789e8f8ed225a1d79e0cc7a806225eb56c483f))

- Update Steam Stats
  ([`0455eac`](https://github.com/Nicconike/Steam-Stats/commit/0455eac516102089b8646af8d58573300111a40c))

- Update Steam Stats
  ([`c9ea827`](https://github.com/Nicconike/Steam-Stats/commit/c9ea827cf3137395436faa609ab350ab736b348d))

- Update Steam Stats
  ([`709bcca`](https://github.com/Nicconike/Steam-Stats/commit/709bcca35cde3b822c62abb45fb2bf58a27ab767))

- Update Steam Stats
  ([`995cd06`](https://github.com/Nicconike/Steam-Stats/commit/995cd0650a14edf67833272abb8faf76d522234e))

- Update Steam Stats
  ([`c6518c0`](https://github.com/Nicconike/Steam-Stats/commit/c6518c0ad6632efd6179a09f75e5090ebfa9eec8))

- Update Steam Stats
  ([`9fd6f75`](https://github.com/Nicconike/Steam-Stats/commit/9fd6f75dca99524515e971a3c498ebde4039ea81))

- Update Steam Stats
  ([`de3df19`](https://github.com/Nicconike/Steam-Stats/commit/de3df1964e486d33a6bbb443691a357569adc446))

- Update Steam Stats
  ([`b19b0a2`](https://github.com/Nicconike/Steam-Stats/commit/b19b0a24f4f6fb03dcd268339592c5e721b51df1))

- Update Steam Stats
  ([`a86df94`](https://github.com/Nicconike/Steam-Stats/commit/a86df944732710d0bbb7a2484af377b8a96cdc43))

- Update Steam Stats
  ([`11b3b1c`](https://github.com/Nicconike/Steam-Stats/commit/11b3b1c21746f3601298b499cdbe0251f80b9bef))

- Update Steam Stats
  ([`5a55403`](https://github.com/Nicconike/Steam-Stats/commit/5a554036eaf4565707d36f16d09307a28805bb8a))

- Update Steam Stats
  ([`e369cc8`](https://github.com/Nicconike/Steam-Stats/commit/e369cc8babd44eca4924f72794ecd5c6c90dc55a))

- Update Steam Stats
  ([`f29280c`](https://github.com/Nicconike/Steam-Stats/commit/f29280c68a04dfdeb5809c8cf238d428a5f523be))

- Update Steam Stats
  ([`086b5cc`](https://github.com/Nicconike/Steam-Stats/commit/086b5cc40117de74efdc79ea549b9e9c2d1fac1a))

- Update Steam Stats
  ([`d1fd260`](https://github.com/Nicconike/Steam-Stats/commit/d1fd2608e0f33a2f84c14b66df2d3b82c295fb33))

- Update Steam Stats
  ([`26c391a`](https://github.com/Nicconike/Steam-Stats/commit/26c391acfd9ac98c442a15c799645f3c1b0a8894))

- Update Steam Stats
  ([`ff4553a`](https://github.com/Nicconike/Steam-Stats/commit/ff4553acc2ced8a7f65ccf536b5f3bc4bad898af))

- Update Steam Stats
  ([`d22e120`](https://github.com/Nicconike/Steam-Stats/commit/d22e1203b85180bcfc62990f7bdf90894162cb51))

- Update Steam Stats
  ([`75b1155`](https://github.com/Nicconike/Steam-Stats/commit/75b11554e368291e508c7812837c84efdb179f52))

- Update Steam Stats
  ([`7b0cabd`](https://github.com/Nicconike/Steam-Stats/commit/7b0cabd7e5753e98633e098fe5d17c4ec3255c2e))

- **deps**: Bump pipdeptree in the python-packages group
  ([#13](https://github.com/Nicconike/Steam-Stats/pull/13),
  [`458ca97`](https://github.com/Nicconike/Steam-Stats/commit/458ca97d4dfa88c0478db91202e3abd86cc7a9e7))

Bumps the python-packages group with 1 update:
Updates `pipdeptree` from 2.23.0 to 2.23.1

- **deps**: Bump playwright in the python-packages group
  ([#16](https://github.com/Nicconike/Steam-Stats/pull/16),
  [`3c0ed89`](https://github.com/Nicconike/Steam-Stats/commit/3c0ed89d73ea13de1dc831928d8f0e6906218ccc))

Bumps the python-packages group with 1 update:
Updates `playwright` from 1.45.0 to 1.45.1

- **deps**: Bump playwright in the python-packages group
  ([#20](https://github.com/Nicconike/Steam-Stats/pull/20),
  [`ae20223`](https://github.com/Nicconike/Steam-Stats/commit/ae202234a8bff6a64de623f45f4ec39c037148da))

Bumps the python-packages group with 1 update:
Updates `playwright` from 1.45.1 to 1.46.0

- **deps**: Bump the python-packages group with 2 updates
  ([#14](https://github.com/Nicconike/Steam-Stats/pull/14),
  [`2065c52`](https://github.com/Nicconike/Steam-Stats/commit/2065c525c0a661cd7aa7a72e9f924677be71fd45))

Bumps the python-packages group with 2 updates:
Updates `python-semantic-release` from 9.8.5 to 9.8.6
Updates `pylint` from 3.2.5 to 3.2.6

- **deps**: Bump the python-packages group with 3 updates
  ([#23](https://github.com/Nicconike/Steam-Stats/pull/23),
  [`c04058f`](https://github.com/Nicconike/Steam-Stats/commit/c04058f0b8adaee8980c38fb56f890d051668d8c))

Bumps the python-packages group with 3 updates:

Updates `pygithub` from 2.3.0 to 2.4.0
Updates `python-semantic-release` from 9.8.6 to 9.8.7
Updates `pytest-asyncio` from 0.23.8 to 0.24.0

### Continuous Integration

- Bump docker/scout-action ([#19](https://github.com/Nicconike/Steam-Stats/pull/19),
  [`5b2469e`](https://github.com/Nicconike/Steam-Stats/commit/5b2469e48f678d5e2c08ef4d0835ba87f7a4d05f))

Bumps the github-actions group with 1 update in the / directory:
  [docker/scout-action](https://github.com/docker/scout-action).

Updates `docker/scout-action` from 1.11.0 to 1.13.0

- Bump python-semantic-release/python-semantic-release

Updates `python-semantic-release/python-semantic-release` from 9.8.6 to 9.8.7

- Bump the github-actions group with 2 updates

Updates `python-semantic-release/python-semantic-release` from 9.8.5 to 9.8.6
Updates `docker/scout-action` from 1.10.0 to 1.11.0

- Bump python-semantic-release/python-semantic-release

Updates `python-semantic-release/python-semantic-release` from 9.8.3 to 9.8.5

- Update all workflow to not get triggered with a bot commit
  ([`635fdb8`](https://github.com/Nicconike/Steam-Stats/commit/635fdb83be125c8a4318e87dd900132151013948))

- Update release.yml
  ([`49f9d54`](https://github.com/Nicconike/Steam-Stats/commit/49f9d5467f601e750b56afe905ee028d140e0fa9))

- Update workflow
  ([`0b9e7a8`](https://github.com/Nicconike/Steam-Stats/commit/0b9e7a8ba49b5407a7b296e63874eb2e91e6fe94))

- Update workflow to use App token
  ([`5008b26`](https://github.com/Nicconike/Steam-Stats/commit/5008b26427cd5fdfba21ae0281df786f09298ee8))

- Update workflows
  ([`4ec9226`](https://github.com/Nicconike/Steam-Stats/commit/4ec922697cf68f2d218c54736a39220cedb83fee))

### Documentation

- Update readme
  ([`97d29f7`](https://github.com/Nicconike/Steam-Stats/commit/97d29f75d3fdf084b5c93825ee751282b59398c9))

- Update readme
  ([`7e8df83`](https://github.com/Nicconike/Steam-Stats/commit/7e8df8301926c1915911d0689c61f41086ab6f41))

### Features

- Update deps
  ([`89d19e7`](https://github.com/Nicconike/Steam-Stats/commit/89d19e7b4bcc0268654a7e342ac13f108c834760))

### Refactoring

- Handle exceptions in steam_workshop.py using handle_request_exception
  ([`6a5131c`](https://github.com/Nicconike/Steam-Stats/commit/6a5131c8de26e64ab6f63f0117193cc10b7df375))

docs: fix issue templates

test: 94% codecov for steam_workshop.py

- Optimize card.py code
  ([`e5ee0a8`](https://github.com/Nicconike/Steam-Stats/commit/e5ee0a81387ef42771702bb9008f69e33af50ec6))

### Testing

- 99% codecov for main.py
  ([`a63e3c6`](https://github.com/Nicconike/Steam-Stats/commit/a63e3c6041a0e347e35676f631c7b17a1f181db8))

- 99% codecov for main.py
  ([`6c645c6`](https://github.com/Nicconike/Steam-Stats/commit/6c645c6e2ea0743394a6618f72083a90f74cdb93))

- Address bandit reports, remove assert
  ([`55ceaf5`](https://github.com/Nicconike/Steam-Stats/commit/55ceaf5e834488a7fddd6861f11fa4f09204dc1c))

- Fix test_main
  ([`8796ced`](https://github.com/Nicconike/Steam-Stats/commit/8796ced84ea3b76964e8e28028ab52be5641dca6))

- Improve codecov for main.py
  ([`83e02e4`](https://github.com/Nicconike/Steam-Stats/commit/83e02e447b3772734743c3f3d4b8dbf11c2abb48))

- Update test_main.py
  ([`a2edba9`](https://github.com/Nicconike/Steam-Stats/commit/a2edba9b33a830e4e689fc7160368fa956e793c1))

- Update test_main.py
  ([`a10bd98`](https://github.com/Nicconike/Steam-Stats/commit/a10bd9805520069cb3e0ce4dac3867932a959b20))


## v1.0.2 (2024-07-11)

### Bug Fixes

- Update code to gracefully handle loccountrycode var
  ([`e50ca76`](https://github.com/Nicconike/Steam-Stats/commit/e50ca76e1b6bb9582b41a347f163d84cfb26c425))

### Chores

- **deps**: Bump the python-packages group with 2 updates

Updates `playwright` from 1.44.0 to 1.45.0
Updates `python-semantic-release` from 9.8.3 to 9.8.5

### Continuous Integration

- Use token in steam stats workflow
  ([`2101012`](https://github.com/Nicconike/Steam-Stats/commit/2101012f7facb26a9ca0e0edc1c93a43cd4551dd))


## v1.0.1 (2024-07-10)

### Bug Fixes

- Add INPUT_GH_TOKEN as a token env var
  ([`a50764c`](https://github.com/Nicconike/Steam-Stats/commit/a50764c3ecc3df05187bfce3eefbeaa0ac0178f9))

### Chores

- Update Pylint Badge
  ([`500c087`](https://github.com/Nicconike/Steam-Stats/commit/500c087a61ddddc9d61ece26b23ded382f0f8c30))


## v1.0.0 (2024-07-09)

### Breaking Changes

- Major Release 🚀

### Continuous Integration

- Correct scout scan step
  ([`700840d`](https://github.com/Nicconike/Steam-Stats/commit/700840d2935e82a92815444cb39d10465c7f10af))

- Correct the docker workflow for tags
  ([`b64b7d1`](https://github.com/Nicconike/Steam-Stats/commit/b64b7d1aed04032859e9c02fb53ed43be8632ab0))

- Correct the pylint badge generation step
  ([`50be3f4`](https://github.com/Nicconike/Steam-Stats/commit/50be3f4fec1646f695202b78124961b85af0edfb))

- Move app token step at first
  ([`77cff48`](https://github.com/Nicconike/Steam-Stats/commit/77cff483c697a19f0e8f8c113f98ea60de5c5176))

- Pylint workflow should workflow if github actions bot does a commit
  ([`b958eea`](https://github.com/Nicconike/Steam-Stats/commit/b958eea2ba16d6fd684ac685cfedb4b37326114e))

- Revert change
  ([`1b03955`](https://github.com/Nicconike/Steam-Stats/commit/1b03955877beecaf444e2d613ecb6ce1e95da5ce))

- Update badge url & codeql workflow
  ([`ee23446`](https://github.com/Nicconike/Steam-Stats/commit/ee23446bf6b43c6929816beb8fa1c99aa98b8807))

- Update docker action
  ([`82bf032`](https://github.com/Nicconike/Steam-Stats/commit/82bf032ab6e9b19ebd3ffc463f68a1710ecd1bfb))

- Update pylint badge generation
  ([`17dc2ce`](https://github.com/Nicconike/Steam-Stats/commit/17dc2ce4f0b06fd9212fcf21cb0525153fc7d196))

- Update pylint workflow
  ([`11097f3`](https://github.com/Nicconike/Steam-Stats/commit/11097f3c1ba1c074cee36e04ecfdacd2633100db))

- Update pylint workflow to commit to protected branch
  ([`c38fe71`](https://github.com/Nicconike/Steam-Stats/commit/c38fe7152f59a1dc16384a63be21aa9e1631fce3))

- Update release workflow
  ([`28afc5a`](https://github.com/Nicconike/Steam-Stats/commit/28afc5a79cfa898331253dbddc5fa44d8e8bd921))

- Update scoring for pylint badge
  ([`25fa44d`](https://github.com/Nicconike/Steam-Stats/commit/25fa44dfe840dae5dcc64124a3b1ff4ec2c1b015))

- Update workflow
  ([`74c12c4`](https://github.com/Nicconike/Steam-Stats/commit/74c12c488febc0a51b34f76c7bae72e28a0ad5ba))

- Update workflows to check for github actor
  ([`74e18a3`](https://github.com/Nicconike/Steam-Stats/commit/74e18a34e25ec67ff23ce70e6d7b696f82e2ca0c))

- Use custom pylint job instead of actions
  ([`ad37826`](https://github.com/Nicconike/Steam-Stats/commit/ad37826430dbe0ef308cb2fda461327f504c7ff8))

### Documentation

- Correct changelog & pyproject
  ([`a84f81c`](https://github.com/Nicconike/Steam-Stats/commit/a84f81c82180caf45233b399799cc78125fe4a26))

### Performance Improvements

- Improve Card generation & Main Runner Script Code
  ([`1e35e04`](https://github.com/Nicconike/Steam-Stats/commit/1e35e0431dd8d8742c7c566a81ebf0f3ff29af15))

BREAKING CHANGE: Major Release 🚀

### Chores

- Update Pylint Badge
  ([`860b652`](https://github.com/Nicconike/Steam-Stats/commit/860b6523d552a29a488591bff0101184586f6e07))

- Update Steam Stats
  ([`984bfbf`](https://github.com/Nicconike/Steam-Stats/commit/984bfbfc121bd306b7af09baee69f34720042fce))

- Update Steam Stats
  ([`112176b`](https://github.com/Nicconike/Steam-Stats/commit/112176b0c93a5c7240fec84f7ad17d96491ab4f6))

- Update Steam Stats
  ([`bb5458c`](https://github.com/Nicconike/Steam-Stats/commit/bb5458c979a8bf370fe7e159956c249cc151eed5))

- Update Steam Stats
  ([`cc9f5fd`](https://github.com/Nicconike/Steam-Stats/commit/cc9f5fdab23f84973466a663c5d94063554cb047))

- Update Steam Stats
  ([`b2f031e`](https://github.com/Nicconike/Steam-Stats/commit/b2f031e57467f9fa951527e0158ba8a7899cd00a))

- **deps**: Bump pylint in the python-packages group
Updates `pylint` from 3.2.3 to 3.2.5

### Testing

- Improve code cov for main script to 95%
  ([`17383b6`](https://github.com/Nicconike/Steam-Stats/commit/17383b698613632351b16a3fc57aec4aac8f3989))

- Improve codecov for card script to 84%
  ([`81d5f89`](https://github.com/Nicconike/Steam-Stats/commit/81d5f89eba3be0f68b2f142c8dd9c273d5d205be))

- Increase code coverage for main script
  ([`f0a7f52`](https://github.com/Nicconike/Steam-Stats/commit/f0a7f52e9f143c48f9fe2686c9e488a106fad5e1))

- Update test_steam_workshop.py for 100% coverage
  ([`72c964f`](https://github.com/Nicconike/Steam-Stats/commit/72c964faa4e7b7ce8838899554105324dd308709))


## v0.1.5 (2024-06-28)

### Bug Fixes

- Correct the assertion error
  ([`16e7217`](https://github.com/Nicconike/Steam-Stats/commit/16e7217e93a8c2529b7464c91c1a12f06b9e4871))

### Build System

- Missed dockerfile change
  ([`1de324b`](https://github.com/Nicconike/Steam-Stats/commit/1de324b9d28883ae0ce967c149c954a49b35cac6))

### Continuous Integration

- Add output for codeql analysis
  ([`6b8564a`](https://github.com/Nicconike/Steam-Stats/commit/6b8564a69c3d406ec08869e27772ced9efa16735))

- Bump docker/scout-action from 1.9.3 to 1.10.0 in the github-actions group

* ci: bump docker/scout-action in the github-actions group
Updates `docker/scout-action` from 1.9.3 to 1.10.0

* Updated Steam Stats

* ci: update steam stats workflow

### Chores

- Add dependencies in pyproject.toml
  ([`b1438f2`](https://github.com/Nicconike/Steam-Stats/commit/b1438f20623334031d5b1c712d9a5d2ed7ddafce))

- Add versions in requirements.txt
  ([`113ef74`](https://github.com/Nicconike/Steam-Stats/commit/113ef74b4bcdb25e16adfce8a1bbdc1274c3b75a))

- Template update
  ([`2370d9b`](https://github.com/Nicconike/Steam-Stats/commit/2370d9b31a226a2ac6b9ddd0f48151e8c6ef2a29))

- Update dependabot.yml
  ([`3c3fe46`](https://github.com/Nicconike/Steam-Stats/commit/3c3fe46f3d976b67f6b78568dced5b29c5994ffa))

- Update pyproject.toml
  ([`b11e120`](https://github.com/Nicconike/Steam-Stats/commit/b11e1203587e3e6f43e64eb1e14d66ee5a143a19))

- Update release workflow
  ([`21fcc97`](https://github.com/Nicconike/Steam-Stats/commit/21fcc97842f0fb7589ebe5cfac522523e00bdd15))

- Update workflow & dockerfile
  ([`771a869`](https://github.com/Nicconike/Steam-Stats/commit/771a86987075102d47d523427bf9ee7a5d32d193))

- Update workflows
  ([`1080d6b`](https://github.com/Nicconike/Steam-Stats/commit/1080d6b68a260564fd6805d2b160e61489f8bedd))

- Update workflows for requirements.txt
  ([`4e55410`](https://github.com/Nicconike/Steam-Stats/commit/4e55410fedc5820eb57191b61e7a5c6760d8f041))

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

### Refactoring

- Address bandit vulns issues
  ([`04db6ea`](https://github.com/Nicconike/Steam-Stats/commit/04db6ea8f7a0c5d228d168d9555d678bfef309b5))

- Update pyproject.toml and template
  ([`666332e`](https://github.com/Nicconike/Steam-Stats/commit/666332e2a002dfaaba3f9ee4d43cba07b595e2e0))


## v0.1.4 (2024-06-20)

### Bug Fixes

- Update main python script to remvoe setup
  ([`ebfd9e0`](https://github.com/Nicconike/Steam-Stats/commit/ebfd9e01ac097efba2f507f8948084888da51a91))

### Chores

- Update dependencies ([#3](https://github.com/Nicconike/Steam-Stats/pull/3),
  [`99d0f2e`](https://github.com/Nicconike/Steam-Stats/commit/99d0f2ed378f052dc66b882fcd5cb40ea5ffc91e))

### Continuous Integration

- Update workflow to upload reports correctly
  ([`721ec76`](https://github.com/Nicconike/Steam-Stats/commit/721ec76b8e0345816fc9fd2ee7ab445ee98cbb59))

- Update workflows
  ([`b648032`](https://github.com/Nicconike/Steam-Stats/commit/b648032537ea8b667054a3d65ee5e4a2149cc46c))

### Documentation

- Add issue templates
  ([`cffa8f9`](https://github.com/Nicconike/Steam-Stats/commit/cffa8f9e6b02afab0593c3aa86bf7c79e47d56e0))


## v0.1.3 (2024-06-19)

### Bug Fixes

- **workflow**: Test release
  ([`e8c3ddb`](https://github.com/Nicconike/Steam-Stats/commit/e8c3ddba57368f21e9c29207fcb2eb9029ef99db))

### Continuous Integration

- Run with python3
  ([`7c0829b`](https://github.com/Nicconike/Steam-Stats/commit/7c0829b0a2a78f8752e0704672b7f317999b2688))

- Update release workflow & add templates
  ([`8a7e376`](https://github.com/Nicconike/Steam-Stats/commit/8a7e3765ec89b18a03112e24445bfa18c1747cb6))


## v0.1.2 (2024-06-17)

### Bug Fixes

- Update action.yml to pull docker image
  ([`130bc91`](https://github.com/Nicconike/Steam-Stats/commit/130bc91bcc9fcc4d229f5d87fc2b05bc1472ce18))

### Build System

- Addressing the autobuild warning to use v3 for CodeQL
  ([`abc130a`](https://github.com/Nicconike/Steam-Stats/commit/abc130a2641fb29f5b3fb4ef231d059d788b7e35))

### Chores

- Codeql & Pylint Setup
  ([`8ddb1d6`](https://github.com/Nicconike/Steam-Stats/commit/8ddb1d6e75ff4f760192cfeab82ec314357101ee))


## v0.1.1 (2024-06-16)

### Continuous Integration

- Trigger workflow
  ([`68cbea7`](https://github.com/Nicconike/Steam-Stats/commit/68cbea77858ad335336571d81d2904c414478f6f))

- Trigger workflow
  ([`96348ee`](https://github.com/Nicconike/Steam-Stats/commit/96348ee1154e7c2257fbf8080794b0afb7baf4c8))

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

Added codespaces support

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

### Bug Fixes

- **workflow**: Correct & update github workflow for automated release
  ([`44cc88e`](https://github.com/Nicconike/Steam-Stats/commit/44cc88ef4e80c47c0d750f4576aba3d3cdedbc25))

### Continuous Integration

- **workflow**: Update Docker CICD workflow to use semantic-release
  ([`4eb4ac9`](https://github.com/Nicconike/Steam-Stats/commit/4eb4ac9566e07a83d90916042423c1164d77795d))
