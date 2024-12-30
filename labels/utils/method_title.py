import re
from pathlib import Path

import mimesis
import yaml
from mimesis.locales import Locale
from models.core import Defintion

DEFINITIONS = Path("definitions.yaml")
DEFINITIONS_UPDATE = Path("definitions_update.yaml")
TITLE_REGEX = re.compile(r":return: (.+?)(\n|$)")

with DEFINITIONS.open("r", encoding="utf-8") as f:
    release_data = yaml.load(f, Loader=yaml.FullLoader)
    releases = [Defintion(**release_data[r]) for r in release_data]


update = {}

for key in release_data:
    release = Defintion(**release_data[key])
    provider = getattr(mimesis.Generic(Locale.DEFAULT), release.provider)
    method = getattr(provider, release.method)
    doc = method.__doc__
    match = TITLE_REGEX.search(doc)
    title = match.group(1) if match else False
    if title:
        release.title = title
    update[key] = release.model_dump()


with DEFINITIONS_UPDATE.open("w", encoding="utf-8") as f:
    yaml.dump(update, f, Dumper=yaml.Dumper, allow_unicode=True, sort_keys=True)
