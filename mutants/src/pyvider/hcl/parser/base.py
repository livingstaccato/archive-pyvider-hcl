#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Core HCL parsing functionality with CTY integration."""

from __future__ import annotations

from collections.abc import Callable
from inspect import signature as _mutmut_signature
from typing import Annotated, Any, ClassVar

import hcl2
from provide.foundation import logger

from pyvider.cty import CtyType, CtyValue
from pyvider.cty.exceptions import CtyError as CtySchemaError, CtyValidationError
from pyvider.hcl.exceptions import HclParsingError
from pyvider.hcl.parser.inference import auto_infer_cty_type

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


def x_parse_hcl_to_cty__mutmut_orig(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_1(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """
    logger.debug(None, schema_provided=bool(schema))

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_2(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_3(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """
    logger.debug(schema_provided=bool(schema))

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_4(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_5(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_6(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_7(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_8(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_9(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = None  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_10(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(None)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_11(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(None, error=str(e), exc_info=True)
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_12(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_13(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_14(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(error=str(e), exc_info=True)
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_15(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_16(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_17(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_18(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_19(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_20(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_21(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_22(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=None) from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_23(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        logger.debug(None, schema=str(schema))
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_24(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_25(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        logger.debug(schema=str(schema))
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_26(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_27(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_28(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_29(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_30(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_31(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = None
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_32(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(None)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_33(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            logger.debug(None)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_34(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_35(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_36(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_37(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            logger.error(None, error=str(e), exc_info=True)
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_38(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_39(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_40(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            logger.error(error=str(e), exc_info=True)
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_41(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_42(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_43(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_44(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_45(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_46(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_47(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_48(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=None) from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_49(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        logger.debug(None)
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_50(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_51(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_52(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_53(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = None
        return inferred_value


def x_parse_hcl_to_cty__mutmut_54(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(None)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_55(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        logger.debug(None)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_56(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_57(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


def x_parse_hcl_to_cty__mutmut_58(hcl_content: str, schema: CtyType[Any] | None = None) -> CtyValue[Any]:
    """Parse HCL directly into validated CtyValues using pyvider.cty types.

    Args:
        hcl_content: HCL string to parse
        schema: Optional CTY type schema for validation

    Returns:
        Parsed and validated CTY value

    Raises:
        HclParsingError: If parsing or validation fails

    Example:
        >>> hcl = 'name = "example"'
        >>> result = parse_hcl_to_cty(hcl)
        >>> result.value["name"].value
        'example'
    """

    try:
        raw_data = hcl2.loads(hcl_content)  # type: ignore[attr-defined]
    except Exception as e:
        raise HclParsingError(message=f"Failed to parse HCL: {e}") from e

    if schema:
        try:
            validated_value = schema.validate(raw_data)
            return validated_value
        except (CtySchemaError, CtyValidationError) as e:
            raise HclParsingError(message=f"Schema validation failed after HCL parsing: {e}") from e
    else:
        inferred_value = auto_infer_cty_type(raw_data)
        return inferred_value


x_parse_hcl_to_cty__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_hcl_to_cty__mutmut_1": x_parse_hcl_to_cty__mutmut_1,
    "x_parse_hcl_to_cty__mutmut_2": x_parse_hcl_to_cty__mutmut_2,
    "x_parse_hcl_to_cty__mutmut_3": x_parse_hcl_to_cty__mutmut_3,
    "x_parse_hcl_to_cty__mutmut_4": x_parse_hcl_to_cty__mutmut_4,
    "x_parse_hcl_to_cty__mutmut_5": x_parse_hcl_to_cty__mutmut_5,
    "x_parse_hcl_to_cty__mutmut_6": x_parse_hcl_to_cty__mutmut_6,
    "x_parse_hcl_to_cty__mutmut_7": x_parse_hcl_to_cty__mutmut_7,
    "x_parse_hcl_to_cty__mutmut_8": x_parse_hcl_to_cty__mutmut_8,
    "x_parse_hcl_to_cty__mutmut_9": x_parse_hcl_to_cty__mutmut_9,
    "x_parse_hcl_to_cty__mutmut_10": x_parse_hcl_to_cty__mutmut_10,
    "x_parse_hcl_to_cty__mutmut_11": x_parse_hcl_to_cty__mutmut_11,
    "x_parse_hcl_to_cty__mutmut_12": x_parse_hcl_to_cty__mutmut_12,
    "x_parse_hcl_to_cty__mutmut_13": x_parse_hcl_to_cty__mutmut_13,
    "x_parse_hcl_to_cty__mutmut_14": x_parse_hcl_to_cty__mutmut_14,
    "x_parse_hcl_to_cty__mutmut_15": x_parse_hcl_to_cty__mutmut_15,
    "x_parse_hcl_to_cty__mutmut_16": x_parse_hcl_to_cty__mutmut_16,
    "x_parse_hcl_to_cty__mutmut_17": x_parse_hcl_to_cty__mutmut_17,
    "x_parse_hcl_to_cty__mutmut_18": x_parse_hcl_to_cty__mutmut_18,
    "x_parse_hcl_to_cty__mutmut_19": x_parse_hcl_to_cty__mutmut_19,
    "x_parse_hcl_to_cty__mutmut_20": x_parse_hcl_to_cty__mutmut_20,
    "x_parse_hcl_to_cty__mutmut_21": x_parse_hcl_to_cty__mutmut_21,
    "x_parse_hcl_to_cty__mutmut_22": x_parse_hcl_to_cty__mutmut_22,
    "x_parse_hcl_to_cty__mutmut_23": x_parse_hcl_to_cty__mutmut_23,
    "x_parse_hcl_to_cty__mutmut_24": x_parse_hcl_to_cty__mutmut_24,
    "x_parse_hcl_to_cty__mutmut_25": x_parse_hcl_to_cty__mutmut_25,
    "x_parse_hcl_to_cty__mutmut_26": x_parse_hcl_to_cty__mutmut_26,
    "x_parse_hcl_to_cty__mutmut_27": x_parse_hcl_to_cty__mutmut_27,
    "x_parse_hcl_to_cty__mutmut_28": x_parse_hcl_to_cty__mutmut_28,
    "x_parse_hcl_to_cty__mutmut_29": x_parse_hcl_to_cty__mutmut_29,
    "x_parse_hcl_to_cty__mutmut_30": x_parse_hcl_to_cty__mutmut_30,
    "x_parse_hcl_to_cty__mutmut_31": x_parse_hcl_to_cty__mutmut_31,
    "x_parse_hcl_to_cty__mutmut_32": x_parse_hcl_to_cty__mutmut_32,
    "x_parse_hcl_to_cty__mutmut_33": x_parse_hcl_to_cty__mutmut_33,
    "x_parse_hcl_to_cty__mutmut_34": x_parse_hcl_to_cty__mutmut_34,
    "x_parse_hcl_to_cty__mutmut_35": x_parse_hcl_to_cty__mutmut_35,
    "x_parse_hcl_to_cty__mutmut_36": x_parse_hcl_to_cty__mutmut_36,
    "x_parse_hcl_to_cty__mutmut_37": x_parse_hcl_to_cty__mutmut_37,
    "x_parse_hcl_to_cty__mutmut_38": x_parse_hcl_to_cty__mutmut_38,
    "x_parse_hcl_to_cty__mutmut_39": x_parse_hcl_to_cty__mutmut_39,
    "x_parse_hcl_to_cty__mutmut_40": x_parse_hcl_to_cty__mutmut_40,
    "x_parse_hcl_to_cty__mutmut_41": x_parse_hcl_to_cty__mutmut_41,
    "x_parse_hcl_to_cty__mutmut_42": x_parse_hcl_to_cty__mutmut_42,
    "x_parse_hcl_to_cty__mutmut_43": x_parse_hcl_to_cty__mutmut_43,
    "x_parse_hcl_to_cty__mutmut_44": x_parse_hcl_to_cty__mutmut_44,
    "x_parse_hcl_to_cty__mutmut_45": x_parse_hcl_to_cty__mutmut_45,
    "x_parse_hcl_to_cty__mutmut_46": x_parse_hcl_to_cty__mutmut_46,
    "x_parse_hcl_to_cty__mutmut_47": x_parse_hcl_to_cty__mutmut_47,
    "x_parse_hcl_to_cty__mutmut_48": x_parse_hcl_to_cty__mutmut_48,
    "x_parse_hcl_to_cty__mutmut_49": x_parse_hcl_to_cty__mutmut_49,
    "x_parse_hcl_to_cty__mutmut_50": x_parse_hcl_to_cty__mutmut_50,
    "x_parse_hcl_to_cty__mutmut_51": x_parse_hcl_to_cty__mutmut_51,
    "x_parse_hcl_to_cty__mutmut_52": x_parse_hcl_to_cty__mutmut_52,
    "x_parse_hcl_to_cty__mutmut_53": x_parse_hcl_to_cty__mutmut_53,
    "x_parse_hcl_to_cty__mutmut_54": x_parse_hcl_to_cty__mutmut_54,
    "x_parse_hcl_to_cty__mutmut_55": x_parse_hcl_to_cty__mutmut_55,
    "x_parse_hcl_to_cty__mutmut_56": x_parse_hcl_to_cty__mutmut_56,
    "x_parse_hcl_to_cty__mutmut_57": x_parse_hcl_to_cty__mutmut_57,
    "x_parse_hcl_to_cty__mutmut_58": x_parse_hcl_to_cty__mutmut_58,
}


def parse_hcl_to_cty(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_hcl_to_cty__mutmut_orig, x_parse_hcl_to_cty__mutmut_mutants, args, kwargs
    )
    return result


parse_hcl_to_cty.__signature__ = _mutmut_signature(x_parse_hcl_to_cty__mutmut_orig)
x_parse_hcl_to_cty__mutmut_orig.__name__ = "x_parse_hcl_to_cty"

# 📄⚙️🔚
