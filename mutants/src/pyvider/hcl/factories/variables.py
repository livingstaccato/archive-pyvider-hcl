#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Terraform variable factory functions."""

from __future__ import annotations

from collections.abc import Callable
from inspect import signature as _mutmut_signature
from typing import Annotated, Any, ClassVar

from provide.foundation import logger

from pyvider.cty import CtyBool, CtyList, CtyObject, CtyString, CtyType, CtyValue
from pyvider.cty.exceptions import CtyError, CtyValidationError
from pyvider.hcl.factories.types import HclTypeParsingError, parse_hcl_type_string

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


class HclFactoryError(ValueError):
    """Custom exception for errors during HCL factory operations."""


def x_create_variable_cty__mutmut_orig(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_1(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug(None, name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_2(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=None, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_3(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=None)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_4(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug(name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_5(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_6(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug(
        "🏭⏳ Creating variable",
        name=name,
    )

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_7(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("XX🏭⏳ Creating variableXX", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_8(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_9(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ CREATING VARIABLE", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_10(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name and not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_11(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_12(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_13(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error(None, name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_14(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=None)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_15(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error(name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_16(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error(
            "🏭❌ Invalid variable name",
        )
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_17(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("XX🏭❌ Invalid variable nameXX", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_18(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_19(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ INVALID VARIABLE NAME", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_20(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(None)

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_21(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = None
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_22(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(None)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_23(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error(None, name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_24(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=None, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_25(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=None, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_26(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=None)
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_27(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error(name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_28(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_29(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_30(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error(
            "🏭❌ Type string parsing failed",
            name=name,
            type_str=type_str,
        )
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_31(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("XX🏭❌ Type string parsing failedXX", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_32(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_33(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ TYPE STRING PARSING FAILED", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_34(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(None))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_35(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(None) from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_36(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = None

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_37(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"XXtypeXX": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_38(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"TYPE": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_39(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_40(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = None
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_41(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["XXdescriptionXX"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_42(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["DESCRIPTION"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_43(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_44(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = None
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_45(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["XXsensitiveXX"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_46(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["SENSITIVE"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_47(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_48(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = None

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_49(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["XXnullableXX"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_50(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["NULLABLE"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_51(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_52(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(None)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_53(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                None,
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_54(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=None,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_55(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=None,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_56(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=None,
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_57(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_58(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_59(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_60(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_61(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "XX🏭❌ Default value validation failedXX",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_62(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_63(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ DEFAULT VALUE VALIDATION FAILED",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_64(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(None),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_65(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(None) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_66(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = None

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_67(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["XXdefaultXX"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_68(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["DEFAULT"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_69(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = None
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_70(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"XXtypeXX": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_71(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"TYPE": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_72(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "XXdescriptionXX" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_73(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "DESCRIPTION" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_74(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" not in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_75(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = None
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_76(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["XXdescriptionXX"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_77(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["DESCRIPTION"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_78(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "XXsensitiveXX" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_79(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "SENSITIVE" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_80(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" not in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_81(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = None
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_82(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["XXsensitiveXX"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_83(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["SENSITIVE"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_84(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "XXnullableXX" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_85(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "NULLABLE" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_86(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" not in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_87(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = None
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_88(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["XXnullableXX"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_89(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["NULLABLE"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_90(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "XXdefaultXX" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_91(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "DEFAULT" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_92(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" not in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_93(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = None

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_94(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["XXdefaultXX"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_95(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["DEFAULT"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_96(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = None
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_97(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"XXvariableXX": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_98(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"VARIABLE": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_99(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = None

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_100(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(None)

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_101(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"XXvariableXX": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_102(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"VARIABLE": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_103(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject({"variable": CtyList(element_type=None)})

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_104(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject({"variable": CtyList(element_type=CtyObject(None))})

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_105(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject({"variable": CtyList(element_type=CtyObject({name: CtyObject(None)}))})

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_106(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = None
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_107(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(None)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_108(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        logger.debug(None, name=name)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_109(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_110(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        logger.debug(name=name)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_111(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_112(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_113(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_114(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_115(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error(None, name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_116(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=None, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_117(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=None)
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_118(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error(name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_119(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_120(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error(
            "🏭❌ Variable creation failed",
            name=name,
        )
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_121(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("XX🏭❌ Variable creation failedXX", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_122(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ variable creation failed", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_123(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ VARIABLE CREATION FAILED", name=name, error=str(e))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_124(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(None))
        raise HclFactoryError(f"Internal error creating variable CtyValue: {e}") from e


def x_create_variable_cty__mutmut_125(  # noqa: C901
    name: str,
    type_str: str,
    default_py: Any | None = None,
    description: str | None = None,
    sensitive: bool | None = None,
    nullable: bool | None = None,
) -> CtyValue[Any]:
    """Create a Terraform variable CTY structure.

    Args:
        name: Variable name (must be valid identifier)
        type_str: HCL type string (e.g., "string", "list(number)")
        default_py: Optional default value
        description: Optional description
        sensitive: Optional sensitive flag
        nullable: Optional nullable flag

    Returns:
        CTY value representing Terraform variable structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> var = create_variable_cty(
        ...     name="region",
        ...     type_str="string",
        ...     default_py="us-west-2"
        ... )
    """
    logger.debug("🏭⏳ Creating variable", name=name, type_str=type_str)

    if not name or not name.isidentifier():
        logger.error("🏭❌ Invalid variable name", name=name)
        raise HclFactoryError(f"Invalid variable name: '{name}'. Must be a valid identifier.")

    try:
        parsed_variable_type = parse_hcl_type_string(type_str)
    except HclTypeParsingError as e:
        logger.error("🏭❌ Type string parsing failed", name=name, type_str=type_str, error=str(e))
        raise HclFactoryError(f"Invalid type string for variable '{name}': {e}") from e

    variable_attrs_py: dict[str, Any] = {"type": type_str}

    if description is not None:
        variable_attrs_py["description"] = description
    if sensitive is not None:
        variable_attrs_py["sensitive"] = sensitive
    if nullable is not None:
        variable_attrs_py["nullable"] = nullable

    if default_py is not None:
        try:
            parsed_variable_type.validate(default_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Default value validation failed",
                name=name,
                type_str=type_str,
                error=str(e),
            )
            raise HclFactoryError(
                f"Default value for variable '{name}' is not compatible with type '{type_str}': {e}"
            ) from e
        variable_attrs_py["default"] = default_py

    variable_attrs_schema: dict[str, CtyType[Any]] = {"type": CtyString()}
    if "description" in variable_attrs_py:
        variable_attrs_schema["description"] = CtyString()
    if "sensitive" in variable_attrs_py:
        variable_attrs_schema["sensitive"] = CtyBool()
    if "nullable" in variable_attrs_py:
        variable_attrs_schema["nullable"] = CtyBool()
    if "default" in variable_attrs_py:
        variable_attrs_schema["default"] = parsed_variable_type

    root_py_struct = {"variable": [{name: variable_attrs_py}]}
    root_schema = CtyObject(
        {"variable": CtyList(element_type=CtyObject({name: CtyObject(variable_attrs_schema)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Variable creation failed", name=name, error=str(e))
        raise HclFactoryError(None) from e


x_create_variable_cty__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_variable_cty__mutmut_1": x_create_variable_cty__mutmut_1,
    "x_create_variable_cty__mutmut_2": x_create_variable_cty__mutmut_2,
    "x_create_variable_cty__mutmut_3": x_create_variable_cty__mutmut_3,
    "x_create_variable_cty__mutmut_4": x_create_variable_cty__mutmut_4,
    "x_create_variable_cty__mutmut_5": x_create_variable_cty__mutmut_5,
    "x_create_variable_cty__mutmut_6": x_create_variable_cty__mutmut_6,
    "x_create_variable_cty__mutmut_7": x_create_variable_cty__mutmut_7,
    "x_create_variable_cty__mutmut_8": x_create_variable_cty__mutmut_8,
    "x_create_variable_cty__mutmut_9": x_create_variable_cty__mutmut_9,
    "x_create_variable_cty__mutmut_10": x_create_variable_cty__mutmut_10,
    "x_create_variable_cty__mutmut_11": x_create_variable_cty__mutmut_11,
    "x_create_variable_cty__mutmut_12": x_create_variable_cty__mutmut_12,
    "x_create_variable_cty__mutmut_13": x_create_variable_cty__mutmut_13,
    "x_create_variable_cty__mutmut_14": x_create_variable_cty__mutmut_14,
    "x_create_variable_cty__mutmut_15": x_create_variable_cty__mutmut_15,
    "x_create_variable_cty__mutmut_16": x_create_variable_cty__mutmut_16,
    "x_create_variable_cty__mutmut_17": x_create_variable_cty__mutmut_17,
    "x_create_variable_cty__mutmut_18": x_create_variable_cty__mutmut_18,
    "x_create_variable_cty__mutmut_19": x_create_variable_cty__mutmut_19,
    "x_create_variable_cty__mutmut_20": x_create_variable_cty__mutmut_20,
    "x_create_variable_cty__mutmut_21": x_create_variable_cty__mutmut_21,
    "x_create_variable_cty__mutmut_22": x_create_variable_cty__mutmut_22,
    "x_create_variable_cty__mutmut_23": x_create_variable_cty__mutmut_23,
    "x_create_variable_cty__mutmut_24": x_create_variable_cty__mutmut_24,
    "x_create_variable_cty__mutmut_25": x_create_variable_cty__mutmut_25,
    "x_create_variable_cty__mutmut_26": x_create_variable_cty__mutmut_26,
    "x_create_variable_cty__mutmut_27": x_create_variable_cty__mutmut_27,
    "x_create_variable_cty__mutmut_28": x_create_variable_cty__mutmut_28,
    "x_create_variable_cty__mutmut_29": x_create_variable_cty__mutmut_29,
    "x_create_variable_cty__mutmut_30": x_create_variable_cty__mutmut_30,
    "x_create_variable_cty__mutmut_31": x_create_variable_cty__mutmut_31,
    "x_create_variable_cty__mutmut_32": x_create_variable_cty__mutmut_32,
    "x_create_variable_cty__mutmut_33": x_create_variable_cty__mutmut_33,
    "x_create_variable_cty__mutmut_34": x_create_variable_cty__mutmut_34,
    "x_create_variable_cty__mutmut_35": x_create_variable_cty__mutmut_35,
    "x_create_variable_cty__mutmut_36": x_create_variable_cty__mutmut_36,
    "x_create_variable_cty__mutmut_37": x_create_variable_cty__mutmut_37,
    "x_create_variable_cty__mutmut_38": x_create_variable_cty__mutmut_38,
    "x_create_variable_cty__mutmut_39": x_create_variable_cty__mutmut_39,
    "x_create_variable_cty__mutmut_40": x_create_variable_cty__mutmut_40,
    "x_create_variable_cty__mutmut_41": x_create_variable_cty__mutmut_41,
    "x_create_variable_cty__mutmut_42": x_create_variable_cty__mutmut_42,
    "x_create_variable_cty__mutmut_43": x_create_variable_cty__mutmut_43,
    "x_create_variable_cty__mutmut_44": x_create_variable_cty__mutmut_44,
    "x_create_variable_cty__mutmut_45": x_create_variable_cty__mutmut_45,
    "x_create_variable_cty__mutmut_46": x_create_variable_cty__mutmut_46,
    "x_create_variable_cty__mutmut_47": x_create_variable_cty__mutmut_47,
    "x_create_variable_cty__mutmut_48": x_create_variable_cty__mutmut_48,
    "x_create_variable_cty__mutmut_49": x_create_variable_cty__mutmut_49,
    "x_create_variable_cty__mutmut_50": x_create_variable_cty__mutmut_50,
    "x_create_variable_cty__mutmut_51": x_create_variable_cty__mutmut_51,
    "x_create_variable_cty__mutmut_52": x_create_variable_cty__mutmut_52,
    "x_create_variable_cty__mutmut_53": x_create_variable_cty__mutmut_53,
    "x_create_variable_cty__mutmut_54": x_create_variable_cty__mutmut_54,
    "x_create_variable_cty__mutmut_55": x_create_variable_cty__mutmut_55,
    "x_create_variable_cty__mutmut_56": x_create_variable_cty__mutmut_56,
    "x_create_variable_cty__mutmut_57": x_create_variable_cty__mutmut_57,
    "x_create_variable_cty__mutmut_58": x_create_variable_cty__mutmut_58,
    "x_create_variable_cty__mutmut_59": x_create_variable_cty__mutmut_59,
    "x_create_variable_cty__mutmut_60": x_create_variable_cty__mutmut_60,
    "x_create_variable_cty__mutmut_61": x_create_variable_cty__mutmut_61,
    "x_create_variable_cty__mutmut_62": x_create_variable_cty__mutmut_62,
    "x_create_variable_cty__mutmut_63": x_create_variable_cty__mutmut_63,
    "x_create_variable_cty__mutmut_64": x_create_variable_cty__mutmut_64,
    "x_create_variable_cty__mutmut_65": x_create_variable_cty__mutmut_65,
    "x_create_variable_cty__mutmut_66": x_create_variable_cty__mutmut_66,
    "x_create_variable_cty__mutmut_67": x_create_variable_cty__mutmut_67,
    "x_create_variable_cty__mutmut_68": x_create_variable_cty__mutmut_68,
    "x_create_variable_cty__mutmut_69": x_create_variable_cty__mutmut_69,
    "x_create_variable_cty__mutmut_70": x_create_variable_cty__mutmut_70,
    "x_create_variable_cty__mutmut_71": x_create_variable_cty__mutmut_71,
    "x_create_variable_cty__mutmut_72": x_create_variable_cty__mutmut_72,
    "x_create_variable_cty__mutmut_73": x_create_variable_cty__mutmut_73,
    "x_create_variable_cty__mutmut_74": x_create_variable_cty__mutmut_74,
    "x_create_variable_cty__mutmut_75": x_create_variable_cty__mutmut_75,
    "x_create_variable_cty__mutmut_76": x_create_variable_cty__mutmut_76,
    "x_create_variable_cty__mutmut_77": x_create_variable_cty__mutmut_77,
    "x_create_variable_cty__mutmut_78": x_create_variable_cty__mutmut_78,
    "x_create_variable_cty__mutmut_79": x_create_variable_cty__mutmut_79,
    "x_create_variable_cty__mutmut_80": x_create_variable_cty__mutmut_80,
    "x_create_variable_cty__mutmut_81": x_create_variable_cty__mutmut_81,
    "x_create_variable_cty__mutmut_82": x_create_variable_cty__mutmut_82,
    "x_create_variable_cty__mutmut_83": x_create_variable_cty__mutmut_83,
    "x_create_variable_cty__mutmut_84": x_create_variable_cty__mutmut_84,
    "x_create_variable_cty__mutmut_85": x_create_variable_cty__mutmut_85,
    "x_create_variable_cty__mutmut_86": x_create_variable_cty__mutmut_86,
    "x_create_variable_cty__mutmut_87": x_create_variable_cty__mutmut_87,
    "x_create_variable_cty__mutmut_88": x_create_variable_cty__mutmut_88,
    "x_create_variable_cty__mutmut_89": x_create_variable_cty__mutmut_89,
    "x_create_variable_cty__mutmut_90": x_create_variable_cty__mutmut_90,
    "x_create_variable_cty__mutmut_91": x_create_variable_cty__mutmut_91,
    "x_create_variable_cty__mutmut_92": x_create_variable_cty__mutmut_92,
    "x_create_variable_cty__mutmut_93": x_create_variable_cty__mutmut_93,
    "x_create_variable_cty__mutmut_94": x_create_variable_cty__mutmut_94,
    "x_create_variable_cty__mutmut_95": x_create_variable_cty__mutmut_95,
    "x_create_variable_cty__mutmut_96": x_create_variable_cty__mutmut_96,
    "x_create_variable_cty__mutmut_97": x_create_variable_cty__mutmut_97,
    "x_create_variable_cty__mutmut_98": x_create_variable_cty__mutmut_98,
    "x_create_variable_cty__mutmut_99": x_create_variable_cty__mutmut_99,
    "x_create_variable_cty__mutmut_100": x_create_variable_cty__mutmut_100,
    "x_create_variable_cty__mutmut_101": x_create_variable_cty__mutmut_101,
    "x_create_variable_cty__mutmut_102": x_create_variable_cty__mutmut_102,
    "x_create_variable_cty__mutmut_103": x_create_variable_cty__mutmut_103,
    "x_create_variable_cty__mutmut_104": x_create_variable_cty__mutmut_104,
    "x_create_variable_cty__mutmut_105": x_create_variable_cty__mutmut_105,
    "x_create_variable_cty__mutmut_106": x_create_variable_cty__mutmut_106,
    "x_create_variable_cty__mutmut_107": x_create_variable_cty__mutmut_107,
    "x_create_variable_cty__mutmut_108": x_create_variable_cty__mutmut_108,
    "x_create_variable_cty__mutmut_109": x_create_variable_cty__mutmut_109,
    "x_create_variable_cty__mutmut_110": x_create_variable_cty__mutmut_110,
    "x_create_variable_cty__mutmut_111": x_create_variable_cty__mutmut_111,
    "x_create_variable_cty__mutmut_112": x_create_variable_cty__mutmut_112,
    "x_create_variable_cty__mutmut_113": x_create_variable_cty__mutmut_113,
    "x_create_variable_cty__mutmut_114": x_create_variable_cty__mutmut_114,
    "x_create_variable_cty__mutmut_115": x_create_variable_cty__mutmut_115,
    "x_create_variable_cty__mutmut_116": x_create_variable_cty__mutmut_116,
    "x_create_variable_cty__mutmut_117": x_create_variable_cty__mutmut_117,
    "x_create_variable_cty__mutmut_118": x_create_variable_cty__mutmut_118,
    "x_create_variable_cty__mutmut_119": x_create_variable_cty__mutmut_119,
    "x_create_variable_cty__mutmut_120": x_create_variable_cty__mutmut_120,
    "x_create_variable_cty__mutmut_121": x_create_variable_cty__mutmut_121,
    "x_create_variable_cty__mutmut_122": x_create_variable_cty__mutmut_122,
    "x_create_variable_cty__mutmut_123": x_create_variable_cty__mutmut_123,
    "x_create_variable_cty__mutmut_124": x_create_variable_cty__mutmut_124,
    "x_create_variable_cty__mutmut_125": x_create_variable_cty__mutmut_125,
}


def create_variable_cty(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_variable_cty__mutmut_orig, x_create_variable_cty__mutmut_mutants, args, kwargs
    )
    return result


create_variable_cty.__signature__ = _mutmut_signature(x_create_variable_cty__mutmut_orig)
x_create_variable_cty__mutmut_orig.__name__ = "x_create_variable_cty"

# 📄⚙️🔚
