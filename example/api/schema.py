# Standard Library
from typing import Any

# Third Party
from ninja import Schema


class UserData(Schema):
    """
    Schema for user data, including character ID and character name.

    Parameters:
        user_id (int): The ID of the user.
        character_id (int): The ID of the character associated with the user.
        character_name (str): The name of the character.
        portrait (str | None): The URL or path to the character's portrait image.
        notification (boolean): The notification status for the user.
    """

    user_id: int
    character_id: int
    character_name: str
    portrait: str | None = None

    notification: bool


class DataTableSchema(Schema):
    """
    Schema for a data table entry, including raw data, display text, sorting information, translation, and dropdown text.

    Parameters:
        raw (Any): The raw data for the table entry.
        display (str): The display text for the table entry.
        sort (str | None): The sorting information for the table entry.
        translation (str | None): The translation for the table entry.
        dropdown_text (str | None): The dropdown text for the table entry.
    """

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


# React Stuff


class ModalSchema(Schema):
    """Schema for modal dialog data."""

    title: str
    text: str
    icon: str
    modal_id: str
    url: str
    color: str | None = None
    buttonText: str | None = None


class MenuLink(Schema):
    """
    Represents a link in the menu.

    Parameters:
        name (str): The name of the menu link.
        link (str | None): The URL or path the menu link points to.
    """

    name: str
    link: str = None


class MenuCategory(MenuLink):
    """
    Represents a category in the menu, which can contain multiple links.

    Parameters:
        links (list[MenuLink]): A list of links under this category.
        name (str): The name of the menu category.
        link (str | None): The optional link for the menu category.
    """

    links: list[MenuLink] = None


class MenuModalSchema(Schema):
    """Schema for menu modals, including the example modal."""

    create_example: ModalSchema | None = None


class MenuSchema(Schema):
    """
    Schema for the overall menu, including links and modals.

    Parameters:
        links (list[MenuLink]): The list of links in the menu.
        modals (MenuModalSchema | None): The modals associated with the menu.
    """

    links: list[MenuLink] = []
    modals: MenuModalSchema | None = None
