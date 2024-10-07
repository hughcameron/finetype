import argparse
import datetime
import json
from dataclasses import dataclass
from typing import List, Optional

import mimesis
import yaml
from mimesis import Fieldset, random
from mimesis.locales import Locale
from tqdm import tqdm
from yamlcore import CoreLoader


@dataclass
class Release:
    """
    A dataclass to represent a release of data generation.
    """

    provider: str
    method: str
    designation: str
    universal: bool
    release_priority: int
    locales: List[str]
    samples: List[str]
    notes: Optional[str] = None


parser = argparse.ArgumentParser(
    description="Generate fake data using mimesis with given depth and output file."
)
parser.add_argument(
    "--values",
    type=int,
    default=1000,
    help="Number of times to run each method (default: 1000)",
)
parser.add_argument(
    "--priority",
    type=int,
    default=5,
    help="Minimum priority of the release to include (default: 5)",
)
parser.add_argument(
    "--output",
    type=str,
    default="learning_data/type_domain.ndjson",
    help="Output file to write the generated data (default: learning_data/type_domain.ndjson)",
)
parser.add_argument(
    "--seed", type=int, default=42, help="Seed for the random generator (default: 42)"
)
args = parser.parse_args()

VALUES = args.values
PRIORITY = args.priority
OUTFILE = args.output
SEED = args.seed


random.global_seed = SEED


# Function to determine the type of the value
def get_value_type(value):
    if isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, bool):
        return "bool"
    elif isinstance(value, str):
        # Attempt to determine if the string represents a number
        if value.isdigit():
            return "int"
        try:
            float(value)
            return "float"
        except ValueError:
            return "str"
    elif isinstance(value, list) or isinstance(value, tuple):
        if value:
            elem_types = set(get_value_type(elem) for elem in value)
            if len(elem_types) == 1:
                return f"List[{elem_types.pop()}]"
            else:
                types_str = ", ".join(sorted(elem_types))
                return f"List[Union[{types_str}]]"
        else:
            return "List[Any]"
    elif isinstance(value, dict):
        if value:
            key_types = set(get_value_type(k) for k in value.keys())
            value_types = set(get_value_type(v) for v in value.values())
            if len(key_types) == 1 and len(value_types) == 1:
                return f"Dict[{key_types.pop()}, {value_types.pop()}]"
            else:
                key_types_str = ", ".join(sorted(key_types))
                value_types_str = ", ".join(sorted(value_types))
                return f"Dict[Union[{key_types_str}], Union[{value_types_str}]]"
        else:
            return "Dict[Any, Any]"
    elif isinstance(value, (datetime.date, datetime.datetime)):
        return "str"  # Dates are serialized to ISO format strings
    else:
        return "Any"


with open("finetype_releases.yaml", "r", encoding="utf-8") as f:
    release_data = yaml.load(f, Loader=CoreLoader)
    releases = [Release(**release_data[r]) for r in release_data]

total_iterations = 0
for release in releases:
    if release.release_priority >= PRIORITY:
        total_iterations += len(release.locales)

# Start tqdm progress bar
with tqdm(total=total_iterations, desc="Generating data") as pbar, open(
    OUTFILE, "w", encoding="utf-8"
) as ndjson_file:

    for release in releases:
        if release.release_priority >= PRIORITY:
            # For each locale_selection
            for locale_name in release.locales:
                # Instantiate a Fieldset object
                locale = getattr(Locale, locale_name)
                fs = Fieldset(locale=locale, i=VALUES)  # Generate VALUES values at once
                provider = getattr(mimesis.Generic(locale), release.provider)
                method = getattr(provider, release.method)

                # Generate values using Fieldset
                values = fs(f"{release.provider}.{release.method}")
                # Determine data type from the first value
                if values:
                    data_type = get_value_type(values[0])
                    # Write data to ndjson file
                    for value in values:
                        data = {
                            "locale": "UNIVERSAL" if release.universal else locale_name,
                            "provider": release.provider,
                            "method": release.method,
                            "data_type": data_type,
                            "value": value,
                        }
                        ndjson_file.write(json.dumps(data, ensure_ascii=False) + "\n")

            pbar.update(1)

print(f"Data generation complete. Saved to {OUTFILE}.")
