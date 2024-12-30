from typing import Any, List, Optional

from pydantic import BaseModel


class Defintion(BaseModel):
    """
    A definition to release of data generation.
    """

    provider: str
    method: str
    designation: str
    universal: bool
    primitive: str
    locales: List[str]
    samples: List[Any]
    release_priority: int
    title: Optional[str] = None
    description: Optional[str] = None
    aliases: Optional[List[str]] = None
    notes: Optional[str] = None


class Record(BaseModel):
    """
    A record of data generated.
    """

    tag: str
    text: str
