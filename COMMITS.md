## Conventional Commits
This repo follows [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
Major.Minor.Patch

Please refer below commit tags and checkout conventional commits if you are new before contributing

### Commit Types and Their Usage

1. **feat**:
	1. Description: A commit that introduces a new feature to the codebase.
	2. Example: feat(auth): add OAuth2 login support
   	3. Semantic Versioning: MINOR

2. **fix**:
	1. Description: A commit that patches a bug in the codebase.
	2. Example: fix(api): correct user authentication issue
	3. Semantic Versioning: PATCH

3. **docs**:
	1. Description: A commit that adds or updates documentation.
	2. Example: docs(readme): update installation instructions
	3. Semantic Versioning: No version bump

4. **style**:
	1. Description: A commit that does not affect the meaning of the code (e.g., formatting, missing semi-colons).
	2. Example: style: format code with Prettier
	3. Semantic Versioning: No version bump

5. **refactor**:
	1. Description: A commit that neither fixes a bug nor adds a feature but improves the code structure.
	2. Example: refactor: simplify authentication logic
	3. Semantic Versioning: No version bump

6. **perf**:
	1. Description: A commit that improves performance.
	2. Example: perf: optimize database queries
	3. Semantic Versioning: PATCH

7. **test**:
	1. Description: A commit that adds or updates tests.
	2. Example: test: add unit tests for user service
	3. Semantic Versioning: No version bump

8. **build**:
	1. Description: A commit that affects the build system or external dependencies.
	2. Example: build: update webpack to version 5
	3. Semantic Versioning: No version bump

9.  **ci**:
	1. Description: A commit that changes CI configuration files and scripts.
	2. Example: ci: add GitHub Actions workflow
	3. Semantic Versioning: No version bump

10.  **chore**:
	1. Description: A commit that does not modify src or test files. It is used for routine tasks.
	2. Example: chore: update .gitignore file
	3. Semantic Versioning: No version bump

11.  **revert**:
	1. Description: A commit that reverts a previous commit.
	2. Example: revert: revert commit 12345
	3. Semantic Versioning: No version bump

### Major Version Bumps

A major version bump is triggered by a breaking change. According to the Conventional Commits specification, a breaking change can be indicated in two ways:

1. Using BREAKING CHANGE in the Footer:
	1. A commit that has a footer with BREAKING CHANGE: followed by a description of the breaking change.
	2. This can be part of any commit type (feat, fix, chore, etc.).

2. Using ! After the Commit Type and Scope:
	1. A commit that appends a ! after the type and scope in the commit message.
	2. This indicates that the commit introduces a breaking API change.

### Examples of Major Version Bumps

1. Using BREAKING CHANGE in the Footer:
```sh
git commit -m "feat: allow provided config object to extend other configs

BREAKING CHANGE: `settings` and `overrides` keys in config are no longer supported"
```
Explanation: This commit introduces a new feature (feat) and includes a breaking change in the footer. This will trigger a major version bump.

2. Using ! After the Commit Type and Scope:
```sh
git commit -m "fix!: remove deprecated config properties"
```
Explanation: This commit fixes a bug (fix) and indicates a breaking change with !. This will trigger a major version bump.

3. Another Example with !:
```sh
git commit -m "feat(api)!: redirect users to the new workflow page"
```
Explanation: This commit introduces a new feature (feat) in the api scope and indicates a breaking change with !. This will trigger a major version bump.

### Detailed Examples for Minor & Patch Bumps

1. feat:
```sh
git commit -m "feat(auth): add OAuth2 login support"
```
Explanation: This commit adds a new feature to the authentication module, specifically OAuth2 login support.

2. fix:
```sh
git commit -m "fix(api): correct user authentication issue"
```
Explanation: This commit fixes a bug in the API related to user authentication.

3. docs:
```sh
git commit -m "docs(readme): update installation instructions"
```
Explanation: This commit updates the installation instructions in the README file.

4. style:
```sh
git commit -m "style: format code with Prettier"
```
Explanation: This commit formats the code using Prettier, without changing any functionality.

5. refactor:
```sh
git commit -m "refactor: simplify authentication logic"
```
Explanation: This commit refactors the authentication logic to make it simpler, without adding new features or fixing bugs.

6. perf:
```sh
git commit -m "perf: optimize database queries"
```
Explanation: This commit optimizes the database queries to improve performance.

7. test:
```sh
git commit -m "test: add unit tests for user service"
```
Explanation: This commit adds unit tests for the user service.

8. build:
```sh
git commit -m "build: update webpack to version 5"
```
Explanation: This commit updates the build tool webpack to version 5.

9. ci:
```sh
git commit -m "ci: add GitHub Actions workflow"
```
Explanation: This commit adds a new GitHub Actions workflow for continuous integration.

10. chore:
```sh
git commit -m "chore: update .gitignore file"
```
Explanation: This commit updates the .gitignore file, which is a routine task that does not affect the source code or tests.

11. revert:
```sh
git commit -m "revert: revert commit 12345"
```
Explanation: This commit reverts a previous commit identified by the hash 12345.
