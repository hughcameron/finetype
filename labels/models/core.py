from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel


class Reference(BaseModel):
    title: str
    link: str


class Designation(str, Enum):
    universal = "universal"
    locale_specific = "locale_specific"
    broad_characters = "broad_characters"
    broad_numbers = "broad_numbers"
    broad_object = "broad_object"
    broad_words = "broad_words"
    duplicate = "duplicate"
    system_internal = "system_internal"

    def __repr__(self) -> str:
        return self.value


class Definition(BaseModel):
    """
    A definition to release of data generation.
    """

    provider: str
    method: str
    designation: Designation
    primitive: str
    locales: List[str]
    samples: List[Any]
    release_priority: int
    title: Optional[str] = None
    description: Optional[str] = None
    references: Optional[List[Reference]] = None
    aliases: Optional[List[str]] = None
    notes: Optional[str] = None


class Record(BaseModel):
    """
    A record of data generated.
    """

    tag: str
    text: str
