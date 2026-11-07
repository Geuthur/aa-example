# AA Example.<a name="aa-example"></a>

> [!NOTE]
> This repository is a template. Create a new app with `make init-app` instead of renaming by hand, see [Create a New App from this Template](#create-a-new-app-from-this-template).

A Example App that templating example to example

______________________________________________________________________

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=1 -->

- [AA Example.](#aa-example)
  - [Create a New App from this Template](#create-a-new-app-from-this-template)
  - [Features](#features)
  - [Installation](#installation)
    - [Step 1 - Install the Package](#step-1---install-the-package)
    - [Step 2 - Configure Alliance Auth](#step-2---configure-alliance-auth)
    - [Step 3 - Add the Scheduled Tasks](#step-3---add-the-scheduled-tasks)
    - [Step 3.1 - (Optional) Add own Logger File](#step-31---optional-add-own-logger-file)
    - [Step 4 - Migrate & Preload EVE SDE Data](#step-4---migrate--preload-eve-sde-data)
    - [Step 4.1 - Migrate App and collect static](#step-41---migrate-app-and-collect-static)
    - [Step 5 - Setting up Permissions](#step-5---setting-up-permissions)
    - [Step 6 - (Optional) Setting up Compatibilies](#step-6---optional-setting-up-compatibilies)
  - [Frontend Development (React SPA)](#frontend-development-react-spa)
    - [Tech Stack](#tech-stack)
    - [Frontend Makefile Commands](#frontend-makefile-commands)
    - [Local Frontend Development](#local-frontend-development)
  - [Create a New Module](#create-a-new-module)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Checklist](#checklist)
  - [Translations](#translations)
  - [Contributing](#contributing)

<!-- mdformat-toc end -->

## Create a New App from this Template<a name="create-a-new-app-from-this-template"></a>

Create the repository from this template on GitHub, clone it and run the script once with the Python package name, the repository (PyPI) name and the verbose name of the new app:

```shell
make init-app NAME=ledger APPNAME=aa-ledger VERBOSE="AA Ledger"
```

The script `scripts/init_app.py` (Python standard library only) reads the current names from `.make/config.ini` and

- replaces `example` → `ledger`, `Example` → `Ledger`, `EXAMPLE` → `LEDGER`, `aa-example` → `aa-ledger`, `AA Example` → `AA Ledger` and `AA-Example` → `AA-Ledger` in every text file, at word boundaries (`examples` or `example.com` stay as they are; in `LICENSE` only the app names change),
- renames `example/`, `example/templates/example/`, `example/static/example/` and every other file or directory with the old names,
- sets `__version__` to `0.1.0` and resets `CHANGELOG.md` to an empty "In Development" section,
- reports every replacement and rename at the end.

Source maps of the built frontend, the ESI specification `openapi_<date>.json` and files ignored by git are skipped. Options go into `INIT_ARGS`:

| Option                     | Effect                                                                                                                                                                                                                                                            |
| :------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--dry-run`                | Only report what would change.                                                                                                                                                                                                                                    |
| `--drop-migrations`        | Remove the migrations of the template (`0001_initial.py` of the `character` module). Keep them if the module stays as your pattern, otherwise run `make migrations` afterwards.                                                                                   |
| `--drop-template-override` | Remove the `TEMPLATE ONLY` override of `permissions` in `tests/testdata/app.py`. Do this together with making the `General` model concrete (remove `abstract = True` and `managed = False` in `models/general.py`), the override only exists for abstract models. |

```shell
make init-app NAME=ledger APPNAME=aa-ledger VERBOSE="AA Ledger" INIT_ARGS="--drop-migrations --drop-template-override"
```

The script stays in `scripts/` after the run, so it can be repeated on a fresh copy. Afterwards replace `ledger/docs/images/preview-1.png` with a screenshot of the new app and run `make tox-tests`, `make react-test`, `make react-lint` and `make react-build`.

## Features<a name="features"></a>

- **Modern React SPA Frontend**:
  - React 19, TypeScript, and Vite build pipeline
  - AllianceAuth CSS styling, shared design tokens, and responsive layouts
  - Lucide icons (`lucide-react`) and status indicators (`LiveStatusIndicator`, `SecurityBadge`)
  - TanStack Query (`@tanstack/react-query`) for cached state management & TanStack Table (`@tanstack/react-table`) for sortable, searchable data tables
  - Full internationalization (`i18next` / `react-i18next`) with translations for 12 languages
  - Type-safe API communication using `openapi-fetch` and auto-generated TypeScript schemas
- **Django Ninja REST API**:
  - Modular API endpoints (`/example/api/`) with interactive OpenAPI documentation
  - Automated schema and TypeScript type generation via Makefile
- **Example Boilerplate**:
  - Clean Alliance Auth app architecture (models, managers, tasks, forms, and views)
  - Pre-configured unit tests for backend (`AuthTestCase`) and frontend (`Vitest` + Testing Library)

## Installation<a name="installation"></a>

> [!NOTE]
> AA Example needs at least Alliance Auth v5
> Please make sure to update your Alliance Auth before you install this APP

### Step 1 - Install the Package<a name="step-1---install-the-package"></a>

Make sure you're in your virtual environment (venv) of your Alliance Auth then install the pakage.

```shell
pip install aa-example
```

### Step 2 - Configure Alliance Auth<a name="step-2---configure-alliance-auth"></a>

Configure your Alliance Auth settings (`local.py`) as follows:

```python
INSTALLED_APPS = [
    # other apps
    "eve_sde",  # only if it not already existing
    "example",
    # other apps?
]

# This line is right below the `INSTALLED_APPS` list, if not already exist!
INSTALLED_APPS = ["modeltranslation"] + INSTALLED_APPS
```

### Step 3 - Add the Scheduled Tasks<a name="step-3---add-the-scheduled-tasks"></a>

To set up the Scheduled Tasks add following code to your `local.py`

```python
if "example" in INSTALLED_APPS:
    CELERYBEAT_SCHEDULE["AA Example :: Update Characters"] = {
        "task": "example.tasks.update_all_characters",
        "schedule": crontab(minute="*/30"),
    }
```

### Step 3.1 - (Optional) Add own Logger File<a name="step-31---optional-add-own-logger-file"></a>

To set up the Logger add following code to your `local.py`
Ensure that you have writing permission in logs folder.

```python
LOGGING["handlers"]["example_file"] = {
    "level": "INFO",
    "class": "logging.handlers.RotatingFileHandler",
    "filename": os.path.join(BASE_DIR, "log/example.log"),
    "formatter": "verbose",
    "maxBytes": 1024 * 1024 * 5,
    "backupCount": 5,
}
LOGGING["loggers"]["extensions.example"] = {
    "handlers": ["example_file"],
    "level": "DEBUG",
}
```

### Step 4 - Migrate & Preload EVE SDE Data<a name="step-4---migrate--preload-eve-sde-data"></a>

AA Example uses EVE SDE data to map IDs to names for EveTypes. You will need to preload some data from SDE once.

```shell
python manage.py migrate eve_sde
python manage.py esde_load_sde
```

### Step 4.1 - Migrate App and collect static<a name="step-41---migrate-app-and-collect-static"></a>

Migrate the app and collect static.

```shell
python manage.py migrate example
python manage.py collectstatic --noinput
```

### Step 5 - Setting up Permissions<a name="step-5---setting-up-permissions"></a>

With the Following IDs you can set up the permissions for the Example

| ID              | Description                   | Details                                                         |
| :-------------- | :---------------------------- | :-------------------------------------------------------------- |
| `basic_access`  | Can access the Example module | All members with this permission can access the Example module. |
| `manage_access` | Can Manage Example module     | Can manage application settings and data.                       |
| `full_access`   | Full access to Example module | Administrative access with full management permissions.         |

### Step 6 - (Optional) Setting up Compatibilies<a name="step-6---optional-setting-up-compatibilies"></a>

The Following Settings can be setting up in the `local.py`

- EXAMPLE_APP_NAME: `"YOURNAME"` - Set the name of the APP
- EXAMPLE_TASKS_TIME_LIMIT: `1200` - Defines the time (in seconds) a task will timeout
- EXAMPLE_STALE_TYPES: `{"wallet": 60}` - Minutes after which a section is fetched from ESI again

If you set up EXAMPLE_LOGGER_USE to `True` you need to add the following code below:

## Frontend Development (React SPA)<a name="frontend-development-react-spa"></a>

The user interface of AA Example is built as a modern React Single-Page Application (SPA) located in the `frontend/` directory.

### Tech Stack<a name="tech-stack"></a>

- **Framework**: React 19, TypeScript
- **Bundler & Tooling**: Vite 8 (`@vitejs/plugin-react-swc`), AllianceAuth styles from `frontend/src/index.css`
- **UI Components & Icons**: React-Bootstrap, Lucide Icons (`lucide-react`)
- **Data & Tables**: TanStack React Query (`@tanstack/react-query`), TanStack Table (`@tanstack/react-table`)
- **API Client**: `openapi-fetch` with types generated via `openapi-typescript`
- **Testing**: Vitest with `@testing-library/react` and `jsdom`
- **Localization**: `i18next` & `react-i18next` (12 languages)

### Frontend Makefile Commands<a name="frontend-makefile-commands"></a>

You can control the frontend build, test, and development workflows directly from the repository root:

| Command                        | Description                                                             |
| :----------------------------- | :---------------------------------------------------------------------- |
| `make react-dev`               | Starts the Vite development server with proxy to backend                |
| `make react-build`             | Runs TypeScript compilation (`tsc -b`) and Vite production build        |
| `make react-test`              | Runs Vitest unit tests                                                  |
| `make react-lint`              | Runs ESLint verification                                                |
| `make react-eslint`            | Runs ESLint with automated fixes (`--fix`)                              |
| `make react-test-build`        | Runs build, asset copy, translation sync, and `collectstatic`           |
| `make react-release`           | Runs full release build (build, i18n scan, asset copy, `collectstatic`) |
| `make react-copy-assets`       | Copies Vite production build artifacts to Django's static directory     |
| `make react-copy-translations` | Copies frontend i18n translations to Django's static directory          |
| `make react-translations`      | Scans source code and updates i18n translation files                    |
| `make react-openapi`           | Exports Django Ninja OpenAPI schema and regenerates TypeScript types    |
| `make react-clean`             | Cleans React build directory                                            |

### Local Frontend Development<a name="local-frontend-development"></a>

1. **Install dependencies**:

   ```shell
   cd frontend
   npm install
   ```

1. **Start Vite development server**:

   ```shell
   # Inside frontend/
   npm run dev

   # Or from repository root:
   make react-dev
   ```

1. **Run tests and linter**:

   ```shell
   make react-test
   make react-lint
   ```

## Create a New Module<a name="create-a-new-module"></a>

The `character` module is the pattern for every new module: an owner model with ESI
sections, its update status, a task, an API and a page. Copy its files, rename
`character` to the name of the module and adapt the fields, sections and columns.

### Backend<a name="backend"></a>

| File                                                                         | Purpose                                                                                                                                                                         |
| :--------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `example/models/<module>.py`                                                 | The owner model with `UpdateManagerMixin`, `get_esi_scopes()`, `get_token()` and one `update_<section>()` method per section; its `<Module>UpdateStatus(UpdateStatusBaseModel)` |
| `example/models/helpers/update_manager.py`                                   | Shared: add the `<Module>UpdateSection` choices (one value per ESI section) and the stale minutes in `app_settings.EXAMPLE_STALE_TYPES`                                         |
| `example/managers/<module>.py`                                               | `AccessQuerySet`/`AccessManager` subclasses (`visible_to`, `manage_to`), the ESI fetch (`update_<section>_esi` → `update_section_if_changed`) and the update status manager     |
| `example/api/schema.py`                                                      | The Ninja schemas of the module (response and request separately)                                                                                                               |
| `example/api/helpers/<module>.py`                                            | `get_<entity>(request, id, manage=False)` on top of `api/helpers/core.get_object_with_access`                                                                                   |
| `example/api/<module>.py`                                                    | `ApiEndpoints` with `tags`, `summary` and every status code in `response`; register it in `example/api/__init__.py`                                                             |
| `example/tasks.py`                                                           | `update_all_<module>s` (periodic) and `update_<module>` (per owner, inside `retry_task_on_esi_error`)                                                                           |
| `example/__init__.py`                                                        | Add the ESI operation ids to `__operations__`                                                                                                                                   |
| `example/tests/testdata/<module>.py`                                         | Factories of the module (`aa-evesde-factory` for Alliance Auth objects)                                                                                                         |
| `example/tests/test_models/`, `test_managers/`, `test_api/`, `test_tasks.py` | Tests; ESI calls with `pook` under the real ESI URL                                                                                                                             |

### Frontend<a name="frontend"></a>

| File                                  | Purpose                                                                                    |
| :------------------------------------ | :----------------------------------------------------------------------------------------- |
| `frontend/src/Api/calls/<module>.ts`  | The API calls of the module over `apiClient` and its query keys (`<module>QueryKeys`)      |
| `frontend/src/Api/schema.ts`          | Type aliases of the module schemas from the generated `OpenApi.ts`                         |
| `frontend/src/Components/<Module>/`   | The components of the module, e.g. a table on `BaseTable`                                  |
| `frontend/src/Pages/<Module>Page.tsx` | The page: `useQuery` for loading, `useMutation` for actions                                |
| `frontend/src/Routing.tsx`            | The route of the page; the menu link comes from `api/general.py`                           |
| `frontend/src/__tests__/...`          | Tests next to the source: calls with `vi.spyOn(apiClient, ...)`, pages with `vi.mock(...)` |

### Checklist<a name="checklist"></a>

1. Backend: models, managers, schema, helpers, endpoints, task and tests; `make migrations`, `make tox-tests`.
1. `make react-openapi` regenerates `openapi.json` and `OpenApi.ts`; commit both.
1. Frontend: calls, components, page, route and tests; `make react-translations`, `make react-test`, `make react-lint`, `make react-build`.
1. `make pre-commit-checks` and an entry in `CHANGELOG.md`.

## Translations<a name="translations"></a>

[![Translations](https://weblate.geuthur.de/widget/allianceauth/aa-example/multi-auto.svg)](https://weblate.geuthur.de/engage/allianceauth/)

Help us translate this app into your language or improve existing translations. Join our team!"

## Contributing<a name="contributing"></a>

You want to improve the project?
Please ensure you read the [Contribution Guidelines]

<!-- MD Links -->

[contribution guidelines]: https://github.com/Geuthur/aa-example/blob/master/CONTRIBUTING.md "Contribution Guidelines"
