from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, field_validator


class Reference(BaseModel):
    title: str
    link: str


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
    UNIVERSAL = EN

    @classmethod
    def values(cls) -> List[str]:
        return [i.value for i in cls.__members__.values()]


class Designation(str, Enum):
    universal = "universal"
    locale_specific = "locale_specific"
    broad_characters = "broad_characters"
    broad_numbers = "broad_numbers"
    broad_object = "broad_object"
    broad_words = "broad_words"
    duplicate = "duplicate"
    system_internal = "system_internal"


class Definition(BaseModel):
    """
    A definition to release of data generation.
    """

    provider: str
    method: str
    designation: Designation
    primitive: str
    locales: List[Locale]
    samples: List[Any]
    release_priority: int
    title: Optional[str] = None
    description: Optional[str] = None
    references: Optional[List[Reference]] = None
    aliases: Optional[List[str]] = None
    notes: Optional[str] = None

    @field_validator("locales", mode="before")
    @classmethod
    def convert_locales(cls, values):
        if isinstance(values, list):
            for v in values:
                assert hasattr(Locale, v), f"{v} is not an attribute of Locale"
            return [getattr(Locale, value) for value in values]


class Record(BaseModel):
    """
    A record of data generated.
    """

    classification: str
    text: str
