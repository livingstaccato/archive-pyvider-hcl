#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""HCL type string parsing for Terraform type syntax."""

from __future__ import annotations

from collections.abc import Callable
from inspect import signature as _mutmut_signature
import re
from typing import Annotated, Any, ClassVar

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyMap, CtyNumber, CtyObject, CtyString, CtyType

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


class HclTypeParsingError(ValueError):
    """Custom exception for errors during HCL type string parsing."""


PRIMITIVE_TYPE_MAP: dict[str, CtyType[Any]] = {
    "string": CtyString(),
    "number": CtyNumber(),
    "bool": CtyBool(),
    "any": CtyDynamic(),
}

COMPLEX_TYPE_REGEX = re.compile(r"^(list|object|map)\((.*)\)$", re.IGNORECASE | re.DOTALL)


def x_parse_hcl_type_string__mutmut_orig(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_1(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = None

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_2(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.upper() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_3(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() not in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_4(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.upper()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_5(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = None
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_6(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(None)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_7(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_8(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(None)

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_9(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = None
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_10(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).upper()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_11(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(None).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_12(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(2).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_13(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = None

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_14(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(None).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_15(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(3).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_16(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword != "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_17(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "XXlistXX":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_18(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "LIST":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_19(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_20(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError(None)
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_21(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("XXList type string is empty, e.g., 'list()'XX")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_22(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("list type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_23(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("LIST TYPE STRING IS EMPTY, E.G., 'LIST()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_24(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = None
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_25(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(None)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_26(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=None)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_27(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword != "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_28(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "XXmapXX":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_29(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "MAP":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_30(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_31(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError(None)
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_32(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("XXMap type string is empty, e.g., 'map()'XX")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_33(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_34(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("MAP TYPE STRING IS EMPTY, E.G., 'MAP()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_35(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = None
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_36(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(None)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_37(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=None)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_38(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword != "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_39(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "XXobjectXX":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_40(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "OBJECT":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_41(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") and not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_42(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_43(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith(None) or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_44(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("XX{XX") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_45(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_46(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith(None):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_47(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("XX}XX"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_48(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(None)
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_49(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content != "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_50(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "XX{}XX":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_51(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject(None)

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_52(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = None
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_53(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[2:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_54(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:+1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_55(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-2].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_56(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_57(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject(None)

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_58(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = None
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_59(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(None)
        return CtyObject(attributes)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_60(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(None)

    raise HclTypeParsingError(f"Unhandled type keyword: '{type_keyword}'")


def x_parse_hcl_type_string__mutmut_61(type_str: str) -> CtyType[Any]:  # noqa: C901
    """Parse HCL type string into CTY type.

    Supports:
    - Primitives: string, number, bool, any
    - Lists: list(element_type)
    - Maps: map(element_type)
    - Objects: object({attr=type, ...})

    Args:
        type_str: HCL type string (e.g., "list(string)", "object({name=string})")

    Returns:
        Corresponding CTY type

    Raises:
        HclTypeParsingError: If type string is malformed

    Example:
        >>> parse_hcl_type_string("list(string)")
        CtyList(element_type=CtyString())
    """
    type_str = type_str.strip()

    if type_str.lower() in PRIMITIVE_TYPE_MAP:
        return PRIMITIVE_TYPE_MAP[type_str.lower()]

    match = COMPLEX_TYPE_REGEX.match(type_str)
    if not match:
        raise HclTypeParsingError(f"Unknown or malformed type string: '{type_str}'")

    type_keyword = match.group(1).lower()
    inner_content = match.group(2).strip()

    if type_keyword == "list":
        if not inner_content:
            raise HclTypeParsingError("List type string is empty, e.g., 'list()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyList(element_type=element_type)

    if type_keyword == "map":
        if not inner_content:
            raise HclTypeParsingError("Map type string is empty, e.g., 'map()'")
        element_type = parse_hcl_type_string(inner_content)
        return CtyMap(element_type=element_type)

    if type_keyword == "object":
        if not inner_content.startswith("{") or not inner_content.endswith("}"):
            raise HclTypeParsingError(
                f"Object type string content must be enclosed in {{}}, got: '{inner_content}'"
            )
        if inner_content == "{}":
            return CtyObject({})

        attrs_str = inner_content[1:-1].strip()
        if not attrs_str:
            return CtyObject({})

        attributes = _parse_object_attributes_str(attrs_str)
        return CtyObject(attributes)

    raise HclTypeParsingError(None)


x_parse_hcl_type_string__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_hcl_type_string__mutmut_1": x_parse_hcl_type_string__mutmut_1,
    "x_parse_hcl_type_string__mutmut_2": x_parse_hcl_type_string__mutmut_2,
    "x_parse_hcl_type_string__mutmut_3": x_parse_hcl_type_string__mutmut_3,
    "x_parse_hcl_type_string__mutmut_4": x_parse_hcl_type_string__mutmut_4,
    "x_parse_hcl_type_string__mutmut_5": x_parse_hcl_type_string__mutmut_5,
    "x_parse_hcl_type_string__mutmut_6": x_parse_hcl_type_string__mutmut_6,
    "x_parse_hcl_type_string__mutmut_7": x_parse_hcl_type_string__mutmut_7,
    "x_parse_hcl_type_string__mutmut_8": x_parse_hcl_type_string__mutmut_8,
    "x_parse_hcl_type_string__mutmut_9": x_parse_hcl_type_string__mutmut_9,
    "x_parse_hcl_type_string__mutmut_10": x_parse_hcl_type_string__mutmut_10,
    "x_parse_hcl_type_string__mutmut_11": x_parse_hcl_type_string__mutmut_11,
    "x_parse_hcl_type_string__mutmut_12": x_parse_hcl_type_string__mutmut_12,
    "x_parse_hcl_type_string__mutmut_13": x_parse_hcl_type_string__mutmut_13,
    "x_parse_hcl_type_string__mutmut_14": x_parse_hcl_type_string__mutmut_14,
    "x_parse_hcl_type_string__mutmut_15": x_parse_hcl_type_string__mutmut_15,
    "x_parse_hcl_type_string__mutmut_16": x_parse_hcl_type_string__mutmut_16,
    "x_parse_hcl_type_string__mutmut_17": x_parse_hcl_type_string__mutmut_17,
    "x_parse_hcl_type_string__mutmut_18": x_parse_hcl_type_string__mutmut_18,
    "x_parse_hcl_type_string__mutmut_19": x_parse_hcl_type_string__mutmut_19,
    "x_parse_hcl_type_string__mutmut_20": x_parse_hcl_type_string__mutmut_20,
    "x_parse_hcl_type_string__mutmut_21": x_parse_hcl_type_string__mutmut_21,
    "x_parse_hcl_type_string__mutmut_22": x_parse_hcl_type_string__mutmut_22,
    "x_parse_hcl_type_string__mutmut_23": x_parse_hcl_type_string__mutmut_23,
    "x_parse_hcl_type_string__mutmut_24": x_parse_hcl_type_string__mutmut_24,
    "x_parse_hcl_type_string__mutmut_25": x_parse_hcl_type_string__mutmut_25,
    "x_parse_hcl_type_string__mutmut_26": x_parse_hcl_type_string__mutmut_26,
    "x_parse_hcl_type_string__mutmut_27": x_parse_hcl_type_string__mutmut_27,
    "x_parse_hcl_type_string__mutmut_28": x_parse_hcl_type_string__mutmut_28,
    "x_parse_hcl_type_string__mutmut_29": x_parse_hcl_type_string__mutmut_29,
    "x_parse_hcl_type_string__mutmut_30": x_parse_hcl_type_string__mutmut_30,
    "x_parse_hcl_type_string__mutmut_31": x_parse_hcl_type_string__mutmut_31,
    "x_parse_hcl_type_string__mutmut_32": x_parse_hcl_type_string__mutmut_32,
    "x_parse_hcl_type_string__mutmut_33": x_parse_hcl_type_string__mutmut_33,
    "x_parse_hcl_type_string__mutmut_34": x_parse_hcl_type_string__mutmut_34,
    "x_parse_hcl_type_string__mutmut_35": x_parse_hcl_type_string__mutmut_35,
    "x_parse_hcl_type_string__mutmut_36": x_parse_hcl_type_string__mutmut_36,
    "x_parse_hcl_type_string__mutmut_37": x_parse_hcl_type_string__mutmut_37,
    "x_parse_hcl_type_string__mutmut_38": x_parse_hcl_type_string__mutmut_38,
    "x_parse_hcl_type_string__mutmut_39": x_parse_hcl_type_string__mutmut_39,
    "x_parse_hcl_type_string__mutmut_40": x_parse_hcl_type_string__mutmut_40,
    "x_parse_hcl_type_string__mutmut_41": x_parse_hcl_type_string__mutmut_41,
    "x_parse_hcl_type_string__mutmut_42": x_parse_hcl_type_string__mutmut_42,
    "x_parse_hcl_type_string__mutmut_43": x_parse_hcl_type_string__mutmut_43,
    "x_parse_hcl_type_string__mutmut_44": x_parse_hcl_type_string__mutmut_44,
    "x_parse_hcl_type_string__mutmut_45": x_parse_hcl_type_string__mutmut_45,
    "x_parse_hcl_type_string__mutmut_46": x_parse_hcl_type_string__mutmut_46,
    "x_parse_hcl_type_string__mutmut_47": x_parse_hcl_type_string__mutmut_47,
    "x_parse_hcl_type_string__mutmut_48": x_parse_hcl_type_string__mutmut_48,
    "x_parse_hcl_type_string__mutmut_49": x_parse_hcl_type_string__mutmut_49,
    "x_parse_hcl_type_string__mutmut_50": x_parse_hcl_type_string__mutmut_50,
    "x_parse_hcl_type_string__mutmut_51": x_parse_hcl_type_string__mutmut_51,
    "x_parse_hcl_type_string__mutmut_52": x_parse_hcl_type_string__mutmut_52,
    "x_parse_hcl_type_string__mutmut_53": x_parse_hcl_type_string__mutmut_53,
    "x_parse_hcl_type_string__mutmut_54": x_parse_hcl_type_string__mutmut_54,
    "x_parse_hcl_type_string__mutmut_55": x_parse_hcl_type_string__mutmut_55,
    "x_parse_hcl_type_string__mutmut_56": x_parse_hcl_type_string__mutmut_56,
    "x_parse_hcl_type_string__mutmut_57": x_parse_hcl_type_string__mutmut_57,
    "x_parse_hcl_type_string__mutmut_58": x_parse_hcl_type_string__mutmut_58,
    "x_parse_hcl_type_string__mutmut_59": x_parse_hcl_type_string__mutmut_59,
    "x_parse_hcl_type_string__mutmut_60": x_parse_hcl_type_string__mutmut_60,
    "x_parse_hcl_type_string__mutmut_61": x_parse_hcl_type_string__mutmut_61,
}


def parse_hcl_type_string(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_hcl_type_string__mutmut_orig, x_parse_hcl_type_string__mutmut_mutants, args, kwargs
    )
    return result


parse_hcl_type_string.__signature__ = _mutmut_signature(x_parse_hcl_type_string__mutmut_orig)
x_parse_hcl_type_string__mutmut_orig.__name__ = "x_parse_hcl_type_string"


def x__parse_object_attributes_str__mutmut_orig(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_1(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = None
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_2(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = None
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_3(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 1
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_4(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = None

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_5(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 1

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_6(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(None):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_7(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char not in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_8(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "XX({XX":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_9(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance = 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_10(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({" or char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_11(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 2
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_12(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char not in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_13(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in "XX)}XX":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_14(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance = 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_15(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({" or char in ")}":
            balance += 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_16(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 2
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_17(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," or balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_18(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char != "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_19(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "XX,XX" and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_20(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance != 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_21(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 1:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_22(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = None
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_23(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_24(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(None)
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_25(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = None
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_26(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(None)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_27(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = None
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_28(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(None)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_29(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = None

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_30(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i - 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_31(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 2

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_32(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = None
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_33(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = None
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_34(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(None)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_35(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = None
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_36(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(None)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_37(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(None):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_38(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith("XX,XX"):
        raise HclTypeParsingError(f"Trailing comma found in attribute string: '{attrs_str}'")

    return attributes


def x__parse_object_attributes_str__mutmut_39(attrs_str: str) -> dict[str, CtyType[Any]]:
    """Parse object attribute definitions from HCL type string."""
    attributes: dict[str, CtyType[Any]] = {}
    balance = 0
    last_break = 0

    for i, char in enumerate(attrs_str):
        if char in "({":
            balance += 1
        elif char in ")}":
            balance -= 1
        elif char == "," and balance == 0:
            part = attrs_str[last_break:i].strip()
            if not part:
                raise HclTypeParsingError(f"Empty attribute part found in '{attrs_str}'")
            name, type_str = _split_attr_part(part)
            attributes[name] = parse_hcl_type_string(type_str)
            last_break = i + 1

    last_part = attrs_str[last_break:].strip()
    if last_part:
        name, type_str = _split_attr_part(last_part)
        attributes[name] = parse_hcl_type_string(type_str)
    elif attrs_str.strip().endswith(","):
        raise HclTypeParsingError(None)

    return attributes


x__parse_object_attributes_str__mutmut_mutants: ClassVar[MutantDict] = {
    "x__parse_object_attributes_str__mutmut_1": x__parse_object_attributes_str__mutmut_1,
    "x__parse_object_attributes_str__mutmut_2": x__parse_object_attributes_str__mutmut_2,
    "x__parse_object_attributes_str__mutmut_3": x__parse_object_attributes_str__mutmut_3,
    "x__parse_object_attributes_str__mutmut_4": x__parse_object_attributes_str__mutmut_4,
    "x__parse_object_attributes_str__mutmut_5": x__parse_object_attributes_str__mutmut_5,
    "x__parse_object_attributes_str__mutmut_6": x__parse_object_attributes_str__mutmut_6,
    "x__parse_object_attributes_str__mutmut_7": x__parse_object_attributes_str__mutmut_7,
    "x__parse_object_attributes_str__mutmut_8": x__parse_object_attributes_str__mutmut_8,
    "x__parse_object_attributes_str__mutmut_9": x__parse_object_attributes_str__mutmut_9,
    "x__parse_object_attributes_str__mutmut_10": x__parse_object_attributes_str__mutmut_10,
    "x__parse_object_attributes_str__mutmut_11": x__parse_object_attributes_str__mutmut_11,
    "x__parse_object_attributes_str__mutmut_12": x__parse_object_attributes_str__mutmut_12,
    "x__parse_object_attributes_str__mutmut_13": x__parse_object_attributes_str__mutmut_13,
    "x__parse_object_attributes_str__mutmut_14": x__parse_object_attributes_str__mutmut_14,
    "x__parse_object_attributes_str__mutmut_15": x__parse_object_attributes_str__mutmut_15,
    "x__parse_object_attributes_str__mutmut_16": x__parse_object_attributes_str__mutmut_16,
    "x__parse_object_attributes_str__mutmut_17": x__parse_object_attributes_str__mutmut_17,
    "x__parse_object_attributes_str__mutmut_18": x__parse_object_attributes_str__mutmut_18,
    "x__parse_object_attributes_str__mutmut_19": x__parse_object_attributes_str__mutmut_19,
    "x__parse_object_attributes_str__mutmut_20": x__parse_object_attributes_str__mutmut_20,
    "x__parse_object_attributes_str__mutmut_21": x__parse_object_attributes_str__mutmut_21,
    "x__parse_object_attributes_str__mutmut_22": x__parse_object_attributes_str__mutmut_22,
    "x__parse_object_attributes_str__mutmut_23": x__parse_object_attributes_str__mutmut_23,
    "x__parse_object_attributes_str__mutmut_24": x__parse_object_attributes_str__mutmut_24,
    "x__parse_object_attributes_str__mutmut_25": x__parse_object_attributes_str__mutmut_25,
    "x__parse_object_attributes_str__mutmut_26": x__parse_object_attributes_str__mutmut_26,
    "x__parse_object_attributes_str__mutmut_27": x__parse_object_attributes_str__mutmut_27,
    "x__parse_object_attributes_str__mutmut_28": x__parse_object_attributes_str__mutmut_28,
    "x__parse_object_attributes_str__mutmut_29": x__parse_object_attributes_str__mutmut_29,
    "x__parse_object_attributes_str__mutmut_30": x__parse_object_attributes_str__mutmut_30,
    "x__parse_object_attributes_str__mutmut_31": x__parse_object_attributes_str__mutmut_31,
    "x__parse_object_attributes_str__mutmut_32": x__parse_object_attributes_str__mutmut_32,
    "x__parse_object_attributes_str__mutmut_33": x__parse_object_attributes_str__mutmut_33,
    "x__parse_object_attributes_str__mutmut_34": x__parse_object_attributes_str__mutmut_34,
    "x__parse_object_attributes_str__mutmut_35": x__parse_object_attributes_str__mutmut_35,
    "x__parse_object_attributes_str__mutmut_36": x__parse_object_attributes_str__mutmut_36,
    "x__parse_object_attributes_str__mutmut_37": x__parse_object_attributes_str__mutmut_37,
    "x__parse_object_attributes_str__mutmut_38": x__parse_object_attributes_str__mutmut_38,
    "x__parse_object_attributes_str__mutmut_39": x__parse_object_attributes_str__mutmut_39,
}


def _parse_object_attributes_str(*args, **kwargs):
    result = _mutmut_trampoline(
        x__parse_object_attributes_str__mutmut_orig,
        x__parse_object_attributes_str__mutmut_mutants,
        args,
        kwargs,
    )
    return result


_parse_object_attributes_str.__signature__ = _mutmut_signature(x__parse_object_attributes_str__mutmut_orig)
x__parse_object_attributes_str__mutmut_orig.__name__ = "x__parse_object_attributes_str"


def x__split_attr_part__mutmut_orig(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_1(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = None
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_2(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find(None)
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_3(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.rfind("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_4(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("XX=XX")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_5(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos != -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_6(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == +1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_7(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -2:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_8(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(None)

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_9(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = None
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_10(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = None

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_11(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos - 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_12(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 2 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_13(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name and not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_14(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if name or not type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_15(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or type_str:
        raise HclTypeParsingError(f"Invalid attribute name or type in part: '{part}'")

    return name, type_str


def x__split_attr_part__mutmut_16(part: str) -> tuple[str, str]:
    """Split 'name=type' attribute definition."""
    equal_sign_pos = part.find("=")
    if equal_sign_pos == -1:
        raise HclTypeParsingError(f"Malformed attribute part (missing '='): '{part}'")

    name = part[:equal_sign_pos].strip()
    type_str = part[equal_sign_pos + 1 :].strip()

    if not name or not type_str:
        raise HclTypeParsingError(None)

    return name, type_str


x__split_attr_part__mutmut_mutants: ClassVar[MutantDict] = {
    "x__split_attr_part__mutmut_1": x__split_attr_part__mutmut_1,
    "x__split_attr_part__mutmut_2": x__split_attr_part__mutmut_2,
    "x__split_attr_part__mutmut_3": x__split_attr_part__mutmut_3,
    "x__split_attr_part__mutmut_4": x__split_attr_part__mutmut_4,
    "x__split_attr_part__mutmut_5": x__split_attr_part__mutmut_5,
    "x__split_attr_part__mutmut_6": x__split_attr_part__mutmut_6,
    "x__split_attr_part__mutmut_7": x__split_attr_part__mutmut_7,
    "x__split_attr_part__mutmut_8": x__split_attr_part__mutmut_8,
    "x__split_attr_part__mutmut_9": x__split_attr_part__mutmut_9,
    "x__split_attr_part__mutmut_10": x__split_attr_part__mutmut_10,
    "x__split_attr_part__mutmut_11": x__split_attr_part__mutmut_11,
    "x__split_attr_part__mutmut_12": x__split_attr_part__mutmut_12,
    "x__split_attr_part__mutmut_13": x__split_attr_part__mutmut_13,
    "x__split_attr_part__mutmut_14": x__split_attr_part__mutmut_14,
    "x__split_attr_part__mutmut_15": x__split_attr_part__mutmut_15,
    "x__split_attr_part__mutmut_16": x__split_attr_part__mutmut_16,
}


def _split_attr_part(*args, **kwargs):
    result = _mutmut_trampoline(
        x__split_attr_part__mutmut_orig, x__split_attr_part__mutmut_mutants, args, kwargs
    )
    return result


_split_attr_part.__signature__ = _mutmut_signature(x__split_attr_part__mutmut_orig)
x__split_attr_part__mutmut_orig.__name__ = "x__split_attr_part"

# 📄⚙️🔚
