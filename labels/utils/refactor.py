import csv
import json
from pathlib import Path
from typing import Any

import yaml
from domains.collection import save_yaml_model
from models.core import Definition, Designation, Domain, Locale, Reference
from pydantic import BaseModel, field_validator

DOMAINS_FILE = "domain_match.tsv"
DEFINITIONS_FILE = Path("definitions.yaml")


class PriorDefModel(BaseModel):
    """
    A definition to release of data generation.
    """

    designation: Designation
    primitive: str
    provider: str
    method: str
    locales: list[Locale]
    samples: list[Any]
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


def read_file(file_path):
    """
    Reads a file and returns its content based on the file extension.

    Args:
        file_path (str): Path to the file.

    Returns:
        list or dict: Content of the file.

    Raises:
        ValueError: If the file format is not supported.
    """
    if file_path.endswith(".tsv"):
        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            return list(reader)
    elif file_path.endswith(".json"):
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format. Only TSV and JSON are supported.")


def load_definitions(file_path):
    """
    Loads definitions from a YAML file.

    Args:
        file_path (Path): Path to the YAML file.

    Returns:
        list: List of PriorDefModel objects.
    """
    with file_path.open("r", encoding="utf-8") as f:
        release_data = yaml.load(f, Loader=yaml.FullLoader)
        return [PriorDefModel(**release_data[r]) for r in release_data]


def build_domains_dict(domains_file):
    """
    Builds a dictionary mapping sector and definition to domain.

    Args:
        domains_file (str): Path to the TSV file containing domain mappings.

    Returns:
        dict: Dictionary mapping sector.definition to domain.
    """
    domains = {}
    for row in read_file(domains_file):
        key = f"{row['sector']}.{row['definition']}"
        domains[key] = row["domain"]
    return domains


def build_definition_tree(releases, domains):
    """
    Builds a nested dictionary structure for definitions organized by domain and sector.

    Args:
        releases (list): List of PriorDefModel objects.
        domains (dict): Dictionary mapping sector.definition to domain.

    Returns:
        dict: Nested dictionary structure for definitions.
    """
    definition_tree = {}
    for r in releases:
        r_data = r.model_dump(mode="json")
        sector_name = r_data.pop("provider")
        definition_name = r_data.pop("method")
        domain_name = domains[f"{sector_name}.{definition_name}"]
        r_data["name"] = definition_name

        if domain_name not in definition_tree:
            definition_tree[domain_name] = {}

        if sector_name not in definition_tree[domain_name]:
            definition_tree[domain_name][sector_name] = {
                "name": sector_name,
                "definitions": [],
            }

        definition_tree[domain_name][sector_name]["definitions"].append(
            Definition(**r_data),
        )
    return definition_tree


def save_definition_tree(definition_tree):
    """
    Saves the definition tree to YAML files organized by domain and sector.

    Args:
        definition_tree (dict): Nested dictionary structure for definitions.
    """
    for domain_name, sectors in definition_tree.items():
        print("domain name:", domain_name)

        domain_dict = {"name": domain_name, "sectors": list(sectors.values())}
        domain_data = Domain(**domain_dict)

        doc_path = Path(f"domains/{domain_name}/domain.yaml")
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        save_yaml_model(domain_data, doc_path)

        for sector_name in sectors:
            sector_path = Path(f"domains/{domain_name}/{sector_name}.py")
            if not sector_path.exists():
                sector_path.write_text("")


def main():
    releases = load_definitions(DEFINITIONS_FILE)
    domains = build_domains_dict(DOMAINS_FILE)
    definition_tree = build_definition_tree(releases, domains)
    save_definition_tree(definition_tree)


if __name__ == "__main__":
    main()
