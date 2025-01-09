from mimesis import Generic
from models.core import Locale

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
