from collections.abc import Generator
from pathlib import Path

import yaml
from mimesis import Generic
from models.core import Domain, Locale, Release
from pydantic import BaseModel

from domains.datetime.date import Date
from domains.datetime.datetime import Datetime
from domains.datetime.time import Time

FINETYPE_PROVIDERS = [Datetime, Date, Time]


def generic_set(locale: Locale | str) -> Generic:
    if locale in (Locale.UNIVERSAL, "universal"):
        locale = Locale.EN
    if isinstance(locale, str):
        locale = getattr(Locale, locale)
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


def load_domain(domain_config: Path) -> Domain:
    return load_yaml_model(Domain, domain_config)


def load_releases(domain_configs: Generator[Path]) -> Release:
    domains = [load_domain(conf) for conf in domain_configs]
    return Release(domains=domains)
