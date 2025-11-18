#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Automatic CTY type inference from Python data structures."""

from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal
from inspect import signature as _mutmut_signature
from typing import Annotated, Any, ClassVar

from provide.foundation import logger

from pyvider.cty import CtyBool, CtyDynamic, CtyList, CtyNumber, CtyObject, CtyString, CtyValue

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


def x__auto_infer_value_to_cty__mutmut_orig(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_1(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is not None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_2(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(None)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_3(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(None)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_4(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(None)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_5(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_6(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=None).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_7(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = None
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_8(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(None) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_9(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = None
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_10(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = None
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_11(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(None)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_12(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=None, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_13(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=None)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_14(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_15(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(
            vtype=obj_type,
        )

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_16(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        None,
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_17(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=None,
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_18(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=None,
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_19(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_20(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_21(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_22(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_23(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_24(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_25(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(None),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_26(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(None)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_27(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(None)[:100],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_28(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:101],
    )
    return CtyValue.unknown(CtyDynamic())


def x__auto_infer_value_to_cty__mutmut_29(raw_value: Any) -> CtyValue[Any]:
    """Recursively infers a Python value to its corresponding CtyValue.

    Args:
        raw_value: Python value to infer CTY type for

    Returns:
        CTY value with inferred type

    Note:
        Unknown types are returned as CtyDynamic with a warning logged.
    """
    if raw_value is None:
        return CtyDynamic().validate(None)  # type: ignore[no-any-return]
    if isinstance(raw_value, str):
        return CtyString().validate(raw_value)
    if isinstance(raw_value, bool):
        return CtyBool().validate(raw_value)
    if isinstance(raw_value, int | float | Decimal):
        return CtyNumber().validate(raw_value)
    if isinstance(raw_value, list):
        return CtyList(element_type=CtyDynamic()).validate(raw_value)  # type: ignore[no-any-return]
    if isinstance(raw_value, dict):
        inferred_attrs = {k: _auto_infer_value_to_cty(v) for k, v in raw_value.items()}
        inferred_attr_types = {k: v.type for k, v in inferred_attrs.items()}
        obj_type = CtyObject(inferred_attr_types)
        return CtyValue(vtype=obj_type, value=inferred_attrs)

    logger.warning(
        value_type=str(type(raw_value)),
        value_repr=repr(raw_value)[:100],
    )
    return CtyValue.unknown(None)


x__auto_infer_value_to_cty__mutmut_mutants: ClassVar[MutantDict] = {
    "x__auto_infer_value_to_cty__mutmut_1": x__auto_infer_value_to_cty__mutmut_1,
    "x__auto_infer_value_to_cty__mutmut_2": x__auto_infer_value_to_cty__mutmut_2,
    "x__auto_infer_value_to_cty__mutmut_3": x__auto_infer_value_to_cty__mutmut_3,
    "x__auto_infer_value_to_cty__mutmut_4": x__auto_infer_value_to_cty__mutmut_4,
    "x__auto_infer_value_to_cty__mutmut_5": x__auto_infer_value_to_cty__mutmut_5,
    "x__auto_infer_value_to_cty__mutmut_6": x__auto_infer_value_to_cty__mutmut_6,
    "x__auto_infer_value_to_cty__mutmut_7": x__auto_infer_value_to_cty__mutmut_7,
    "x__auto_infer_value_to_cty__mutmut_8": x__auto_infer_value_to_cty__mutmut_8,
    "x__auto_infer_value_to_cty__mutmut_9": x__auto_infer_value_to_cty__mutmut_9,
    "x__auto_infer_value_to_cty__mutmut_10": x__auto_infer_value_to_cty__mutmut_10,
    "x__auto_infer_value_to_cty__mutmut_11": x__auto_infer_value_to_cty__mutmut_11,
    "x__auto_infer_value_to_cty__mutmut_12": x__auto_infer_value_to_cty__mutmut_12,
    "x__auto_infer_value_to_cty__mutmut_13": x__auto_infer_value_to_cty__mutmut_13,
    "x__auto_infer_value_to_cty__mutmut_14": x__auto_infer_value_to_cty__mutmut_14,
    "x__auto_infer_value_to_cty__mutmut_15": x__auto_infer_value_to_cty__mutmut_15,
    "x__auto_infer_value_to_cty__mutmut_16": x__auto_infer_value_to_cty__mutmut_16,
    "x__auto_infer_value_to_cty__mutmut_17": x__auto_infer_value_to_cty__mutmut_17,
    "x__auto_infer_value_to_cty__mutmut_18": x__auto_infer_value_to_cty__mutmut_18,
    "x__auto_infer_value_to_cty__mutmut_19": x__auto_infer_value_to_cty__mutmut_19,
    "x__auto_infer_value_to_cty__mutmut_20": x__auto_infer_value_to_cty__mutmut_20,
    "x__auto_infer_value_to_cty__mutmut_21": x__auto_infer_value_to_cty__mutmut_21,
    "x__auto_infer_value_to_cty__mutmut_22": x__auto_infer_value_to_cty__mutmut_22,
    "x__auto_infer_value_to_cty__mutmut_23": x__auto_infer_value_to_cty__mutmut_23,
    "x__auto_infer_value_to_cty__mutmut_24": x__auto_infer_value_to_cty__mutmut_24,
    "x__auto_infer_value_to_cty__mutmut_25": x__auto_infer_value_to_cty__mutmut_25,
    "x__auto_infer_value_to_cty__mutmut_26": x__auto_infer_value_to_cty__mutmut_26,
    "x__auto_infer_value_to_cty__mutmut_27": x__auto_infer_value_to_cty__mutmut_27,
    "x__auto_infer_value_to_cty__mutmut_28": x__auto_infer_value_to_cty__mutmut_28,
    "x__auto_infer_value_to_cty__mutmut_29": x__auto_infer_value_to_cty__mutmut_29,
}


def _auto_infer_value_to_cty(*args, **kwargs):
    result = _mutmut_trampoline(
        x__auto_infer_value_to_cty__mutmut_orig, x__auto_infer_value_to_cty__mutmut_mutants, args, kwargs
    )
    return result


_auto_infer_value_to_cty.__signature__ = _mutmut_signature(x__auto_infer_value_to_cty__mutmut_orig)
x__auto_infer_value_to_cty__mutmut_orig.__name__ = "x__auto_infer_value_to_cty"


def x_auto_infer_cty_type__mutmut_orig(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_1(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    logger.debug(None, data_type=str(type(raw_data)))
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_2(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_3(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    logger.debug(data_type=str(type(raw_data)))
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_4(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_5(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_6(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_7(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_8(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_9(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(raw_data)


def x_auto_infer_cty_type__mutmut_10(raw_data: Any) -> CtyValue[Any]:
    """Automatically infer CTY type from raw Python data.

    This function takes Python data structures (typically from HCL parsing)
    and automatically infers appropriate CTY types.

    Args:
        raw_data: Python data structure to infer types for

    Returns:
        CTY value with inferred types

    Example:
        >>> data = {"name": "test", "count": 5}
        >>> result = auto_infer_cty_type(data)
        >>> isinstance(result.type, CtyObject)
        True
    """
    return _auto_infer_value_to_cty(None)


x_auto_infer_cty_type__mutmut_mutants: ClassVar[MutantDict] = {
    "x_auto_infer_cty_type__mutmut_1": x_auto_infer_cty_type__mutmut_1,
    "x_auto_infer_cty_type__mutmut_2": x_auto_infer_cty_type__mutmut_2,
    "x_auto_infer_cty_type__mutmut_3": x_auto_infer_cty_type__mutmut_3,
    "x_auto_infer_cty_type__mutmut_4": x_auto_infer_cty_type__mutmut_4,
    "x_auto_infer_cty_type__mutmut_5": x_auto_infer_cty_type__mutmut_5,
    "x_auto_infer_cty_type__mutmut_6": x_auto_infer_cty_type__mutmut_6,
    "x_auto_infer_cty_type__mutmut_7": x_auto_infer_cty_type__mutmut_7,
    "x_auto_infer_cty_type__mutmut_8": x_auto_infer_cty_type__mutmut_8,
    "x_auto_infer_cty_type__mutmut_9": x_auto_infer_cty_type__mutmut_9,
    "x_auto_infer_cty_type__mutmut_10": x_auto_infer_cty_type__mutmut_10,
}


def auto_infer_cty_type(*args, **kwargs):
    result = _mutmut_trampoline(
        x_auto_infer_cty_type__mutmut_orig, x_auto_infer_cty_type__mutmut_mutants, args, kwargs
    )
    return result


auto_infer_cty_type.__signature__ = _mutmut_signature(x_auto_infer_cty_type__mutmut_orig)
x_auto_infer_cty_type__mutmut_orig.__name__ = "x_auto_infer_cty_type"

# 📄⚙️🔚
