#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""CTY value formatting and pretty printing."""

from __future__ import annotations

from collections.abc import Callable
from inspect import signature as _mutmut_signature
from typing import Annotated, Any, ClassVar, cast

from pyvider.cty import (
    CtyBool,
    CtyDynamic,
    CtyList,
    CtyMap,
    CtyNumber,
    CtyObject,
    CtyString,
    CtyTuple,
    CtyValue,
)

MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x__pretty_print_cty_recursive__mutmut_orig(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_1(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = None
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_2(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "XX{\nXX"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_3(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = None
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_4(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(None, value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_5(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], None)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_6(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_7(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(
            dict[str, Any],
        )
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_8(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(None):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_9(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s = " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_10(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s -= " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_11(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) - f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_12(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " / (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_13(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += "XX XX" * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_14(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent - 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_15(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 3) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_16(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s = _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_17(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s -= _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_18(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(None, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_19(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, None)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_20(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_21(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(
                    val,
                )
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_22(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent - 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_23(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 3)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_24(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s = _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_25(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s -= _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_26(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(None, indent + 2)
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_27(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), None
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_28(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(indent + 2)
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_29(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val),
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_30(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(vtype=None, value=val), indent + 2)
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_31(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=None), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_32(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(value=val), indent + 2)
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_33(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(
                        vtype=value.type.attribute_types[key],
                    ),
                    indent + 2,
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_34(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent - 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_35(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 3
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_36(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i <= len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_37(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) + 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_38(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 2:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_39(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s = ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_40(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s -= ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_41(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += "XX,\nXX"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_42(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s = "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_43(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s -= "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_44(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "XX\nXX"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_45(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s = " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_46(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s -= " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_47(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent - "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_48(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " / indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_49(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += "XX XX" * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_50(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "XX}XX"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_51(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = None
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_52(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "XX[\nXX"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_53(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = None
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_54(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(None, value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_55(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], None)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_56(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_57(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(
            list[Any],
        )
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_58(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(None):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_59(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s = " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_60(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s -= " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_61(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " / (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_62(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += "XX XX" * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_63(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent - 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_64(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 3)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_65(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s = _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_66(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s -= _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_67(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(None, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_68(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, None)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_69(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_70(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(
                    item,
                )
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_71(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent - 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_72(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 3)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_73(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s = _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_74(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s -= _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_75(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(None, indent + 2)
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_76(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(vtype=value.type.element_type, value=item), None)
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_77(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(indent + 2)
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_78(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item),
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_79(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(vtype=None, value=item), indent + 2)
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_80(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=None), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_81(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(value=item), indent + 2)
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_82(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(
                        vtype=value.type.element_type,
                    ),
                    indent + 2,
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_83(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent - 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_84(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 3
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_85(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i <= len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_86(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) + 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_87(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 2:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_88(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s = ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_89(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s -= ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_90(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += "XX,\nXX"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_91(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s = "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_92(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s -= "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_93(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "XX\nXX"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_94(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s = " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_95(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s -= " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_96(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent - "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_97(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " / indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_98(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += "XX XX" * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_99(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "XX]XX"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_100(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = None
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_101(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "XX{\nXX"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_102(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = None
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_103(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(None, value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_104(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], None)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_105(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_106(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(
            dict[str, Any],
        )
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_107(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(None):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_108(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s = " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_109(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s -= " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_110(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) - f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_111(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " / (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_112(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += "XX XX" * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_113(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent - 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_114(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 3) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_115(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s = _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_116(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s -= _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_117(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(None, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_118(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, None)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_119(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_120(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(
                    val,
                )
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_121(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent - 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_122(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 3)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_123(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s = _pretty_print_cty_recursive(CtyValue(vtype=value.type.element_type, value=val), indent + 2)
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_124(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s -= _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_125(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(None, indent + 2)
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_126(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(vtype=value.type.element_type, value=val), None)
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_127(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(indent + 2)
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_128(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val),
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_129(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(vtype=None, value=val), indent + 2)
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_130(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=None), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_131(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(value=val), indent + 2)
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_132(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(
                        vtype=value.type.element_type,
                    ),
                    indent + 2,
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_133(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent - 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_134(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 3
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_135(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i <= len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_136(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) + 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_137(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 2:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_138(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s = ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_139(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s -= ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_140(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += "XX,\nXX"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_141(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s = "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_142(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s -= "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_143(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "XX\nXX"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_144(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s = " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_145(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s -= " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_146(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent - "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_147(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " / indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_148(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += "XX XX" * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_149(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "XX}XX"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_150(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = None
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_151(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "XX[\nXX"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_152(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = None
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_153(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(None, value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_154(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], None)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_155(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_156(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(
            list[Any],
        )
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_157(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(None):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_158(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s = " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_159(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s -= " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_160(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " / (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_161(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += "XX XX" * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_162(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent - 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_163(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 3)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_164(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s = _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_165(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s -= _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_166(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(None, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_167(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, None)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_168(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_169(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(
                    item,
                )
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_170(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent - 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_171(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 3)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_172(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s = _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_173(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s -= _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_174(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(None, indent + 2)
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_175(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(vtype=value.type.element_types[i], value=item), None)
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_176(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(indent + 2)
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_177(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item),
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_178(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(vtype=None, value=item), indent + 2)
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_179(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=None), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_180(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(CtyValue(value=item), indent + 2)
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_181(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(
                        vtype=value.type.element_types[i],
                    ),
                    indent + 2,
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_182(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent - 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_183(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 3
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_184(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i <= len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_185(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) + 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_186(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 2:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_187(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s = ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_188(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s -= ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_189(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += "XX,\nXX"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_190(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s = "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_191(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s -= "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_192(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "XX\nXX"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_193(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s = " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_194(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s -= " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_195(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent - "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_196(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " / indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_197(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += "XX XX" * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_198(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "XX]XX"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_199(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(None)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_200(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).upper()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_201(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(None).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_202(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(None)
    else:
        return str(value.value)


def x__pretty_print_cty_recursive__mutmut_203(value: CtyValue[Any], indent: int) -> str:  # noqa: C901
    """Recursive helper for pretty printing CtyValue objects.

    Args:
        value: CTY value to format
        indent: Current indentation level

    Returns:
        Formatted string representation
    """
    if isinstance(value.type, CtyObject):
        s = "{\n"
        obj_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(obj_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.attribute_types[key], value=val), indent + 2
                )
            if i < len(obj_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyList):
        s = "[\n"
        list_value = cast(list[Any], value.value)
        for i, item in enumerate(list_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=item), indent + 2
                )
            if i < len(list_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyMap):
        s = "{\n"
        map_value = cast(dict[str, Any], value.value)
        for i, (key, val) in enumerate(map_value.items()):
            s += " " * (indent + 2) + f'"{key}": '
            # Check if val is already a CtyValue or needs to be wrapped
            if isinstance(val, CtyValue):
                s += _pretty_print_cty_recursive(val, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_type, value=val), indent + 2
                )
            if i < len(map_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "}"
        return s

    elif isinstance(value.type, CtyTuple):
        s = "[\n"
        tuple_value = cast(list[Any], value.value)
        for i, item in enumerate(tuple_value):
            s += " " * (indent + 2)
            # Check if item is already a CtyValue or needs to be wrapped
            if isinstance(item, CtyValue):
                s += _pretty_print_cty_recursive(item, indent + 2)
            else:
                s += _pretty_print_cty_recursive(
                    CtyValue(vtype=value.type.element_types[i], value=item), indent + 2
                )
            if i < len(tuple_value) - 1:
                s += ",\n"
            else:
                s += "\n"
        s += " " * indent + "]"
        return s

    elif isinstance(value.type, CtyString):
        return f'"{value.value}"'
    elif isinstance(value.type, CtyNumber):
        return str(value.value)
    elif isinstance(value.type, CtyBool):
        return str(value.value).lower()
    elif isinstance(value.type, CtyDynamic):
        return str(value.value)
    else:
        return str(None)


x__pretty_print_cty_recursive__mutmut_mutants: ClassVar[MutantDict] = {
    "x__pretty_print_cty_recursive__mutmut_1": x__pretty_print_cty_recursive__mutmut_1,
    "x__pretty_print_cty_recursive__mutmut_2": x__pretty_print_cty_recursive__mutmut_2,
    "x__pretty_print_cty_recursive__mutmut_3": x__pretty_print_cty_recursive__mutmut_3,
    "x__pretty_print_cty_recursive__mutmut_4": x__pretty_print_cty_recursive__mutmut_4,
    "x__pretty_print_cty_recursive__mutmut_5": x__pretty_print_cty_recursive__mutmut_5,
    "x__pretty_print_cty_recursive__mutmut_6": x__pretty_print_cty_recursive__mutmut_6,
    "x__pretty_print_cty_recursive__mutmut_7": x__pretty_print_cty_recursive__mutmut_7,
    "x__pretty_print_cty_recursive__mutmut_8": x__pretty_print_cty_recursive__mutmut_8,
    "x__pretty_print_cty_recursive__mutmut_9": x__pretty_print_cty_recursive__mutmut_9,
    "x__pretty_print_cty_recursive__mutmut_10": x__pretty_print_cty_recursive__mutmut_10,
    "x__pretty_print_cty_recursive__mutmut_11": x__pretty_print_cty_recursive__mutmut_11,
    "x__pretty_print_cty_recursive__mutmut_12": x__pretty_print_cty_recursive__mutmut_12,
    "x__pretty_print_cty_recursive__mutmut_13": x__pretty_print_cty_recursive__mutmut_13,
    "x__pretty_print_cty_recursive__mutmut_14": x__pretty_print_cty_recursive__mutmut_14,
    "x__pretty_print_cty_recursive__mutmut_15": x__pretty_print_cty_recursive__mutmut_15,
    "x__pretty_print_cty_recursive__mutmut_16": x__pretty_print_cty_recursive__mutmut_16,
    "x__pretty_print_cty_recursive__mutmut_17": x__pretty_print_cty_recursive__mutmut_17,
    "x__pretty_print_cty_recursive__mutmut_18": x__pretty_print_cty_recursive__mutmut_18,
    "x__pretty_print_cty_recursive__mutmut_19": x__pretty_print_cty_recursive__mutmut_19,
    "x__pretty_print_cty_recursive__mutmut_20": x__pretty_print_cty_recursive__mutmut_20,
    "x__pretty_print_cty_recursive__mutmut_21": x__pretty_print_cty_recursive__mutmut_21,
    "x__pretty_print_cty_recursive__mutmut_22": x__pretty_print_cty_recursive__mutmut_22,
    "x__pretty_print_cty_recursive__mutmut_23": x__pretty_print_cty_recursive__mutmut_23,
    "x__pretty_print_cty_recursive__mutmut_24": x__pretty_print_cty_recursive__mutmut_24,
    "x__pretty_print_cty_recursive__mutmut_25": x__pretty_print_cty_recursive__mutmut_25,
    "x__pretty_print_cty_recursive__mutmut_26": x__pretty_print_cty_recursive__mutmut_26,
    "x__pretty_print_cty_recursive__mutmut_27": x__pretty_print_cty_recursive__mutmut_27,
    "x__pretty_print_cty_recursive__mutmut_28": x__pretty_print_cty_recursive__mutmut_28,
    "x__pretty_print_cty_recursive__mutmut_29": x__pretty_print_cty_recursive__mutmut_29,
    "x__pretty_print_cty_recursive__mutmut_30": x__pretty_print_cty_recursive__mutmut_30,
    "x__pretty_print_cty_recursive__mutmut_31": x__pretty_print_cty_recursive__mutmut_31,
    "x__pretty_print_cty_recursive__mutmut_32": x__pretty_print_cty_recursive__mutmut_32,
    "x__pretty_print_cty_recursive__mutmut_33": x__pretty_print_cty_recursive__mutmut_33,
    "x__pretty_print_cty_recursive__mutmut_34": x__pretty_print_cty_recursive__mutmut_34,
    "x__pretty_print_cty_recursive__mutmut_35": x__pretty_print_cty_recursive__mutmut_35,
    "x__pretty_print_cty_recursive__mutmut_36": x__pretty_print_cty_recursive__mutmut_36,
    "x__pretty_print_cty_recursive__mutmut_37": x__pretty_print_cty_recursive__mutmut_37,
    "x__pretty_print_cty_recursive__mutmut_38": x__pretty_print_cty_recursive__mutmut_38,
    "x__pretty_print_cty_recursive__mutmut_39": x__pretty_print_cty_recursive__mutmut_39,
    "x__pretty_print_cty_recursive__mutmut_40": x__pretty_print_cty_recursive__mutmut_40,
    "x__pretty_print_cty_recursive__mutmut_41": x__pretty_print_cty_recursive__mutmut_41,
    "x__pretty_print_cty_recursive__mutmut_42": x__pretty_print_cty_recursive__mutmut_42,
    "x__pretty_print_cty_recursive__mutmut_43": x__pretty_print_cty_recursive__mutmut_43,
    "x__pretty_print_cty_recursive__mutmut_44": x__pretty_print_cty_recursive__mutmut_44,
    "x__pretty_print_cty_recursive__mutmut_45": x__pretty_print_cty_recursive__mutmut_45,
    "x__pretty_print_cty_recursive__mutmut_46": x__pretty_print_cty_recursive__mutmut_46,
    "x__pretty_print_cty_recursive__mutmut_47": x__pretty_print_cty_recursive__mutmut_47,
    "x__pretty_print_cty_recursive__mutmut_48": x__pretty_print_cty_recursive__mutmut_48,
    "x__pretty_print_cty_recursive__mutmut_49": x__pretty_print_cty_recursive__mutmut_49,
    "x__pretty_print_cty_recursive__mutmut_50": x__pretty_print_cty_recursive__mutmut_50,
    "x__pretty_print_cty_recursive__mutmut_51": x__pretty_print_cty_recursive__mutmut_51,
    "x__pretty_print_cty_recursive__mutmut_52": x__pretty_print_cty_recursive__mutmut_52,
    "x__pretty_print_cty_recursive__mutmut_53": x__pretty_print_cty_recursive__mutmut_53,
    "x__pretty_print_cty_recursive__mutmut_54": x__pretty_print_cty_recursive__mutmut_54,
    "x__pretty_print_cty_recursive__mutmut_55": x__pretty_print_cty_recursive__mutmut_55,
    "x__pretty_print_cty_recursive__mutmut_56": x__pretty_print_cty_recursive__mutmut_56,
    "x__pretty_print_cty_recursive__mutmut_57": x__pretty_print_cty_recursive__mutmut_57,
    "x__pretty_print_cty_recursive__mutmut_58": x__pretty_print_cty_recursive__mutmut_58,
    "x__pretty_print_cty_recursive__mutmut_59": x__pretty_print_cty_recursive__mutmut_59,
    "x__pretty_print_cty_recursive__mutmut_60": x__pretty_print_cty_recursive__mutmut_60,
    "x__pretty_print_cty_recursive__mutmut_61": x__pretty_print_cty_recursive__mutmut_61,
    "x__pretty_print_cty_recursive__mutmut_62": x__pretty_print_cty_recursive__mutmut_62,
    "x__pretty_print_cty_recursive__mutmut_63": x__pretty_print_cty_recursive__mutmut_63,
    "x__pretty_print_cty_recursive__mutmut_64": x__pretty_print_cty_recursive__mutmut_64,
    "x__pretty_print_cty_recursive__mutmut_65": x__pretty_print_cty_recursive__mutmut_65,
    "x__pretty_print_cty_recursive__mutmut_66": x__pretty_print_cty_recursive__mutmut_66,
    "x__pretty_print_cty_recursive__mutmut_67": x__pretty_print_cty_recursive__mutmut_67,
    "x__pretty_print_cty_recursive__mutmut_68": x__pretty_print_cty_recursive__mutmut_68,
    "x__pretty_print_cty_recursive__mutmut_69": x__pretty_print_cty_recursive__mutmut_69,
    "x__pretty_print_cty_recursive__mutmut_70": x__pretty_print_cty_recursive__mutmut_70,
    "x__pretty_print_cty_recursive__mutmut_71": x__pretty_print_cty_recursive__mutmut_71,
    "x__pretty_print_cty_recursive__mutmut_72": x__pretty_print_cty_recursive__mutmut_72,
    "x__pretty_print_cty_recursive__mutmut_73": x__pretty_print_cty_recursive__mutmut_73,
    "x__pretty_print_cty_recursive__mutmut_74": x__pretty_print_cty_recursive__mutmut_74,
    "x__pretty_print_cty_recursive__mutmut_75": x__pretty_print_cty_recursive__mutmut_75,
    "x__pretty_print_cty_recursive__mutmut_76": x__pretty_print_cty_recursive__mutmut_76,
    "x__pretty_print_cty_recursive__mutmut_77": x__pretty_print_cty_recursive__mutmut_77,
    "x__pretty_print_cty_recursive__mutmut_78": x__pretty_print_cty_recursive__mutmut_78,
    "x__pretty_print_cty_recursive__mutmut_79": x__pretty_print_cty_recursive__mutmut_79,
    "x__pretty_print_cty_recursive__mutmut_80": x__pretty_print_cty_recursive__mutmut_80,
    "x__pretty_print_cty_recursive__mutmut_81": x__pretty_print_cty_recursive__mutmut_81,
    "x__pretty_print_cty_recursive__mutmut_82": x__pretty_print_cty_recursive__mutmut_82,
    "x__pretty_print_cty_recursive__mutmut_83": x__pretty_print_cty_recursive__mutmut_83,
    "x__pretty_print_cty_recursive__mutmut_84": x__pretty_print_cty_recursive__mutmut_84,
    "x__pretty_print_cty_recursive__mutmut_85": x__pretty_print_cty_recursive__mutmut_85,
    "x__pretty_print_cty_recursive__mutmut_86": x__pretty_print_cty_recursive__mutmut_86,
    "x__pretty_print_cty_recursive__mutmut_87": x__pretty_print_cty_recursive__mutmut_87,
    "x__pretty_print_cty_recursive__mutmut_88": x__pretty_print_cty_recursive__mutmut_88,
    "x__pretty_print_cty_recursive__mutmut_89": x__pretty_print_cty_recursive__mutmut_89,
    "x__pretty_print_cty_recursive__mutmut_90": x__pretty_print_cty_recursive__mutmut_90,
    "x__pretty_print_cty_recursive__mutmut_91": x__pretty_print_cty_recursive__mutmut_91,
    "x__pretty_print_cty_recursive__mutmut_92": x__pretty_print_cty_recursive__mutmut_92,
    "x__pretty_print_cty_recursive__mutmut_93": x__pretty_print_cty_recursive__mutmut_93,
    "x__pretty_print_cty_recursive__mutmut_94": x__pretty_print_cty_recursive__mutmut_94,
    "x__pretty_print_cty_recursive__mutmut_95": x__pretty_print_cty_recursive__mutmut_95,
    "x__pretty_print_cty_recursive__mutmut_96": x__pretty_print_cty_recursive__mutmut_96,
    "x__pretty_print_cty_recursive__mutmut_97": x__pretty_print_cty_recursive__mutmut_97,
    "x__pretty_print_cty_recursive__mutmut_98": x__pretty_print_cty_recursive__mutmut_98,
    "x__pretty_print_cty_recursive__mutmut_99": x__pretty_print_cty_recursive__mutmut_99,
    "x__pretty_print_cty_recursive__mutmut_100": x__pretty_print_cty_recursive__mutmut_100,
    "x__pretty_print_cty_recursive__mutmut_101": x__pretty_print_cty_recursive__mutmut_101,
    "x__pretty_print_cty_recursive__mutmut_102": x__pretty_print_cty_recursive__mutmut_102,
    "x__pretty_print_cty_recursive__mutmut_103": x__pretty_print_cty_recursive__mutmut_103,
    "x__pretty_print_cty_recursive__mutmut_104": x__pretty_print_cty_recursive__mutmut_104,
    "x__pretty_print_cty_recursive__mutmut_105": x__pretty_print_cty_recursive__mutmut_105,
    "x__pretty_print_cty_recursive__mutmut_106": x__pretty_print_cty_recursive__mutmut_106,
    "x__pretty_print_cty_recursive__mutmut_107": x__pretty_print_cty_recursive__mutmut_107,
    "x__pretty_print_cty_recursive__mutmut_108": x__pretty_print_cty_recursive__mutmut_108,
    "x__pretty_print_cty_recursive__mutmut_109": x__pretty_print_cty_recursive__mutmut_109,
    "x__pretty_print_cty_recursive__mutmut_110": x__pretty_print_cty_recursive__mutmut_110,
    "x__pretty_print_cty_recursive__mutmut_111": x__pretty_print_cty_recursive__mutmut_111,
    "x__pretty_print_cty_recursive__mutmut_112": x__pretty_print_cty_recursive__mutmut_112,
    "x__pretty_print_cty_recursive__mutmut_113": x__pretty_print_cty_recursive__mutmut_113,
    "x__pretty_print_cty_recursive__mutmut_114": x__pretty_print_cty_recursive__mutmut_114,
    "x__pretty_print_cty_recursive__mutmut_115": x__pretty_print_cty_recursive__mutmut_115,
    "x__pretty_print_cty_recursive__mutmut_116": x__pretty_print_cty_recursive__mutmut_116,
    "x__pretty_print_cty_recursive__mutmut_117": x__pretty_print_cty_recursive__mutmut_117,
    "x__pretty_print_cty_recursive__mutmut_118": x__pretty_print_cty_recursive__mutmut_118,
    "x__pretty_print_cty_recursive__mutmut_119": x__pretty_print_cty_recursive__mutmut_119,
    "x__pretty_print_cty_recursive__mutmut_120": x__pretty_print_cty_recursive__mutmut_120,
    "x__pretty_print_cty_recursive__mutmut_121": x__pretty_print_cty_recursive__mutmut_121,
    "x__pretty_print_cty_recursive__mutmut_122": x__pretty_print_cty_recursive__mutmut_122,
    "x__pretty_print_cty_recursive__mutmut_123": x__pretty_print_cty_recursive__mutmut_123,
    "x__pretty_print_cty_recursive__mutmut_124": x__pretty_print_cty_recursive__mutmut_124,
    "x__pretty_print_cty_recursive__mutmut_125": x__pretty_print_cty_recursive__mutmut_125,
    "x__pretty_print_cty_recursive__mutmut_126": x__pretty_print_cty_recursive__mutmut_126,
    "x__pretty_print_cty_recursive__mutmut_127": x__pretty_print_cty_recursive__mutmut_127,
    "x__pretty_print_cty_recursive__mutmut_128": x__pretty_print_cty_recursive__mutmut_128,
    "x__pretty_print_cty_recursive__mutmut_129": x__pretty_print_cty_recursive__mutmut_129,
    "x__pretty_print_cty_recursive__mutmut_130": x__pretty_print_cty_recursive__mutmut_130,
    "x__pretty_print_cty_recursive__mutmut_131": x__pretty_print_cty_recursive__mutmut_131,
    "x__pretty_print_cty_recursive__mutmut_132": x__pretty_print_cty_recursive__mutmut_132,
    "x__pretty_print_cty_recursive__mutmut_133": x__pretty_print_cty_recursive__mutmut_133,
    "x__pretty_print_cty_recursive__mutmut_134": x__pretty_print_cty_recursive__mutmut_134,
    "x__pretty_print_cty_recursive__mutmut_135": x__pretty_print_cty_recursive__mutmut_135,
    "x__pretty_print_cty_recursive__mutmut_136": x__pretty_print_cty_recursive__mutmut_136,
    "x__pretty_print_cty_recursive__mutmut_137": x__pretty_print_cty_recursive__mutmut_137,
    "x__pretty_print_cty_recursive__mutmut_138": x__pretty_print_cty_recursive__mutmut_138,
    "x__pretty_print_cty_recursive__mutmut_139": x__pretty_print_cty_recursive__mutmut_139,
    "x__pretty_print_cty_recursive__mutmut_140": x__pretty_print_cty_recursive__mutmut_140,
    "x__pretty_print_cty_recursive__mutmut_141": x__pretty_print_cty_recursive__mutmut_141,
    "x__pretty_print_cty_recursive__mutmut_142": x__pretty_print_cty_recursive__mutmut_142,
    "x__pretty_print_cty_recursive__mutmut_143": x__pretty_print_cty_recursive__mutmut_143,
    "x__pretty_print_cty_recursive__mutmut_144": x__pretty_print_cty_recursive__mutmut_144,
    "x__pretty_print_cty_recursive__mutmut_145": x__pretty_print_cty_recursive__mutmut_145,
    "x__pretty_print_cty_recursive__mutmut_146": x__pretty_print_cty_recursive__mutmut_146,
    "x__pretty_print_cty_recursive__mutmut_147": x__pretty_print_cty_recursive__mutmut_147,
    "x__pretty_print_cty_recursive__mutmut_148": x__pretty_print_cty_recursive__mutmut_148,
    "x__pretty_print_cty_recursive__mutmut_149": x__pretty_print_cty_recursive__mutmut_149,
    "x__pretty_print_cty_recursive__mutmut_150": x__pretty_print_cty_recursive__mutmut_150,
    "x__pretty_print_cty_recursive__mutmut_151": x__pretty_print_cty_recursive__mutmut_151,
    "x__pretty_print_cty_recursive__mutmut_152": x__pretty_print_cty_recursive__mutmut_152,
    "x__pretty_print_cty_recursive__mutmut_153": x__pretty_print_cty_recursive__mutmut_153,
    "x__pretty_print_cty_recursive__mutmut_154": x__pretty_print_cty_recursive__mutmut_154,
    "x__pretty_print_cty_recursive__mutmut_155": x__pretty_print_cty_recursive__mutmut_155,
    "x__pretty_print_cty_recursive__mutmut_156": x__pretty_print_cty_recursive__mutmut_156,
    "x__pretty_print_cty_recursive__mutmut_157": x__pretty_print_cty_recursive__mutmut_157,
    "x__pretty_print_cty_recursive__mutmut_158": x__pretty_print_cty_recursive__mutmut_158,
    "x__pretty_print_cty_recursive__mutmut_159": x__pretty_print_cty_recursive__mutmut_159,
    "x__pretty_print_cty_recursive__mutmut_160": x__pretty_print_cty_recursive__mutmut_160,
    "x__pretty_print_cty_recursive__mutmut_161": x__pretty_print_cty_recursive__mutmut_161,
    "x__pretty_print_cty_recursive__mutmut_162": x__pretty_print_cty_recursive__mutmut_162,
    "x__pretty_print_cty_recursive__mutmut_163": x__pretty_print_cty_recursive__mutmut_163,
    "x__pretty_print_cty_recursive__mutmut_164": x__pretty_print_cty_recursive__mutmut_164,
    "x__pretty_print_cty_recursive__mutmut_165": x__pretty_print_cty_recursive__mutmut_165,
    "x__pretty_print_cty_recursive__mutmut_166": x__pretty_print_cty_recursive__mutmut_166,
    "x__pretty_print_cty_recursive__mutmut_167": x__pretty_print_cty_recursive__mutmut_167,
    "x__pretty_print_cty_recursive__mutmut_168": x__pretty_print_cty_recursive__mutmut_168,
    "x__pretty_print_cty_recursive__mutmut_169": x__pretty_print_cty_recursive__mutmut_169,
    "x__pretty_print_cty_recursive__mutmut_170": x__pretty_print_cty_recursive__mutmut_170,
    "x__pretty_print_cty_recursive__mutmut_171": x__pretty_print_cty_recursive__mutmut_171,
    "x__pretty_print_cty_recursive__mutmut_172": x__pretty_print_cty_recursive__mutmut_172,
    "x__pretty_print_cty_recursive__mutmut_173": x__pretty_print_cty_recursive__mutmut_173,
    "x__pretty_print_cty_recursive__mutmut_174": x__pretty_print_cty_recursive__mutmut_174,
    "x__pretty_print_cty_recursive__mutmut_175": x__pretty_print_cty_recursive__mutmut_175,
    "x__pretty_print_cty_recursive__mutmut_176": x__pretty_print_cty_recursive__mutmut_176,
    "x__pretty_print_cty_recursive__mutmut_177": x__pretty_print_cty_recursive__mutmut_177,
    "x__pretty_print_cty_recursive__mutmut_178": x__pretty_print_cty_recursive__mutmut_178,
    "x__pretty_print_cty_recursive__mutmut_179": x__pretty_print_cty_recursive__mutmut_179,
    "x__pretty_print_cty_recursive__mutmut_180": x__pretty_print_cty_recursive__mutmut_180,
    "x__pretty_print_cty_recursive__mutmut_181": x__pretty_print_cty_recursive__mutmut_181,
    "x__pretty_print_cty_recursive__mutmut_182": x__pretty_print_cty_recursive__mutmut_182,
    "x__pretty_print_cty_recursive__mutmut_183": x__pretty_print_cty_recursive__mutmut_183,
    "x__pretty_print_cty_recursive__mutmut_184": x__pretty_print_cty_recursive__mutmut_184,
    "x__pretty_print_cty_recursive__mutmut_185": x__pretty_print_cty_recursive__mutmut_185,
    "x__pretty_print_cty_recursive__mutmut_186": x__pretty_print_cty_recursive__mutmut_186,
    "x__pretty_print_cty_recursive__mutmut_187": x__pretty_print_cty_recursive__mutmut_187,
    "x__pretty_print_cty_recursive__mutmut_188": x__pretty_print_cty_recursive__mutmut_188,
    "x__pretty_print_cty_recursive__mutmut_189": x__pretty_print_cty_recursive__mutmut_189,
    "x__pretty_print_cty_recursive__mutmut_190": x__pretty_print_cty_recursive__mutmut_190,
    "x__pretty_print_cty_recursive__mutmut_191": x__pretty_print_cty_recursive__mutmut_191,
    "x__pretty_print_cty_recursive__mutmut_192": x__pretty_print_cty_recursive__mutmut_192,
    "x__pretty_print_cty_recursive__mutmut_193": x__pretty_print_cty_recursive__mutmut_193,
    "x__pretty_print_cty_recursive__mutmut_194": x__pretty_print_cty_recursive__mutmut_194,
    "x__pretty_print_cty_recursive__mutmut_195": x__pretty_print_cty_recursive__mutmut_195,
    "x__pretty_print_cty_recursive__mutmut_196": x__pretty_print_cty_recursive__mutmut_196,
    "x__pretty_print_cty_recursive__mutmut_197": x__pretty_print_cty_recursive__mutmut_197,
    "x__pretty_print_cty_recursive__mutmut_198": x__pretty_print_cty_recursive__mutmut_198,
    "x__pretty_print_cty_recursive__mutmut_199": x__pretty_print_cty_recursive__mutmut_199,
    "x__pretty_print_cty_recursive__mutmut_200": x__pretty_print_cty_recursive__mutmut_200,
    "x__pretty_print_cty_recursive__mutmut_201": x__pretty_print_cty_recursive__mutmut_201,
    "x__pretty_print_cty_recursive__mutmut_202": x__pretty_print_cty_recursive__mutmut_202,
    "x__pretty_print_cty_recursive__mutmut_203": x__pretty_print_cty_recursive__mutmut_203,
}


def _pretty_print_cty_recursive(*args, **kwargs):
    result = _mutmut_trampoline(
        x__pretty_print_cty_recursive__mutmut_orig, x__pretty_print_cty_recursive__mutmut_mutants, args, kwargs
    )
    return result


_pretty_print_cty_recursive.__signature__ = _mutmut_signature(x__pretty_print_cty_recursive__mutmut_orig)
x__pretty_print_cty_recursive__mutmut_orig.__name__ = "x__pretty_print_cty_recursive"


def x_pretty_print_cty__mutmut_orig(value: CtyValue[Any]) -> None:
    """Pretty print a CTY value to stdout.

    Args:
        value: CTY value to print

    Example:
        >>> from pyvider.cty import CtyString
        >>> val = CtyString().validate("test")
        >>> pretty_print_cty(val)
        "test"
    """
    print(_pretty_print_cty_recursive(value, 0))


def x_pretty_print_cty__mutmut_1(value: CtyValue[Any]) -> None:
    """Pretty print a CTY value to stdout.

    Args:
        value: CTY value to print

    Example:
        >>> from pyvider.cty import CtyString
        >>> val = CtyString().validate("test")
        >>> pretty_print_cty(val)
        "test"
    """
    print(None)


def x_pretty_print_cty__mutmut_2(value: CtyValue[Any]) -> None:
    """Pretty print a CTY value to stdout.

    Args:
        value: CTY value to print

    Example:
        >>> from pyvider.cty import CtyString
        >>> val = CtyString().validate("test")
        >>> pretty_print_cty(val)
        "test"
    """
    print(_pretty_print_cty_recursive(None, 0))


def x_pretty_print_cty__mutmut_3(value: CtyValue[Any]) -> None:
    """Pretty print a CTY value to stdout.

    Args:
        value: CTY value to print

    Example:
        >>> from pyvider.cty import CtyString
        >>> val = CtyString().validate("test")
        >>> pretty_print_cty(val)
        "test"
    """
    print(_pretty_print_cty_recursive(value, None))


def x_pretty_print_cty__mutmut_4(value: CtyValue[Any]) -> None:
    """Pretty print a CTY value to stdout.

    Args:
        value: CTY value to print

    Example:
        >>> from pyvider.cty import CtyString
        >>> val = CtyString().validate("test")
        >>> pretty_print_cty(val)
        "test"
    """
    print(_pretty_print_cty_recursive(0))


def x_pretty_print_cty__mutmut_5(value: CtyValue[Any]) -> None:
    """Pretty print a CTY value to stdout.

    Args:
        value: CTY value to print

    Example:
        >>> from pyvider.cty import CtyString
        >>> val = CtyString().validate("test")
        >>> pretty_print_cty(val)
        "test"
    """
    print(
        _pretty_print_cty_recursive(
            value,
        )
    )


def x_pretty_print_cty__mutmut_6(value: CtyValue[Any]) -> None:
    """Pretty print a CTY value to stdout.

    Args:
        value: CTY value to print

    Example:
        >>> from pyvider.cty import CtyString
        >>> val = CtyString().validate("test")
        >>> pretty_print_cty(val)
        "test"
    """
    print(_pretty_print_cty_recursive(value, 1))


x_pretty_print_cty__mutmut_mutants: ClassVar[MutantDict] = {
    "x_pretty_print_cty__mutmut_1": x_pretty_print_cty__mutmut_1,
    "x_pretty_print_cty__mutmut_2": x_pretty_print_cty__mutmut_2,
    "x_pretty_print_cty__mutmut_3": x_pretty_print_cty__mutmut_3,
    "x_pretty_print_cty__mutmut_4": x_pretty_print_cty__mutmut_4,
    "x_pretty_print_cty__mutmut_5": x_pretty_print_cty__mutmut_5,
    "x_pretty_print_cty__mutmut_6": x_pretty_print_cty__mutmut_6,
}


def pretty_print_cty(*args, **kwargs):
    result = _mutmut_trampoline(
        x_pretty_print_cty__mutmut_orig, x_pretty_print_cty__mutmut_mutants, args, kwargs
    )
    return result


pretty_print_cty.__signature__ = _mutmut_signature(x_pretty_print_cty__mutmut_orig)
x_pretty_print_cty__mutmut_orig.__name__ = "x_pretty_print_cty"

# 📄⚙️🔚
