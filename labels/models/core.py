from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Defintion:
    """
    A definition to release of data generation.
    """

    provider: str
    method: str
    designation: str
    universal: bool
    release_priority: int
    locales: List[str]
    samples: List[str]
    notes: Optional[str] = None
