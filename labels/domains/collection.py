from collections.abc import Generator
from pathlib import Path

import yaml
from mimesis import Generic
from models.core import Locale, Release, Sector
from pydantic import BaseModel

from domains.datetime.date import Date
from domains.datetime.datetime import Datetime
from domains.datetime.time import Time

FINETYPE_PROVIDERS = [Datetime, Date, Time]
DOMAINS_DIR = Path("domains")
SECTOR_CONFIGS = DOMAINS_DIR.rglob("*.yaml")


def generic_set(locale: Locale | str = Locale.UNIVERSAL) -> Generic:
    if locale in (Locale.UNIVERSAL, "universal"):
        locale = Locale.EN
    if isinstance(locale, str):
        locale = Locale(locale)
    generic = Generic(locale)
    for provider in FINETYPE_PROVIDERS:
        generic.add_provider(provider)
    return generic


def load_yaml_model(model: BaseModel, path: Path):
    with path.open("r", encoding="utf-8") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        return model.parse_obj(data)


def save_yaml_model(model: BaseModel, path: Path):
    with path.open("w", encoding="utf-8") as file:
        yaml.dump(
            model.model_dump(mode="json"),
            file,
            Dumper=yaml.Dumper,
            allow_unicode=True,
            sort_keys=False,
        )


def load_sector(sector_config: Path) -> tuple[str, Sector]:
    return sector_config.parent.stem, load_yaml_model(Sector, sector_config)


def load_release(sector_configs: Generator[Path] = SECTOR_CONFIGS) -> Release:
    release_data = {}
    for sector_config in sector_configs:
        domain, sector = load_sector(sector_config)
        release_data.setdefault(domain, {"name": domain, "sectors": []})
        release_data[domain]["sectors"].append(sector)
    return Release(domains=list(release_data.values()))
