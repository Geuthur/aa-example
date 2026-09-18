# Changelog

## [In Development] - Unreleased

<!--
> [!NOTE]
>

> [!TIP]
>

> [!IMPORTANT]
>

> [!WARNING]
>

> [!CAUTION]
>

Section Order:

### Added
### Fixed
### Changed
### Removed
-->

<!-- Your changes go here -->

### Added

- React SPA frontend (`frontend/`):
  - Vite + React 19 + TypeScript build pipeline with Vitest unit tests
  - Bundle optimization and vendor chunk splitting (`@vendor`, `@react-libs`, `@bootstrap-libs`, `@lang-libs`)
  - Internationalization (`i18next`) with scanner configuration and translations for 12 languages
  - Type-safe OpenAPI client integration (`openapi-fetch`, `openapi-typescript`)
  - Custom ESLint rule for bootstrap heading imports
  - Reusable components: `BaseTable` (with filter, pagination, and column configuration), `BaseModal`, `FetchingLoader`, `ErrorLoader`, `ErrorBoundary`, `BaseHeader`, `BaseMenu`, and `AuthMenu`
  - Forms and pages: `UserSettingsForm`, `Base`, `MainPage`, and `Settings`
- Ninja API endpoints:
  - User settings endpoint (`/api/general/user-setting`)
  - Character list endpoint with filtering (`/api/general/characters`)
  - Extended API schema definitions
- Backend:
  - `GeneralSetting` model for user settings
  - `GeneralManager` custom manager
  - EVE Online character helper in `example/helpers/eveonline.py`
  - `example/forms.py` (`GeneralForm`)
  - `example/templates/example/react_base.html` template for mounting the React application
- Makefile automation:
  - Added React targets in `.make/conf.d/react.mk` (`react-dev`, `react-build`, `react-lint`, `react-test`, `react-i18n-scan`)
- GitHub Actions:
  - Added `frontend` job for React linting, unit testing, and build check in `.github/workflows/autotester.yml`
- Tox environment:
  - Added `[testenv:react]` to execute frontend unit tests
- Agent development rules under `.agents/rules/` (API, Git commits & changelog, planning, React, and testing guidelines)

### Fixed

- Weblate URL in `CONTRIBUTING.md`

### Changed

- Updated `tox.ini` to include development environment for `allianceauth` and frontend test runner
- Updated `.github/workflows/autotester.yml` to require frontend checks before `test-coverage`
- Updated `.pre-commit-config.yaml` dependencies and added excludes for `frontend/` and React build artifacts
- Updated root `eslint.config.js` to ignore frontend source and compiled React assets
- Updated `.stylelintrc.json` to ignore compiled React CSS and allow the `:global` pseudo-class
- Reorganized navigation templates (moved from `partials/navigation/` to `navigation/`)
- Updated `example/views.py` and `example/urls.py` to route and serve the React base app and settings view

### Removed

- Deprecated navigation partial template `example/templates/example/partials/navigation/navigation.html`

## [1.0.0] - 2026-09-10

### Added

- `pook` dependency for URL Tests like ESI Calls
- CODEOWNERS
- Ninja API
  - API Schema Example
  - API Example
- Makefile System
- Applogger
- Unified template settings
- CSS, JS Bundle Example
- Universal Updater
- JS Helper

### Changed

- Optimized tests enviroment
- Updated `pyproject.toml`
- Optimized `.gitignore`
- Updated pre-commit dependencies
- Dependency `allianceuth` set to `>=5`
- Dependency `django-ninja` set to `>=1.5,<2`

### Removed

- `django-eveuniverse` dependency
- `allianceauth-app-utils` dependency
- `when_esi_is_available` decorator
- Admin View
- Unnecessary Stuff in `app_settings`

## [0.0.4] - 2025-09-03

### Added

- Admin Example View

### Changed

- Update Pre-Commit
- GitHub Workflow
- Prepared ESI Provider to new Guideline
- Updated pyproject
- Updated tox
- Updated npm
- Optimized AA Test Enviroment

### Fixed

- Template Path (`template` to `example`)

### Removed

- Cache Buster [Commit](https://github.com/Geuthur/aa-template/blob/4518910bc1a77b5323d5f5c91cad60f60b44b432/template/helpers/static_files.py)

## [0.0.3] - 2025-07-04

### Changed

- Refactor aa-example

## [0.0.2] - 2025-02-06

### Change

- Update AA to 4.6.1
- Update Pre Commit

### Added

- Translation
- Python 3.13 Support
- Cache Buster by [@ppfeufer](https://github.com/ppfeufer)

## [0.0.1] - 2024-08-xx

### Added

- Initial public release

<!-- Links -->

[0.0.2]: https://github.com/Geuthur/aa-example/compare/v0.0.1...v0.0.2 "0.0.2"
[0.0.3]: https://github.com/Geuthur/aa-example/compare/v0.0.2...v0.0.3 "0.0.3"
[0.0.4]: https://github.com/Geuthur/aa-example/compare/v0.0.3...v0.0.4 "0.0.4"
[1.0.0]: https://github.com/Geuthur/aa-example/compare/v0.0.4...v1.0.0 "v1.0.0"
[in development]: https://github.com/Geuthur/aa-example/compare/v1.0.0...HEAD "In Development"
