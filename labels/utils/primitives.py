import datetime
from pathlib import Path
from typing import Any, Dict, List, Union

import mimesis
import yaml
from mimesis.locales import Locale
from models.core import Defintion

DEFINITIONS = Path("definitions.yaml")
DEFINITIONS_UPDATE = Path("definitions_update.yaml")

TYPE_MAP = {
    int: "int",
    float: "float",
    bool: "bool",
    str: "str",
    list: "List",
    tuple: "List",
    dict: "Dict",
    datetime.date: "str",
    datetime.datetime: "str",
}


def determine_primitive(text: Any) -> str:
    """
    Determine the type of the input text and return it as a string.

    :param text: The input to determine the type of.
    :return: The type of the input as a string.
    """
    if text is None:
        return "None"

    text_type = type(text)

    if text_type in TYPE_MAP:
        return handle_mapped_type(text, text_type)

    if isinstance(text, str):
        return determine_string_type(text)

    return "Any"


def handle_mapped_type(text: Any, text_type: type) -> str:
    """
    Handle types that are directly mapped in the TYPE_MAP.

    :param text: The input to determine the type of.
    :param text_type: The type of the input.
    :return: The type of the input as a string.
    """
    if text_type in {list, tuple}:
        return determine_list_type(text)
    if text_type is dict:
        return determine_dict_type(text)
    if text_type in {datetime.date, datetime.datetime}:
        return "str"
    return TYPE_MAP[text_type]


def determine_list_type(text: Union[List[Any], tuple]) -> str:
    """
    Determine the type of a list or tuple.

    :param text: The list or tuple to determine the type of.
    :return: The type of the list or tuple as a string.
    """
    if text:
        elem_types = {determine_primitive(elem) for elem in text}
        if len(elem_types) == 1:
            return f"List[{elem_types.pop()}]"
        types_str = ", ".join(sorted(elem_types))
        return f"List[Union[{types_str}]]"
    return "List[Any]"


def determine_dict_type(text: Dict[Any, Any]) -> str:
    """
    Determine the type of a dictionary.

    :param text: The dictionary to determine the type of.
    :return: The type of the dictionary as a string.
    """
    if text:
        key_types = {determine_primitive(k) for k in text}
        value_types = {determine_primitive(v) for v in text.values()}
        if len(key_types) == 1 and len(value_types) == 1:
            return f"Dict[{key_types.pop()}, {value_types.pop()}]"
        key_types_str = ", ".join(sorted(key_types))
        value_types_str = ", ".join(sorted(value_types))
        return f"Dict[Union[{key_types_str}], Union[{value_types_str}]]"
    return "Dict[Any, Any]"


def determine_string_type(text: str) -> str:
    """
    Determine if a string represents a number or should be treated as a string.

    :param text: The string to determine the type of.
    :return: The type of the string as a string.
    """
    if text.isdigit():
        return "int"
    try:
        float(text)
        return "float"
    except ValueError:
        return "str"


with DEFINITIONS.open("r", encoding="utf-8") as f:
    release_data = yaml.load(f, Loader=yaml.FullLoader)
    releases = [Defintion(**release_data[r]) for r in release_data]


update = {}

for key in release_data:
    release = Defintion(**release_data[key])
    provider = getattr(mimesis.Generic(Locale.DEFAULT), release.provider)
    method = getattr(provider, release.method)
    release.primitive = determine_primitive(release.samples[0])
    update[key] = release.model_dump()


with DEFINITIONS_UPDATE.open("w", encoding="utf-8") as f:
    yaml.dump(update, f, Dumper=yaml.Dumper, allow_unicode=True, sort_keys=True)
