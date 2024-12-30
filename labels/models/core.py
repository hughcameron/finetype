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
    release_priority: int
    locales: List[str]
    samples: List[Any]
    notes: Optional[str] = None


class Record(BaseModel):
    """
    A record of data generated.
    """

    tag: str
    text: str
