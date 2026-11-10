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

### Added

- `scripts/init_app.py` and `make init-app NAME=<package> APPNAME=aa-<name> VERBOSE="AA <Name>"` create a new app from the template: rename `example`, `Example`, `EXAMPLE`, `aa-example`, `AA Example` and `AA-Example` in every text file and path at word boundaries, set `__version__` to `0.1.0`, reset `CHANGELOG.md`, optionally drop the template migrations (`--drop-migrations`) and the `TEMPLATE ONLY` override (`--drop-template-override`); unit tests in `tests/test_init_app.py`
- README section "Create a New App from this Template" replaces the warning about `0001_initial.py`
- Python scaffold from the apps: `retry_task_on_esi_error`, `DOWNTIME_TIMER` and `DownTimeError` (`providers.py`, `errors.py`), `models/helpers/update_manager.py` with `UpdateSectionResult`, `_NeedsUpdate`, `UpdateStatus`, `UpdateSection`, `UpdateStatusBaseModel`, `UpdateManager` and `UpdateManagerMixin` (aa-ledger as base, `UpdateSection` base class and `get_status` as opt-ins), `api/helpers/core.py` with `get_object_with_access` and `can_view_overview`
- Character module as pattern for new modules: `CharacterOwner` with the ESI section `wallet` and `CharacterUpdateStatus` (`models/character.py`, migration `0001_initial`), `managers/character.py`, `api/character.py` (`GET characters/`, `GET characters/{character_id}/`, `POST characters/{character_id}/update/`), `api/helpers/character.py`, tasks `update_all_characters` and `update_character`, setting `EXAMPLE_STALE_TYPES`
- Frontend of the character module: `Api/calls/character.ts` with `characterQueryKeys`, `Pages/CharacterPage.tsx`, `Components/Character/` (`CharacterTable`, `CharacterStatusBadge`), route `characters/` and menu link
- README section "Create a New Module" with the file list of both sides
- Tests for all of the above, the ESI fetch with `pook` under the real ESI URL
- `BaseTable`: `showFooter` renders the column `footer` definitions as a summary row (from aa-ledger); `className` props per area (`headerClassName`, `bodyClassName`, `rowClassName`, `footClassName`, `footerClassName`) and slots (`toolbar`, `footer`, `emptyState`) so apps override instead of copying
- `ErrorLoader`, `FetchingLoader` and `ErrorBoundary` take `className` props (`iconClassName`, `spinnerClassName`, `traceClassName`)
- Tests for the loaders (`__tests__/Components/Base/Loader/Loader.test.tsx`)
- `useCooldown`, `useOwnerCooldowns`, `useFeedback` and `useUserData` hooks in `frontend/src/Hooks/` (shared with the other apps)
- `useMenu` hook in `frontend/src/Menu/Hooks/`, `AuthLeftMenuAsync` and `AuthRightMenuAsync` load the menu through it
- `AdministrationMenuItem` in `frontend/src/Menu/BaseMenu.tsx`: an `administration` link is shown in red with a shield icon
- [ADD] `badge` and `has_errors` on the `MenuLink` schema and an issue count badge in `BaseMenu` (`bg-danger`, pulsing via `aa-menu-badge-pulse` while `has_errors` is set), as template for the `Settings` navigation item of all plugins.
- `BaseTable`: optional server-side pagination (`serverPagination`) with total count and an optional loading state (`isLoading`, `loadingText`). Existing tables are unchanged.
- Optional extra `tests-allianceauth-development` (test packages plus the Alliance Auth 6 pre-release) for the tox environment `allianceauth-development` and `make tox-tests-development`; a non-blocking CI job "AA Development" runs it on Python 3.13 and 3.14

### Fixed

- [FIX] ESI outages and limits inside a section did not retry `update_character`: the `UpdateManager` turned every ESI error except `TokenError` into an update status, so `retry_task_on_esi_error` only saw the downtime check on entry. `_handle_update_exception` now raises the errors the task retries on (`ESIErrorLimitException`, `ESIBucketLimitException`, `HTTPServerError` 502/503/504, `RequestError`, `DownTimeError`), checked by the new `is_retryable_esi_error()` in `providers.py`. `execute_section` records them as a failed run of the section before raising, so the section shows the error and stays stale until the retry succeeds. Other errors (e.g. HTTP 500 or 404) still end in the update status only.

- [FIX] On phones narrower than 640 px the pages were wider than the screen because of the minimum width of the `aa-react container` of `aa-geuthur-react`. `Routing.tsx` sets `fluidOnSmallScreens` on `AuthBase` (`aa-geuthur-react` 1.2.0), so the container shrinks with the screen. New apps made from the template have it from the start.

- The CSS of `aa-geuthur-react` is imported with `@import` at the top of `Styles/index.css` instead of in `Main.tsx`. Vite put the package CSS from `Main.tsx` into the vendor chunk, which `react_base.html` does not load, so tables had no background, filters were white and containers had no minimum width. `aa-geuthur-react` is raised to `^1.0.2` (fixes the active menu links)

- Template leftovers: `// Voices of War` import heading in `Pages/404.tsx`, tooltip id `vowra` in `Utils/bootsTrap.tsx` (now `aa-example-tooltip`), scrollbar comment in `Styles/index.css`, "AA Skillfarm" in README step 4, and `__package_name__` is `aa-example` in lower case like in every other app

- Fixed the `import-headings` ESLint rule duplicating comments above the first import on every `--fix` pass, which could grow a file exponentially; added a unit test (`eslint-rules/import-headings.test.mjs`).

- Fixed `make coverage` exiting with 0 when tests failed. The reports are still created, and the target now exits with the status of the test run, or with the status of `coverage report` if the tests passed.

- [FIX] The pulsing menu and tab badges scaled up and down with their number. Only the glow around the badge pulses now.

- [FIX] `__operations__` was an empty list, which makes `esi.client` raise an `AttributeError` with `DEBUG=False`. It now contains the public operation `GetStatus`; added a regression test (`example/tests/test_providers.py`).

### Changed

- [CHANGE] The `AppLogger` is created only once in `example/providers.py`. `api/character.py`, `managers/character.py`, `managers/general.py`, `models/helpers/update_manager.py` and `tasks.py` import it with `from example.providers import logger` instead of building their own. Log records now carry the logger name `example.providers` instead of the module name; the `[Example]` prefix is unchanged.
- [CHANGE] Language files other than `en` hold only real translations as Weblate writes them, missing keys fall back to English. `i18next-scanner` maintains only `en`; the empty placeholders were removed from the other languages.
- [CHANGE] `aa-geuthur-react` raised to `^1.3.0`. The package bundles its own translations and registers them with i18next through `AaReactProvider`, so `Main.tsx` lists only the namespace `translation`, the copies under `example/static/example/i18n/<lng>/aa-geuthur-react.json` are removed and `make react-copy-translations` no longer copies them. Untranslated strings in `frontend/i18n/<lng>/translation.json` are empty instead of English (`i18next-scanner` writes the key as value only for `en`); `returnEmptyString: false` shows the English fallback at runtime. Translate on Weblate as before.
- `managers.py` moved to `managers/general.py`; `AccessQuerySet` resolves ownership through `character__character_ownership__user` and exposes `visible_q`/`manage_q` for subclasses
- `Api/ApiCalls.ts` moved to `Api/calls/general.ts`; API calls and query keys of a module live in `Api/calls/<module>.ts`
- The API error responses use `ErrorSchema` instead of `dict`; the menu links to the character page
- `__operations__` contains `GetCharactersCharacterIdWallet`; `UserMainFactory` uses the ESI scopes of `CharacterOwner`
- BaseTable stack, filters and loaders use Bootstrap utilities instead of CSS modules, like aa-ledger. The filter theme (input, clear button, dropdown, popover) moved to `Styles/table.css` as `aa-table-filter-*` classes, the shake animation to `Styles/index.css`; the loading state dims the rows with `opacity-50 pe-none` (`aria-busy`)
- [CHANGE] Tests use the Alliance Auth factories (`UserFactory`, `EveAllianceInfoFactory`, `EveCorporationInfoFactory`, `EveCharacterFactory`) and test helpers (`add_character_to_user` etc.) from `aa-evesde-factory` (new test dependency) instead of own copies; `testdata/factory.py` and `testdata/utils.py` are removed. Its usernames are unique, so a random name can no longer match an existing user such as the superuser of a test class. `UserMainFactory` stays as the app's own subclass.
- Aligned the template with `aa-ledger`: entry files are now `Main.tsx`, `Routing.tsx` and `constants.ts` (replacing `main.tsx`, `App.tsx` and `configuration.ts`), global styles live in `Styles/index.css` and `Styles/table.css`.
- Replaced `BaseTable`, `BaseModal`, the loaders and the `Utils` helpers with the shared `aa-ledger` implementation. `BaseTable` `variant` is now `default` or `light`, and row selection and `onRowClick` are supported.
- Formatting helpers are consolidated in `Utils/format.ts` (`formatNumber`, `formatCompactNumber`, `formatIsk`, `formatDate`, `formatRelativeTime`, `formatEta`) with an `en` locale fallback; `renderTooltip` lives in `Utils/bootsTrap.tsx`.
- The Style Guide, settings and main page use Bootstrap components instead of the custom `aa-panel`, `aa-btn`, `aa-badge` and `aa-section` classes.
- `General` defines a `Permission` enum with `get_perm`, `has_perm`, `has_any_perm` and `has_management_access`; views, menu hook and API use it instead of hard-coded permission strings.
- Aligned `.pre-commit-config.yaml`, `.gitignore`, `tox.ini`, `CONTRIBUTING.md` and the issue template configuration with `aa-ledger`.
- Replaced `pook` with `pookx` in the test dependencies.

### Removed

- `api/character.py` stub with dummy data and `ExampleSchema`; `example_task` (replaced by `update_all_characters`)
- CSS modules `BaseTable`, `BaseTableFilter`, `BaseTableForm`, `BaseTablePages`, `ErrorBoundary`, `ErrorLoader`, `FetchingLoader` under `Styles/modules/`
- Removed the legacy server-rendered templates (`base.html`, `bundles/`, `navigation/`, `view-index.html`) and the unused `character_id` route of the React view.
- Removed the unused `Badges`, `Forms` and `Tables` frontend components, the `tableHelper.module.css` style, the Bootstrap table variant and the `react` tox environment.
- Removed the custom CSS panel, button, badge, section, and tab utility classes in favor of Bootstrap 5.3.
- Removed the agent rules under `.agents/rules/`. The agent rules for this project now live in the Brain repository.
- [REMOVE] The unused `ExampleTestCase` alias of `AuthTestCase` in `example/tests/__init__.py`.
- Removed the HTML helpers `bootstrap_icon()`, `bootstrap_text_style_class()` and `description()` from `UpdateStatus`. The frontend renders the update status from the API itself.

### Changed

- The shared React base comes from the npm package [`aa-geuthur-react`](https://github.com/Geuthur/aa-geuthur-react) (BaseTable stack, BaseModal, loaders, `BaseSectionHeader`, menu, `useMenu`, `useUserData`, `useCooldown`, `useFeedback`, `AuthBase`, `ErrorPage`, utils, `createApiClient`, `queryKeys`, styles, ESLint rule `import-headings`). `Routing.tsx` wraps the app in `AaReactProvider`, `Main.tsx` loads the namespace `aa-geuthur-react` next to `translation` and imports `aa-geuthur-react/styles.css`, `apiClient` is `createApiClient<paths>()`
- `make react-copy-translations` also copies `i18n/<lng>/aa-geuthur-react.json` of the package into `static/example/i18n/<lng>/`

### Removed

- The copies of the shared modules and their tests: `Components/Base/`, `Menu/`, `Hooks/`, `Utils/`, `Pages/Base.tsx`, `Pages/404.tsx`, `Api/query.ts`, `Styles/table.css`, the CSS modules `bootsTrap` and `BaseModal`, `eslint-rules/` and the rules of `Styles/index.css` the package ships (`aa-react.container`, `aa-shake`, `aa-menu-badge-pulse`, `aa-nav-danger`); `loadMenu` and `loadUserData` of `Api/calls/general.ts` (now in the package); the dev dependency `openapi-typescript-helpers`

<!-- Your changes go here -->

## [1.0.1] - 2026-10-18

### Added

- Dynamic frontend configuration via `configuration.ts` (`AppName`, `ProjectName`) driving root container mounting, Vite dev proxy, API routes, and table tooltips.
- Alliance Auth Flatly and Darkly theme compatibility with semantic CSS tokens and theme overrides (`html[data-theme="flatly"]`, `html[data-theme="darkly"]`).
- Alternative table styling `aa-table-light` and `aa-table-shell-light` (`variant="vowra-light"`) optimized for modals and containers with `aa-panel` backgrounds.
- Showcase section and interactive modal preview for `aa-table-light` in the Style Guide.
- Frontend style guide route with AllianceAuth utility previews and table variants.
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
- Managed per-user settings with typed JSON GET/PUT endpoints.
- Static React inline styles moved into local CSS Modules.
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
- Frontend dependencies:
  - Installed `lucide-react` for UI icons
- Frontend Badges & Indicators (`frontend/src/Components/Badges/`):
  - `LiveStatusIndicator` component with status dot animation, timestamp tooltips, and unit tests
  - `SecurityBadge` component for formatting and styling EVE Online system security levels
- Frontend Utilities (`frontend/src/Utils/`):
  - `eveOnline.ts`: Helper functions for EVE Online entity image URLs (character portraits, corporation/alliance logos) and security status formatting
  - `bootsTrap.tsx`: Bootstrap badge and variant helper utilities
  - `iconHelper.tsx`: Dynamic icon helper with Lucide icons
- Frontend Navigation:
  - `AuthLeftMenu` and `AuthRightMenu` (with async variants `AuthLeftMenuAsync` and `AuthRightMenuAsync`) supporting split navigation and external links
- Frontend Pages:
  - `404` (NotFound) page component
- Frontend unit test coverage:
  - Unit tests for EVE Online utilities, Bootstrap helpers, and icon helper (`src/Utils/`)
  - Unit tests for badges and indicators (`SecurityBadge`, `LiveStatusIndicator`, `liveStatusHelper`)
  - Unit tests for `AuthLeftMenu`, `AuthRightMenu`, and `404` ErrorPage
  - Extended tests for `tableHelper` (CSV export and tooltip rendering)

### Fixed

- Circular import between `ApiCalls.ts` and `Api.ts` by importing `ProjectName` directly from `@/configuration`.
- `UserMainFactory` import path in `example/tests/__init__.py`.
- Missing permission handling during test data generation in `example/tests/testdata/factory.py`.
- Weblate URL in `CONTRIBUTING.md`

### Changed

- Replaced all `<main>` and `<section>` container tags across `aa-example` components and pages (`BaseHeader.tsx`, `MainPage.tsx`, `SettingsPage.tsx`, `StyleGuide.tsx`, `404.tsx`) with `react-bootstrap` `Card` (`Card.Body`, `Card.Header`).
- Dynamic React root container ID in `react_base.html` (`aa-{{ app_name }}-root`).
- Updated `SettingsPage.module.css` with semantic color tokens (`var(--aa-text-title)`).
- Updated backend view tests in `test_access.py` to inherit from `AuthTestCase` with tripartite test structure.
- Removed Tailwind utility classes from the React frontend in favor of AllianceAuth CSS classes and design tokens.
- Ninja API:
  - Menu API (`/example/api/menu/`):
    - Changed endpoint path from `/example/api/view/menu/` to `/example/api/menu/`
    - Separated navigation structure into `left_links` and `right_links`
    - Added `is_external` flag to `MenuLink` schema
  - User API (`/example/api/user/`):
    - Changed endpoint path from `/example/api/view/user/` to `/example/api/user/`
    - Added `is_admin` permission check to `UserData` schema
    - Added corporation (`corporation_id`, `corporation_name`) and optional alliance (`alliance_id`, `alliance_name`) fields to `UserData`
- Frontend Components & Styling:
  - `BaseTable`: Enhanced styling, compact mode, responsive layout, and improved table helper utilities (`tableHelper.tsx`)
  - `BaseMenu` and `Base.tsx`: Integrated left and right navigation menus, external links, and admin permission handling
  - Replaced `App.css` with `index.css` containing AllianceAuth design tokens, sci-fi theme variables, and custom scrollbars
  - Updated `vite.config.ts` with the `@` path alias
- Standard View is React based
- Updated `tox.ini` to include development environment for `allianceauth` and frontend test runner
- Updated `.github/workflows/autotester.yml` to require frontend checks before `test-coverage`
- Updated `.pre-commit-config.yaml` dependencies and added excludes for `frontend/` and React build artifacts
- Updated root `eslint.config.js` to ignore frontend source and compiled React assets
- Updated `.stylelintrc.json` to ignore compiled React CSS and allow the `:global` pseudo-class
- Reorganized navigation templates (moved from `partials/navigation/` to `navigation/`)
- Updated `example/views.py` and `example/urls.py` to route and serve the React base app and settings view
- Updated `README.md` with React SPA frontend documentation, Makefile targets, and missing `General` model permissions (`full_access`)
- Switched settings route in `App.tsx` to use `SettingsPage.tsx` with dedicated CSS Module styling and optimistic TanStack Query mutation
- Added `setupTests.ts` with Vitest DOM cleanup and jest-dom matchers

### Removed

- Removed legacy `Settings.tsx` page component in favor of `SettingsPage.tsx`
- Obsolete Django `UserSettingsForm`; settings are now validated by the typed JSON API.
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
[1.0.1]: https://github.com/Geuthur/aa-example/compare/v1.0.0...v1.0.1 "v1.0.1"
[in development]: https://github.com/Geuthur/aa-example/compare/v1.0.1...HEAD "In Development"
