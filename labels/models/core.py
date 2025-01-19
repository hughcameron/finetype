from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, field_validator


class Designation(str, Enum):
    universal = "universal"
    locale_specific = "locale_specific"
    broad_characters = "broad_characters"
    broad_numbers = "broad_numbers"
    broad_object = "broad_object"
    broad_words = "broad_words"
    duplicate = "duplicate"
    system_internal = "system_internal"


class Domain(BaseModel):
    name: str
    sectors: list[Sector]


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
    UNIVERSAL = "universal"

    @classmethod
    def _missing_(cls, value: str) -> Locale:
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    @classmethod
    def from_value(cls, value: str) -> Locale:
        try:
            return cls[value]
        except KeyError:
            return cls._missing_(value)


class Record(BaseModel):
    """
    A record of data generated.
    """

    classification: str
    text: str


class Reference(BaseModel):
    title: str
    link: str


class Release(BaseModel):
    domains: list[Domain]


class Sector(BaseModel):
    name: str
    definitions: list[Definition]


class Variation(BaseModel):
    name: str
    arguments: dict


class Definition(BaseModel):
    """
    A definition to release of data generation.
    """

    name: str
    designation: Designation
    primitive: str
    locales: list[Locale]
    variations: list[Variation]
    release_priority: int
    title: str | None = None
    description: str | None = None
    references: list[Reference] | None = None
    aliases: list[str] | None = None
    notes: str | None = None

    @field_validator("locales", mode="before")
    @classmethod
    def lower_locales(cls, values: list[str]) -> list[Locale] | bool:
        if isinstance(values, list):
            return [Locale.from_value(value) for value in values]
        return False

    class Config:
        use_enum_values = False
        json_encoders = {Locale: lambda v: v.name}
