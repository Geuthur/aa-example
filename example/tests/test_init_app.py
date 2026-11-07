"""Tests for scripts/init_app.py, the script that creates a new app from the template."""

# Standard Library
import importlib.util
import tempfile
from pathlib import Path
from unittest import TestCase

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "init_app.py"
_spec = importlib.util.spec_from_file_location("init_app", SCRIPT)
init_app = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(init_app)

# The template under test uses its own names so the test does not depend on
# the names of this repository.
SRC = init_app.Names("demo", "aa-demo", "AA Demo")
DST = init_app.Names("fleet", "aa-fleet", "AA Fleet")

APP_PY = '''# Third Party
import factory

# AA EVE SDE Factory
from evesde_factory.allianceauth import EveCharacterFactory, UserFactory
from evesde_factory.utils import add_character_to_user

# Django
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Alliance Auth
from allianceauth.tests.auth_utils import AuthUtils

# AA Demo
from demo import __app_name__
from demo.models.character import CharacterOwner


class UserMainFactory(UserFactory):
    """Generate a User object."""

    permissions__ = [f"{__app_name__}.basic_access"]
    scopes__ = CharacterOwner.get_esi_scopes()

    # TEMPLATE ONLY: Do not copy this override into a real app.
    # The template models are abstract.
    # pylint: disable=no-self-argument
    @factory.post_generation
    def permissions(obj, create, extracted, **kwargs):
        """Set permissions."""
        if not create:
            return
        for permission_name in extracted or []:
            app_label, codename = permission_name.split(".")
            content_type, _ = ContentType.objects.get_or_create(
                app_label=app_label, model="general"
            )
            Permission.objects.get_or_create(
                content_type=content_type,
                codename=codename,
                defaults={"name": codename},
            )
            AuthUtils.add_permission_to_user_by_name(permission_name, obj)

    # pylint: disable=no-self-argument
    @factory.post_generation
    def main_character(obj, create, _, **kwargs):
        if not create:
            return
        add_character_to_user(user=obj, character=EveCharacterFactory())
'''

CHANGELOG = """# Changelog

## [In Development] - Unreleased

<!--
Section Order:

### Added
-->

### Added

- Something new

## [1.0.1] - 2026-10-18

### Fixed

- A bug

<!-- Links -->

[1.0.1]: https://github.com/Geuthur/aa-demo/compare/v1.0.0...v1.0.1 "v1.0.1"
[in development]: https://github.com/Geuthur/aa-demo/compare/v1.0.1...HEAD "In Development"
"""

FILES = {
    ".make/config.ini": (
        "# Configuration file for the AA Demo project\n\n[General]\n"
        "appname = aa-demo\nappname_verbose = AA Demo\npackage = demo\n\n"
        "[Git]\ngit_repository = https://github.com/Geuthur/$(GENERAL__APPNAME)\n"
    ),
    "demo/__init__.py": (
        '__version__ = "1.0.1"\n__title__ = "Demo"\n\n__package_name__ = "aa-demo"\n'
        '__app_name__ = "demo"\n__app_name_useragent__ = "AA-Demo"\n'
    ),
    "demo/app_settings.py": (
        'DEMO_APP_NAME = getattr(settings, "DEMO_APP_NAME", "Demo")\n'
        "DEMO_STALE_TYPES = {}\n"
    ),
    "demo/apps.py": (
        "# AA Demo\nfrom demo import __version__\n\n\nclass DemoConfig(AppConfig):\n"
        '    name = "demo"\n    verbose_name = f"Demo v{__version__}"\n'
    ),
    "demo/models/general.py": (
        "class General(models.Model):\n    class Meta:\n        abstract = True\n"
        '        verbose_name = "AA-Demo"\n\n    def get_perm(cls, perm):\n'
        '        return f"demo.{perm}"\n'
    ),
    "demo/migrations/__init__.py": "",
    "demo/migrations/0001_initial.py": "# demo migration\n",
    "demo/tests/testdata/app.py": APP_PY,
    "demo/templates/demo/base.html": "{% static 'demo/css/aa-demo.css' %}\n",
    "demo/static/demo/css/aa-demo.css": ".demo-class { color: red; }\n",
    "demo/static/demo/react/js/index-abc.js.map": '{"sources": ["demo/x"]}\n',
    "demo/openapi_2026-08-18.json": '{"demo": "", "examples": [1]}\n',
    "demo/docs/images/preview-1.png": b"\x89PNG\r\n\x1a\n\x00\x00binary demo",
    "aa-demo-models.png": b"\x89PNG\r\n\x1a\n\x00\x00binary demo",
    "CHANGELOG.md": CHANGELOG,
    "LICENSE": (
        "For demo, if you distribute copies of such a program.\n"
        "    AA Demo Module for Alliance Auth\n"
    ),
    "README.md": (
        "# AA Demo\n\nSee https://docs.demo.com and https://demo.org/demos for demos.\n"
        "The settings `aaDemoSettings`, `DemoConfig`, `DEMO_APP_NAME`, "
        "`demo_update_status` and `create_demo` belong to the app.\n"
        "A Demos heading and the word Demos stay.\n"
    ),
    "frontend/src/constants.ts": (
        'export const AppName = "aa-demo";\nexport const ProjectName = "demo";\n'
    ),
    "node_modules/demo/index.js": "module.exports = 'demo';\n",
    "frontend/build/demo.js": "demo\n",
}


def write_template(root: Path) -> None:
    for name, content in FILES.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")


class TestNames(TestCase):
    def test_derived_names(self):
        self.assertEqual(DST.title, "Fleet")
        self.assertEqual(DST.settings_prefix, "FLEET")
        self.assertEqual(DST.user_agent, "AA-Fleet")

    def test_title_from_verbose_name(self):
        self.assertEqual(init_app.title_from_verbose("AA Voices of War"), "VoicesOfWar")
        self.assertEqual(init_app.title_from_verbose("aa Tax-System"), "TaxSystem")
        self.assertEqual(init_app.title_from_verbose("Ledger"), "Ledger")

    def test_rejects_invalid_names(self):
        for names in (
            init_app.Names("Fleet", "aa-fleet", "AA Fleet"),
            init_app.Names("fleet-x", "aa-fleet", "AA Fleet"),
            init_app.Names("class", "aa-fleet", "AA Fleet"),
            init_app.Names("fleet", "AA_Fleet", "AA Fleet"),
            init_app.Names("fleet", "aa-fleet", "AA"),
        ):
            with self.assertRaises(init_app.InitAppError):
                names.validate()


class TestReplaceText(TestCase):
    def setUp(self):
        self.rules = init_app.build_rules(SRC, DST)

    def replace(self, text, **kwargs):
        return init_app.replace_text(text, self.rules, **kwargs)[0]

    def test_replaces_names_at_word_boundaries(self):
        self.assertEqual(
            self.replace("from demo.models import x"), "from fleet.models import x"
        )
        self.assertEqual(self.replace("demo_update_status"), "fleet_update_status")
        self.assertEqual(self.replace("create_demo()"), "create_fleet()")
        self.assertEqual(self.replace("r'^demo/'"), "r'^fleet/'")
        self.assertEqual(self.replace("DEMO_APP_NAME"), "FLEET_APP_NAME")
        self.assertEqual(self.replace("class DemoConfig"), "class FleetConfig")
        self.assertEqual(self.replace("aaDemoSettings"), "aaFleetSettings")
        self.assertEqual(self.replace('"Demo v1"'), '"Fleet v1"')
        self.assertEqual(self.replace("pip install aa-demo"), "pip install aa-fleet")
        self.assertEqual(self.replace("# AA Demo"), "# AA Fleet")
        self.assertEqual(
            self.replace('useragent = "AA-Demo"'), 'useragent = "AA-Fleet"'
        )
        self.assertEqual(self.replace("aa-demo-models.png"), "aa-fleet-models.png")

    def test_keeps_other_words(self):
        for text in (
            "for demos and Demos",
            "https://docs.demo.com/path",
            "https://demo.org/x",
            "demo.net",
            "DEMOS",
            "nodemo",
        ):
            self.assertEqual(self.replace(text), text)

    def test_compound_only_keeps_bare_words(self):
        text = "For demo, see the AA Demo Module and aa-demo, Demo and DEMO."
        self.assertEqual(
            self.replace(text, compound_only=True),
            "For demo, see the AA Fleet Module and aa-fleet, Demo and DEMO.",
        )

    def test_counts_per_rule(self):
        _, counts = init_app.replace_text("demo demo Demo aa-demo", self.rules)
        self.assertEqual(counts, {"package": 2, "title": 1, "app name": 1})


class TestRun(TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        write_template(self.root)

    def read(self, name):
        return (self.root / name).read_text(encoding="utf-8")

    def test_replaces_renames_and_reports(self):
        report = init_app.run(self.root, DST)

        self.assertFalse((self.root / "demo").exists())
        self.assertEqual(
            self.read("fleet/__init__.py"),
            '__version__ = "0.1.0"\n__title__ = "Fleet"\n\n__package_name__ = "aa-fleet"\n'
            '__app_name__ = "fleet"\n__app_name_useragent__ = "AA-Fleet"\n',
        )
        self.assertEqual(
            self.read(".make/config.ini").splitlines()[2:6],
            [
                "[General]",
                "appname = aa-fleet",
                "appname_verbose = AA Fleet",
                "package = fleet",
            ],
        )
        self.assertIn("class FleetConfig", self.read("fleet/apps.py"))
        self.assertIn('verbose_name = "AA-Fleet"', self.read("fleet/models/general.py"))
        self.assertIn('f"fleet.{perm}"', self.read("fleet/models/general.py"))
        self.assertEqual(
            self.read("fleet/templates/fleet/base.html"),
            "{% static 'fleet/css/aa-fleet.css' %}\n",
        )
        self.assertEqual(
            self.read("fleet/static/fleet/css/aa-fleet.css"),
            ".fleet-class { color: red; }\n",
        )
        self.assertEqual(
            self.read("frontend/src/constants.ts"),
            'export const AppName = "aa-fleet";\nexport const ProjectName = "fleet";\n',
        )
        self.assertEqual(
            self.read("README.md"),
            "# AA Fleet\n\nSee https://docs.demo.com and https://demo.org/demos for demos.\n"
            "The settings `aaFleetSettings`, `FleetConfig`, `FLEET_APP_NAME`, "
            "`fleet_update_status` and `create_fleet` belong to the app.\n"
            "A Demos heading and the word Demos stay.\n",
        )
        self.assertEqual(
            self.read("LICENSE"),
            "For demo, if you distribute copies of such a program.\n"
            "    AA Fleet Module for Alliance Auth\n",
        )
        self.assertEqual(
            (self.root / "aa-fleet-models.png").read_bytes(),
            FILES["aa-demo-models.png"],
        )
        self.assertFalse((self.root / "aa-demo-models.png").exists())

        renamed = {old.as_posix(): new.as_posix() for old, new in report.renamed}
        self.assertEqual(
            renamed,
            {
                "demo": "fleet",
                "demo/templates/demo": "demo/templates/fleet",
                "demo/static/demo": "demo/static/fleet",
                "demo/static/demo/css/aa-demo.css": "demo/static/demo/css/aa-fleet.css",
                "aa-demo-models.png": "aa-fleet-models.png",
            },
        )
        self.assertEqual(
            report.replaced[Path("demo/__init__.py")],
            {"user agent": 1, "app name": 1, "title": 1, "package": 1},
        )
        self.assertEqual(report.removed, [])
        self.assertTrue(any("preview-1.png" in hint for hint in report.hints))

    def test_keeps_skipped_files(self):
        init_app.run(self.root, DST)

        self.assertEqual(
            self.read("fleet/static/fleet/react/js/index-abc.js.map"),
            '{"sources": ["demo/x"]}\n',
        )
        self.assertEqual(
            self.read("fleet/openapi_2026-08-18.json"),
            '{"demo": "", "examples": [1]}\n',
        )
        self.assertEqual(
            self.read("node_modules/demo/index.js"), "module.exports = 'demo';\n"
        )
        self.assertEqual(self.read("frontend/build/demo.js"), "demo\n")

    def test_resets_changelog(self):
        init_app.run(self.root, DST)

        self.assertEqual(
            self.read("CHANGELOG.md"),
            "# Changelog\n\n## [In Development] - Unreleased\n\n<!--\nSection Order:\n\n### Added\n-->\n\n"
            "<!-- Your changes go here -->\n\n<!-- Links -->\n\n"
            '[in development]: https://github.com/Geuthur/aa-fleet/commits/master "In Development"\n',
        )

    def test_keeps_migrations_and_override_by_default(self):
        init_app.run(self.root, DST)

        self.assertTrue((self.root / "fleet/migrations/0001_initial.py").is_file())
        self.assertEqual(
            self.read("fleet/migrations/0001_initial.py"), "# fleet migration\n"
        )
        self.assertIn("TEMPLATE ONLY", self.read("fleet/tests/testdata/app.py"))

    def test_drops_migrations(self):
        report = init_app.run(self.root, DST, drop_migrations_=True)

        self.assertFalse((self.root / "fleet/migrations/0001_initial.py").exists())
        self.assertTrue((self.root / "fleet/migrations/__init__.py").is_file())
        self.assertEqual(
            [p.as_posix() for p in report.removed], ["demo/migrations/0001_initial.py"]
        )

    def test_drops_template_override(self):
        report = init_app.run(self.root, DST, drop_template_override_=True)

        app_py = self.read("fleet/tests/testdata/app.py")
        self.assertEqual(
            app_py,
            '''# Third Party
import factory

# AA EVE SDE Factory
from evesde_factory.allianceauth import EveCharacterFactory, UserFactory
from evesde_factory.utils import add_character_to_user

# AA Fleet
from fleet import __app_name__
from fleet.models.character import CharacterOwner


class UserMainFactory(UserFactory):
    """Generate a User object."""

    permissions__ = [f"{__app_name__}.basic_access"]
    scopes__ = CharacterOwner.get_esi_scopes()

    # pylint: disable=no-self-argument
    @factory.post_generation
    def main_character(obj, create, _, **kwargs):
        if not create:
            return
        add_character_to_user(user=obj, character=EveCharacterFactory())
''',
        )
        self.assertTrue(any("still abstract" in hint for hint in report.hints))

    def test_dry_run_changes_nothing(self):
        before = {
            path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()
        }

        report = init_app.run(self.root, DST, drop_migrations_=True, dry_run=True)

        after = {
            path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()
        }
        self.assertEqual(before, after)
        self.assertIn(Path("README.md"), report.replaced)
        self.assertEqual(len(report.renamed), 5)
        self.assertEqual(len(report.removed), 1)

    def test_rejects_same_or_existing_package(self):
        with self.assertRaises(init_app.InitAppError):
            init_app.run(self.root, init_app.Names("demo", "aa-fleet", "AA Fleet"))
        (self.root / "fleet").mkdir()
        with self.assertRaises(init_app.InitAppError):
            init_app.run(self.root, DST)

    def test_main_reports_errors(self):
        self.assertEqual(
            init_app.main(
                [
                    "--root",
                    str(self.root),
                    "--package",
                    "Bad",
                    "--app-name",
                    "aa-x",
                    "--verbose-name",
                    "AA X",
                ]
            ),
            1,
        )
        self.assertEqual(
            init_app.main(
                [
                    "--root",
                    str(self.root),
                    "--package",
                    "fleet",
                    "--app-name",
                    "aa-fleet",
                    "--verbose-name",
                    "AA Fleet",
                ]
            ),
            0,
        )
        self.assertTrue((self.root / "fleet").is_dir())
