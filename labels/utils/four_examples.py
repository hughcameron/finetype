import random
from pathlib import Path

import yaml
from domains.collection import generic_set
from mimesis import Fieldset
from mimesis.locales import Locale
from models.core import Definition

DEFINITIONS = Path("definitions.yaml")
DEFINITIONS_UPDATE = Path("definitions_update.yaml")
TEXTS = 4

with DEFINITIONS.open("r", encoding="utf-8") as f:
    release_data = yaml.load(f, Loader=yaml.FullLoader)
    releases = [Definition(**release_data[r]) for r in release_data]

update = {}

for key in release_data:
    release = Definition(**release_data[key])
    fs = Fieldset(locale=Locale.DEFAULT, i=TEXTS)  # Generate VALUES texts at once
    generic = generic_set(Locale.DEFAULT)
    provider = getattr(generic, release.provider)
    method = getattr(provider, release.method)
    locale_selection = [random.choice(release.locales) for _ in range(TEXTS)]
    samples = []
    for locale_name in locale_selection:
        sample = method()
        if isinstance(sample, tuple):
            sample = list(sample)
        samples.append(sample)
    release.samples = samples
    update[key] = release.model_dump(mode="json")

with DEFINITIONS_UPDATE.open("w", encoding="utf-8") as f:
    yaml.dump(update, f, Dumper=yaml.Dumper, allow_unicode=True, sort_keys=True)
