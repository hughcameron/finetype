import datetime
import inspect
import json

from faker import Faker
from tqdm import tqdm  # Import tqdm

RUNCOUNT = 1000  # Number of times to run each method

LOCALES = [
    "ar_AA",
    "ar_AE",
    "ar_BH",
    "ar_EG",
    "ar_JO",
    "ar_PS",
    "ar_SA",
    "az_AZ",
    "bg_BG",
    "bn_BD",
    "bs_BA",
    "cs_CZ",
    "da_DK",
    "de_AT",
    "de_CH",
    "de_DE",
    "dk_DK",
    "el_CY",
    "el_GR",
    "en_AU",
    "en_BD",
    "en_CA",
    "en_GB",
    "en_IE",
    "en_IN",
    "en_MS",
    "en_NZ",
    "en_PH",
    "en_PK",
    "en_TH",
    "en_US",
    "es_AR",
    "es_CA",
    "es_CL",
    "es_CO",
    "es_ES",
    "es_MX",
    "et_EE",
    "fa_IR",
    "fi_FI",
    "fil_PH",
    "fr_BE",
    "fr_CA",
    "fr_CH",
    "fr_FR",
    # 'fr_QC',
    "ga_IE",
    "he_IL",
    "hi_IN",
    "hr_HR",
    "hu_HU",
    "hy_AM",
    "id_ID",
    "it_CH",
    "it_IT",
    "ja_JP",
    "ka_GE",
    "ko_KR",
    "lb_LU",
    "lt_LT",
    "lv_LV",
    "mt_MT",
    "ne_NP",
    "nl_BE",
    "nl_NL",
    "no_NO",
    "or_IN",
    "pl_PL",
    "pt_BR",
    "pt_PT",
    "ro_RO",
    "ru_RU",
    "sk_SK",
    "sl_SI",
    "sq_AL",
    "sv_SE",
    "ta_IN",
    "th_TH",
    "tl_PH",
    "tr_TR",
    "tw_GH",
    "uk_UA",
    "vi_VN",
    "yo_NG",
    "zh_CN",
    "zh_TW",
    "zu_ZA",
]

RESTRICTED_METHODS = [
    "bothify",
    "lexify",
    "hexify",
    "numerify",
    "random_elements",
    "random_digit_not_null_or_empty",
    "random_number",
    "random_digit_above_two",
    "random_element",
    "random_choices",
    "random_letters",
    "random_uppercase_letter",
    "random_sample",
    "random_digit_or_empty",
    "random_int",
    "random_letter",
    "random_digit",
    "random_lowercase_letter",
    "random_digit_not_null",
    "pydecimal",
    "pylist",
    "pystr_format",
    "pybool",
    "pystruct",
    "pytuple",
    "pyint",
    "pyobject",
    "pystr",
    "pyiterable",
    "pyset",
    "pyfloat",
    "pydict",
    "pytimezone",
]


# Function to safely serialize values
def serialize_value(value):
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, str):
        # Attempt to convert numeric strings to numbers
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass  # Keep as string if not a number
    return value  # Return the value as is


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


# Open a file for writing ndjson data
with open("data/fake_data.ndjson", "w", encoding="utf-8") as file:

    # Iterate over all available locales with tqdm progress bar
    for locale in tqdm(LOCALES, desc="Locales"):
        fake = Faker(locale)
        providers = fake.get_providers()
        provider_methods = {}

        # Collect all provider methods for the current locale
        for provider in providers:
            provider_name = provider.__provider__.split(".")[-1]
            for method_name in dir(provider):
                if (
                    not method_name.startswith("_")
                    and method_name not in RESTRICTED_METHODS
                ):
                    method = getattr(provider, method_name)
                    if callable(method):
                        # Check if the method can be called without required arguments
                        sig = inspect.signature(method)
                        if all(
                            param.default != inspect.Parameter.empty
                            or param.kind
                            in (
                                inspect.Parameter.VAR_POSITIONAL,
                                inspect.Parameter.VAR_KEYWORD,
                            )
                            for param in sig.parameters.values()
                        ):
                            if provider_name not in provider_methods:
                                provider_methods[provider_name] = set()
                            provider_methods[provider_name].add(method_name)

        # Generate and write fake data for each provider method with tqdm progress bar
        for provider_name, methods in provider_methods.items():
            for method in tqdm(
                methods, desc=f"{locale} - {provider_name}", leave=False
            ):
                for _ in range(RUNCOUNT):  # Generate RUNCOUNT values
                    try:
                        value = getattr(fake, method)()

                        # Exclude binary values
                        if isinstance(value, bytes):
                            continue  # Skip binary values

                        # Safely serialize the value
                        serialized_value = serialize_value(value)

                        # Determine the type of the value
                        data_type = get_value_type(serialized_value)

                        # Create a dictionary to hold the data
                        data = {
                            "locale": locale,
                            "provider": provider_name,
                            "method": method,
                            "data_type": data_type,
                            "value": serialized_value,
                        }
                        # Write the JSON object to the ndjson file
                        file.write(json.dumps(data, ensure_ascii=False) + "\n")
                    except Exception as e:
                        # Optionally, you can log the error or skip it
                        error_data = {
                            "locale": locale,
                            "provider": provider_name,
                            "method": method,
                            "error": str(e),
                        }
                        # Write the error data to the ndjson file
                        file.write(json.dumps(error_data, ensure_ascii=False) + "\n")
