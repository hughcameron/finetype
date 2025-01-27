import argparse
import asyncio
from pathlib import Path

import aiofiles
from domains.collection import generic_set, load_release
from mimesis import random
from models.core import Definition, Domain, Record, Sector
from tqdm.asyncio import tqdm

parser = argparse.ArgumentParser(
    description="Release data using mimesis with given definitions.",
)
parser.add_argument(
    "--release",
    type=str,
    help="Path to the release definitions file.",
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
RELEASE_PATH = args.release
OUTFILE = Path(args.output)
SEED = args.seed

random.global_seed = SEED

release = load_release(RELEASE_PATH) if RELEASE_PATH else load_release()

total_iterations = 0
for domain in release.domains:
    for sector in domain.sectors:
        for definition in sector.definitions:
            if definition.release_priority >= PRIORITY:
                total_iterations += len(definition.locales) * TEXTS
                for variant in definition.variants:
                    total_iterations += len(definition.locales) * TEXTS


async def generate_data_for_locale(
    domain: Domain,
    sector: Sector,
    definition: Definition,
    locale,
    ndjson_file,
    pbar,
):
    generic = generic_set(locale)
    provider = getattr(generic, sector.name)
    method = getattr(provider, definition.name)

    records = []
    for _ in range(TEXTS):
        record = Record(
            classification=f"{domain.name}.{sector.name}.{definition.name}.{locale.name}",
            text=str(method()),
        )
        records.append(record.model_dump_json())
        pbar.update(1)  # Update the progress bar for each iteration
    for variant in definition.variants:
        for _ in range(TEXTS):
            record = Record(
                classification=f"{domain.name}.{sector.name}.{definition.name}__{variant.name}.{locale.name}",
                text=str(method(**variant.arguments)),
            )
            records.append(record.model_dump_json())
            pbar.update(1)  # Update the progress bar for each iteration

    await ndjson_file.write("\n".join(records) + "\n")


async def main():
    async with aiofiles.open(OUTFILE, "w", encoding="utf-8") as ndjson_file:
        tasks = []
        pbar = tqdm(total=total_iterations, desc="Generating data", unit_scale=True)
        try:
            for domain in release.domains:
                for sector in domain.sectors:
                    for definition in sector.definitions:
                        if definition.release_priority >= PRIORITY:
                            for locale in definition.locales:
                                task = generate_data_for_locale(
                                    domain,
                                    sector,
                                    definition,
                                    locale,
                                    ndjson_file,
                                    pbar,
                                )
                                tasks.append(task)

            await asyncio.gather(*tasks)
        finally:
            pbar.close()

    print(f"Data generation complete. Saved to {OUTFILE}.")


if __name__ == "__main__":
    asyncio.run(main())
