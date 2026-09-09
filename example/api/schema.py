# Standard Library
from typing import Any

# Third Party
from ninja import Schema


class DataTableSchema(Schema):
    raw: Any
    display: str
    sort: str | None = None
    translation: str | None = None
    dropdown_text: str | None = None


class ExampleSchema(Schema):
    character_id: int | None = None
    character_name: str | None = None
    corporation_id: int | None = None
    corporation_name: str | None = None
