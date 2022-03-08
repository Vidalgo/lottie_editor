from typing import Any, Union, get_args, get_origin


def is_annotation_optional(annotation: Any):
    """
    Checks if the given annotation is Optional.

    Args:
        annotation (Any): annotation to check

    Returns:
        True - annotation is Optional, False otherwise

    References:
        https://stackoverflow.com/questions/56832881/check-if-a-field-is-typing-optional
    """
    return get_origin(annotation) is Union and type(None) in get_args(annotation)
