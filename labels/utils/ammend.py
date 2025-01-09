"Create, Update, Delete Definitions"

import argparse
import csv
import json
from pathlib import Path

import yaml
from models.core import Definition

DEFINITIONS = Path("definitions.yaml")


def load_definitions():
    with DEFINITIONS.open("r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def save_definitions(definitions):
    with DEFINITIONS.open("w", encoding="utf-8") as f:
        yaml.dump(
            definitions,
            f,
            Dumper=yaml.Dumper,
            allow_unicode=True,
            sort_keys=True,
        )


def read_file(file_path):
    if file_path.endswith(".tsv"):
        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            return list(reader)
    elif file_path.endswith(".json"):
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported file format. Only TSV and JSON are supported.")


def update_definitions(file_path):
    definitions = load_definitions()
    rows = read_file(file_path)
    for row in rows:
        key = row.pop("key")
        if key in definitions:
            new_def = definitions[key].copy()
            new_def.update(row)
            valid = Definition(**new_def).model_dump(mode="json")
            definitions[key] = valid
        else:
            print(f"Warning: Key {key} not found in definitions.")
    save_definitions(definitions)


def delete_definitions(file_path):
    definitions = load_definitions()
    rows = read_file(file_path)
    for row in rows:
        key = row["key"]
        if key in definitions:
            del definitions[key]
        else:
            print(f"Warning: Key {key} not found in definitions.")
    save_definitions(definitions)


def create_definitions(file_path):
    definitions = load_definitions()
    rows = read_file(file_path)
    for row in rows:
        key = row.pop("key")
        if key not in definitions:
            definitions[key] = row
        else:
            print(f"Warning: Key {key} already exists in definitions.")
    save_definitions(definitions)


def main():
    parser = argparse.ArgumentParser(
        description="Manage definitions in definitions.yaml",
    )
    parser.add_argument(
        "--update",
        help="TSV or JSON file with definition keys and fields to update",
    )
    parser.add_argument(
        "--delete",
        help="TSV or JSON file with definition keys to delete",
    )
    parser.add_argument(
        "--create",
        help="TSV or JSON file with definition fields to create",
    )

    args = parser.parse_args()

    if args.update:
        update_definitions(args.update)
    if args.delete:
        delete_definitions(args.delete)
    if args.create:
        create_definitions(args.create)


if __name__ == "__main__":
    main()
