import csv
import json
from pathlib import Path

import yaml
from models.core import Definition

DEFINITIONS = Path("definitions.yaml")
DEFINITIONS_JSON = Path("definitions.ndjson")
CLASSIFICATIONS_JSON = Path("classifications.ndjson")
DEFINITIONS_TSV = Path("definitions.tsv")

with DEFINITIONS.open("r", encoding="utf-8") as f:
    release_data = yaml.load(f, Loader=yaml.FullLoader)

definitions = []
classifications = []

for key in release_data:
    release = Definition(**release_data[key])
    release_record = release.model_dump(mode="json")
    def_record = release_record.copy()
    def_record["key"] = key
    definitions.append(def_record)
    for locale_name in release.locales:
        classification_qual = f"{release.provider}.{release.method}.{locale_name}"
        cls_record = release_record.copy()
        cls_record["classification"] = classification_qual
        cls_record["locale"] = locale_name
        classifications.append(cls_record)

# Write definitions to definitions.ndjson
with DEFINITIONS_JSON.open("w", encoding="utf-8") as f:
    for definition in definitions:
        f.write(json.dumps(definition) + "\n")

# Write classifications to classifications.ndjson
with CLASSIFICATIONS_JSON.open("w", encoding="utf-8") as f:
    for cls in classifications:
        f.write(json.dumps(cls) + "\n")

# Write definitions to definitions.tsv
with DEFINITIONS_TSV.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=definitions[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(definitions)
