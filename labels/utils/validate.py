from pathlib import Path

import yaml
from domains.collection import generic_set
from models.core import Definition

DEFINITIONS = Path("definitions.yaml")

with DEFINITIONS.open("r", encoding="utf-8") as f:
    release_data = yaml.load(f, Loader=yaml.FullLoader)


for key in release_data:
    print(key)
    release = Definition(**release_data[key])
    for locale_name in release.locales:
        generic = generic_set(locale_name)
        provider = getattr(generic, release.provider)
        method = getattr(provider, release.method)
        assert method() is not None
