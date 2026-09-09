# Example module for AllianceAuth.<a name="aa-example"></a>

> [!WARNING]
> Before you create Models, etc remove the 0001_initial.py from migrations folder if you dont have created own one.

A Example App that templating example to example

______________________________________________________________________

- [AA Example](#aa-example)
  - [Features](#features)
  - [Upcoming](#upcoming)
  - [Installation](#features)
    - [Step 1 - Install the Package](#step1)
    - [Step 2 - Configure Alliance Auth](#step2)
    - [Step 3 - Add the Scheduled Tasks and Settings](#step3)
    - [Step 4 - Migrate & Preload EVE SDE Data](#step4)
      - [Step 4.1 - Migrate App and collect static](#step41)
    - [Step 5 - Setting up Permissions](#step5)
    - [Step 6 - (Optional) Setting up Compatibilies](#step6)
  - [Translations](#translations)
  - [Contributing](#contributing)

## Features<a name="features"></a>

- Example
  - Copy & Paste

## Upcoming<a name="upcoming"></a>

- Crazy Shit incoming.

## Installation<a name="installation"></a>

> [!NOTE]
> AA Example needs at least Alliance Auth v5
> Please make sure to update your Alliance Auth before you install this APP

### Step 1 - Install the Package<a name="step1"></a>

Make sure you're in your virtual environment (venv) of your Alliance Auth then install the pakage.

```shell
pip install aa-example
```

### Step 2 - Configure Alliance Auth<a name="step2"></a>

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

### Step 3 - Add the Scheduled Tasks<a name="step3"></a>

To set up the Scheduled Tasks add following code to your `local.py`

```python
if "example" in INSTALLED_APPS:
    CELERYBEAT_SCHEDULE["AA Example :: Test Task"] = {
        "task": "example.tasks.example_task",
        "schedule": crontab(minute=0, hour="*/1"),
    }
```

### Step 3.1 - (Optional) Add own Logger File

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

### Step 4 - Migrate & Preload EVE SDE Data<a name="step4"></a>

AA Skillfarm uses EVE SDE data to map IDs to names for EveTypes. You will need to preload some data from SDE once.

```shell
python manage.py migrate eve_sde
python manage.py esde_load_sde
```

### Step 4.1 - Migrate App and collect static<a name="step41">

Migrate the app and collect static.

```shell
python manage.py migrate example
python manage.py collectstatic --noinput
```

### Step 5 - Setting up Permissions<a name="step5"></a>

With the Following IDs you can set up the permissions for the Example

| ID              | Description                   |                                                         |
| :-------------- | :---------------------------- | :------------------------------------------------------ |
| `basic_access`  | Can access the Example module | All Members with the Permission can access the Example. |
| `manage_access` | Can Manage Example module     | Can manage Application                                  |

### Step 6 - (Optional) Setting up Compatibilies<a name="step6"></a>

The Following Settings can be setting up in the `local.py`

- EXAMPLE_APP_NAME: `"YOURNAME"` - Set the name of the APP
- EXAMPLE_TASKS_TIME_LIMIT: `7200` - Defines the time (in seconds) a task will timeout

If you set up EXAMPLE_LOGGER_USE to `True` you need to add the following code below:

## Translations<a name="translations"></a>

[![Translations](https://weblate.geuthur.de/widget/allianceauth/aa-example/multi-auto.svg)](https://weblate.geuthur.de/engage/allianceauth/)

Help us translate this app into your language or improve existing translations. Join our team!"

## Contributing <a name="contributing"></a>

You want to improve the project?
Please ensure you read the [Contribution Guidelines]

<!-- MD Links -->

[contribution guidelines]: https://github.com/Geuthur/aa-example/blob/master/CONTRIBUTING.md "Contribution Guidelines"
