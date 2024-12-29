import datetime
from typing import Any


def determine_primitive(text: Any) -> str:
    """
    Function to determine the type of the input text.

    :param text: The input to determine the type of.
    :return: The type of the input as a string.
    """
    type_map = {
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

    if text is None:
        return "None"

    text_type = type(text)

    if text_type in type_map:
        if text_type in {list, tuple}:
            if text:
                elem_types = {determine_primitive(elem) for elem in text}
                if len(elem_types) == 1:
                    return f"List[{elem_types.pop()}]"
                types_str = ", ".join(sorted(elem_types))
                return f"List[Union[{types_str}]]"
            return "List[Any]"
        if text_type is dict:
            if text:
                key_types = {determine_primitive(k) for k in text}
                value_types = {determine_primitive(v) for v in text.values()}
                if len(key_types) == 1 and len(value_types) == 1:
                    return f"Dict[{key_types.pop()}, {value_types.pop()}]"
                key_types_str = ", ".join(sorted(key_types))
                value_types_str = ", ".join(sorted(value_types))
                return f"Dict[Union[{key_types_str}], Union[{value_types_str}]]"
            return "Dict[Any, Any]"
        if text_type in {datetime.date, datetime.datetime}:
            return "str"
        return type_map[text_type]

    if isinstance(text, str):
        # Attempt to determine if the string represents a number
        if text.isdigit():
            return "int"
        try:
            float(text)
            return "float"
        except ValueError:
            return "str"

    return "Any"
