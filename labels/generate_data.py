import argparse

import mimesis
from mimesis import Fieldset
from mimesis.locales import Locale
import inspect
import datetime
import json

import argparse

from tqdm import tqdm
from mimesis import random

parser = argparse.ArgumentParser(description="Generate fake data using mimesis with given depth and output file.")
parser.add_argument('--values', type=int, default=1000, help='Number of times to run each method (default: 1000)')
parser.add_argument('--output', type=str, default='data/type_domain.ndjson', help='Output file to write the generated data (default: data/type_domain.ndjson)')
parser.add_argument('--seed', type=int, default=42, help='Seed for the random generator (default: 42)')
args = parser.parse_args()


VALUES = args.values
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

# Get the list of locales
locales_list = [locale for locale in Locale]

# Calculate total iterations for progress bar
total_iterations = 0
for locale in locales_list:
    providers = dir(mimesis.Generic(locale))
    for provider_name in providers:
        provider = getattr(mimesis.Generic(locale), provider_name)
        methods = [func for func in dir(provider) if callable(getattr(provider, func)) and not func.startswith('_')]
        total_iterations += len(methods)

# Start tqdm progress bar
with tqdm(total=total_iterations, desc="Generating data") as pbar, open(OUTFILE, 'w', encoding='utf-8') as ndjson_file:

    # For each locale
    for locale in locales_list:

        # Instantiate a Fieldset object
        fs = Fieldset(locale=locale, i=VALUES)  # Generate VALUES values at once
        # Get the data providers
        providers = dir(mimesis.Generic(locale))
        # For each provider
        for provider_name in providers:
            provider = getattr(mimesis.Generic(locale), provider_name)
            # Get all methods of the provider
            methods = [func for func in dir(provider)
                       if callable(getattr(provider, func)) and not func.startswith('_')]
            # For each method
            for method_name in methods:
                method = getattr(provider, method_name)
                # Check if method accepts no required arguments
                sig = inspect.signature(method)
                params = sig.parameters
                if all(p.default != inspect.Parameter.empty or
                       p.kind == inspect.Parameter.VAR_POSITIONAL or
                       p.kind == inspect.Parameter.VAR_KEYWORD
                       for p in params.values()):
                    # Generate 1000 values at once
                    try:
                        # Generate values using Fieldset
                        values = fs(f"{provider_name}.{method_name}")
                        # Determine data type from the first value
                        if values:
                            data_type = get_value_type(values[0])
                            # Write data to ndjson file
                            for value in values:
                                data = {
                                    'locale': locale.value,
                                    'provider_name': provider_name,
                                    'method': method_name,
                                    'data_type': data_type,
                                    'value': value
                                }
                                ndjson_file.write(json.dumps(data, ensure_ascii=False) + "\n")
                    except Exception:
                        # If there's an error, skip
                        pass
                else:
                    # Method requires arguments, skip
                    pass
                pbar.update(1)

print(f"Data generation complete. Saved to {OUTFILE}.")
