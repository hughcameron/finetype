import argparse
from pathlib import Path

import mimesis
import yaml
from mimesis import Fieldset, random
from mimesis.locales import Locale
from models.core import Defintion, Record
from tqdm import tqdm
from yamlcore import CoreLoader

parser = argparse.ArgumentParser(
    description="Release data using mimesis with given definitions.",
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

TEXTS = args.texts
PRIORITY = args.priority
OUTFILE = Path(args.output)
SEED = args.seed

DEFINITIONS = Path("definitions.yaml")

random.global_seed = SEED


with DEFINITIONS.open("r", encoding="utf-8") as f:
    release_data = yaml.load(f, Loader=CoreLoader)
    releases = [Defintion(**release_data[r]) for r in release_data]

total_iterations = 0
for release in releases:
    if release.release_priority >= PRIORITY:
        total_iterations += len(release.locales)

# Start tqdm progress bar
with (
    tqdm(total=total_iterations, desc="Generating data") as pbar,
    OUTFILE.open("w", encoding="utf-8") as ndjson_file,
):
    for release in releases:
        if release.release_priority >= PRIORITY:
            # For each locale_selection
            for locale_name in release.locales:
                # Instantiate a Fieldset object
                locale = getattr(Locale, locale_name)
                fs = Fieldset(locale=locale, i=TEXTS)  # Generate VALUES texts at once
                provider = getattr(mimesis.Generic(locale), release.provider)
                method = getattr(provider, release.method)

                # Generate texts using Fieldset
                texts = fs(f"{release.provider}.{release.method}")
                # Determine data type from the first text
                if texts:
                    locale_name = "UNIVERSAL" if release.universal else locale_name
                    # Write data to ndjson file
                    for text in texts:
                        record = Record(
                            tag=f"{release.provider}.{release.method}.{locale_name}",
                            text=str(text),
                        )
                        ndjson_file.write(record.json() + "\n")

            pbar.update(1)

print(f"Data generation complete. Saved to {OUTFILE}.")
