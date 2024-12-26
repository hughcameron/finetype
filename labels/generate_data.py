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
    description="Generate fake data using mimesis with given depth and output file.",
)
parser.add_argument(
    "--texts",
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
    "--seed",
    type=int,
    default=42,
    help="Seed for the random generator (default: 42)",
)
args = parser.parse_args()

VALUES = args.texts
PRIORITY = args.priority
OUTFILE = args.output
SEED = args.seed


random.global_seed = SEED


# Function to determine the type of the text
def get_text_type(text):
    if isinstance(text, int):
        return "int"
    if isinstance(text, float):
        return "float"
    if isinstance(text, bool):
        return "bool"
    if isinstance(text, str):
        # Attempt to determine if the string represents a number
        if text.isdigit():
            return "int"
        try:
            float(text)
            return "float"
        except ValueError:
            return "str"
    elif isinstance(text, list) or isinstance(text, tuple):
        if text:
            elem_types = set(get_text_type(elem) for elem in text)
            if len(elem_types) == 1:
                return f"List[{elem_types.pop()}]"
            types_str = ", ".join(sorted(elem_types))
            return f"List[Union[{types_str}]]"
        return "List[Any]"
    elif isinstance(text, dict):
        if text:
            key_types = set(get_text_type(k) for k in text.keys())
            text_types = set(get_text_type(v) for v in text.texts())
            if len(key_types) == 1 and len(text_types) == 1:
                return f"Dict[{key_types.pop()}, {text_types.pop()}]"
            key_types_str = ", ".join(sorted(key_types))
            text_types_str = ", ".join(sorted(text_types))
            return f"Dict[Union[{key_types_str}], Union[{text_types_str}]]"
        return "Dict[Any, Any]"
    elif isinstance(text, (datetime.date, datetime.datetime)):
        return "str"  # Dates are serialized to ISO format strings
    else:
        return "Any"


with open("finetype_releases.yaml", encoding="utf-8") as f:
    release_data = yaml.load(f, Loader=CoreLoader)
    releases = [Release(**release_data[r]) for r in release_data]

total_iterations = 0
for release in releases:
    if release.release_priority >= PRIORITY:
        total_iterations += len(release.locales)

# Start tqdm progress bar
with (
    tqdm(total=total_iterations, desc="Generating data") as pbar,
    open(
        OUTFILE,
        "w",
        encoding="utf-8",
    ) as ndjson_file,
):
    for release in releases:
        if release.release_priority >= PRIORITY:
            # For each locale_selection
            for locale_name in release.locales:
                # Instantiate a Fieldset object
                locale = getattr(Locale, locale_name)
                fs = Fieldset(locale=locale, i=VALUES)  # Generate VALUES texts at once
                provider = getattr(mimesis.Generic(locale), release.provider)
                method = getattr(provider, release.method)

                # Generate texts using Fieldset
                texts = fs(f"{release.provider}.{release.method}")
                # Determine data type from the first text
                if texts:
                    data_type = get_text_type(texts[0])
                    local_class = "UNIVERSAL" if release.universal else locale_name
                    # Write data to ndjson file
                    for text in texts:
                        data = {
                            "class": f"{release.provider}.{release.method}.{local_class}",
                            "provider": release.provider,
                            "method": release.method,
                            "locale": local_class,
                            # "data_type": data_type, TODO: Add data type to evaluation
                            "text": text,
                        }
                        ndjson_file.write(json.dumps(data, ensure_ascii=False) + "\n")

            pbar.update(1)

print(f"Data generation complete. Saved to {OUTFILE}.")
