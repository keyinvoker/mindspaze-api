import re


def remove_special_characters(input_string: str) -> str:
    result = re.sub(r"[^a-zA-Z]", " ", input_string)
    return result
