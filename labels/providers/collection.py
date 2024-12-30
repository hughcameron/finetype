from mimesis import Generic
from mimesis.locales import Locale

from providers.datetime import Datetime

FINETYPE_PROVIDERS = [Datetime]


def generic_set(locale: Locale | str) -> Generic:
    if isinstance(locale, str):
        locale = getattr(Locale, locale)
    generic = Generic(locale)
    for provider in FINETYPE_PROVIDERS:
        generic.add_provider(provider)
    return generic
