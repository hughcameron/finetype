import argparse
import asyncio
from pathlib import Path

import aiofiles
from domains.collection import generic_set, load_release
from mimesis import random
from models.core import Definition, Domain, Record, Sector
from tqdm.asyncio import tqdm

# Constants
DEFAULT_TEXTS = 1000
DEFAULT_PRIORITY = 5
DEFAULT_OUTPUT = "learning_data/type_domain.ndjson"
DEFAULT_SEED = 42

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Release data using mimesis with given definitions.")
    parser.add_argument("--release", type=str, help="Path to the release definitions file.")
    parser.add_argument("--texts", type=int, default=DEFAULT_TEXTS, help="Number of times to run each method (default: 1000)")
    parser.add_argument("--priority", type=int, default=DEFAULT_PRIORITY, help="Minimum priority of the release to include (default: 5)")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT, help="Output file to write the generated data (default: learning_data/type_domain.ndjson)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Seed for the random generator (default: 42)")
    return parser.parse_args()

def calculate_total_iterations(release, texts: int, priority: int) -> int:
    """
    Calculate the total number of iterations required for data generation.

    Args:
        release: The release object containing domains, sectors, and definitions.
        texts (int): Number of times to run each method.
        priority (int): Minimum priority of the release to include.

    Returns:
        int: Total number of iterations.
    """
    total_iterations = 0
    for domain in release.domains:
        for sector in domain.sectors:
            for definition in sector.definitions:
                if definition.release_priority >= priority:
                    total_iterations += len(definition.locales) * texts
                    for variant in definition.variants:
                        total_iterations += len(definition.locales) * texts
    return total_iterations

async def generate_data_for_locale(
    domain: Domain,
    sector: Sector,
    definition: Definition,
    locale,
    texts: int,
    ndjson_file,
    pbar,
):
    """
    Generate data for a specific locale and write to the output file.

    Args:
        domain (Domain): The domain object.
        sector (Sector): The sector object.
        definition (Definition): The definition object.
        locale: The locale for which data is generated.
        texts (int): Number of times to run each method.
        ndjson_file: The output file to write the generated data.
        pbar: The progress bar object.
    """
    generic = generic_set(locale)
    provider = getattr(generic, sector.name)
    method = getattr(provider, definition.name)

    records = []
    for _ in range(texts):
        record = Record(
            classification=f"{domain.name}.{sector.name}.{definition.name}.{locale.name}",
            text=str(method()),
        )
        records.append(record.model_dump_json())
        pbar.update(1)
    for variant in definition.variants:
        for _ in range(texts):
            record = Record(
                classification=f"{domain.name}.{sector.name}.{definition.name}__{variant.name}.{locale.name}",
                text=str(method(**variant.arguments)),
            )
            records.append(record.model_dump_json())
            pbar.update(1)

    await ndjson_file.write("\n".join(records) + "\n")

async def generate_data(release, texts: int, priority: int, output_file: Path):
    """
    Generate data for all locales and write to the output file.

    Args:
        release: The release object containing domains, sectors, and definitions.
        texts (int): Number of times to run each method.
        priority (int): Minimum priority of the release to include.
        output_file (Path): The output file to write the generated data.
    """
    total_iterations = calculate_total_iterations(release, texts, priority)
    async with aiofiles.open(output_file, "w", encoding="utf-8") as ndjson_file:
        tasks = []
        pbar = tqdm(total=total_iterations, desc="Generating data", unit_scale=True)
        try:
            for domain in release.domains:
                for sector in domain.sectors:
                    for definition in sector.definitions:
                        if definition.release_priority >= priority:
                            for locale in definition.locales:
                                task = generate_data_for_locale(
                                    domain,
                                    sector,
                                    definition,
                                    locale,
                                    texts,
                                    ndjson_file,
                                    pbar,
                                )
                                tasks.append(task)
            await asyncio.gather(*tasks)
        finally:
            pbar.close()

    print(f"Data generation complete. Saved to {output_file}.")

def main():
    """
    Main function to parse arguments, set the random seed, load the release, and generate data.
    """
    args = parse_arguments()
    random.global_seed = args.seed

    release = load_release(args.release) if args.release else load_release()
    asyncio.run(generate_data(release, args.texts, args.priority, Path(args.output)))

if __name__ == "__main__":
    main()
