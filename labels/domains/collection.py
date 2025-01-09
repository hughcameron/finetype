from mimesis import Generic
from models.core import Locale, Release
from pydantic_yaml import parse_yaml_file_as

from domains.datetime.date import Date
from domains.datetime.datetime import Datetime
from domains.datetime.time import Time

FINETYPE_PROVIDERS = [Datetime, Date, Time]


def generic_set(locale: Locale | str) -> Generic:
    if locale in (Locale.UNIVERSAL, "universal"):
        locale = Locale.EN
    if isinstance(locale, str):
        locale = getattr(Locale, locale)
    generic = Generic(locale)
    for provider in FINETYPE_PROVIDERS:
        generic.add_provider(provider)
    return generic


def load_releases(release_path) -> Release:
    return parse_yaml_file_as(Release, release_path)
