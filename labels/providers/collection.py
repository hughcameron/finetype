from enum import Enum
from typing import List

from mimesis import Generic

from providers.datetime import Datetime

FINETYPE_PROVIDERS = [Datetime]


class Locale(Enum):
    """This class provides access to the supported locales from one place.

    An argument for all local-depend providers.
    """

    AR_AE = "ar-ae"
    AR_DZ = "ar-dz"
    AR_EG = "ar-eg"
    AR_JO = "ar-jo"
    AR_OM = "ar-om"
    AR_SY = "ar-sy"
    AR_YE = "ar-ye"
    CS = "cs"
    DA = "da"
    DE = "de"
    DE_AT = "de-at"
    DE_CH = "de-ch"
    EL = "el"
    EN = "en"
    EN_AU = "en-au"
    EN_CA = "en-ca"
    EN_GB = "en-gb"
    ES = "es"
    ES_MX = "es-mx"
    ET = "et"
    FA = "fa"
    FI = "fi"
    FR = "fr"
    HU = "hu"
    HR = "hr"
    IS = "is"
    IT = "it"
    JA = "ja"
    KK = "kk"
    KO = "ko"
    NL = "nl"
    NL_BE = "nl-be"
    NO = "no"
    PL = "pl"
    PT = "pt"
    PT_BR = "pt-br"
    RU = "ru"
    SK = "sk"
    SV = "sv"
    TR = "tr"
    UK = "uk"
    ZH = "zh"
    DEFAULT = EN
    UNIVERSAL = EN

    @classmethod
    def values(cls) -> List[str]:
        return [i.value for i in cls.__members__.values()]


def generic_set(locale: Locale | str) -> Generic:
    if isinstance(locale, str):
        locale = getattr(Locale, locale)
    generic = Generic(locale)
    for provider in FINETYPE_PROVIDERS:
        generic.add_provider(provider)
    return generic
