#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Terraform resource factory functions."""

from __future__ import annotations

from collections.abc import Callable
from inspect import signature as _mutmut_signature
from typing import Annotated, Any, ClassVar

from provide.foundation import logger

from pyvider.cty import CtyList, CtyObject, CtyType, CtyValue
from pyvider.cty.exceptions import CtyError, CtyValidationError
from pyvider.hcl.factories.types import HclTypeParsingError, parse_hcl_type_string
from pyvider.hcl.factories.variables import HclFactoryError
from pyvider.hcl.parser import auto_infer_cty_type

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


def x_create_resource_cty__mutmut_orig(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_1(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug(None, r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_2(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=None, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_3(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=None)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_4(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug(r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_5(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_6(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug(
        "🏭⏳ Creating resource",
        r_type=r_type,
    )

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_7(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("XX🏭⏳ Creating resourceXX", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_8(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_9(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ CREATING RESOURCE", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_10(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type and not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_11(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_12(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_13(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error(None)
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_14(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("XX🏭❌ Empty resource typeXX")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_15(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_16(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ EMPTY RESOURCE TYPE")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_17(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError(None)

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_18(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("XXResource type 'r_type' cannot be empty.XX")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_19(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_20(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("RESOURCE TYPE 'R_TYPE' CANNOT BE EMPTY.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_21(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name and not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_22(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_23(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_24(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error(None)
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_25(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("XX🏭❌ Empty resource nameXX")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_26(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_27(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ EMPTY RESOURCE NAME")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_28(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError(None)

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_29(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("XXResource name 'r_name' cannot be empty.XX")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_30(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_31(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("RESOURCE NAME 'R_NAME' CANNOT BE EMPTY.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_32(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = None

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_33(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_34(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = None
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_35(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(None)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_36(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    None,
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_37(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=None,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_38(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=None,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_39(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=None,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_40(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=None,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_41(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=None,
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_42(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_43(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_44(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_45(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_46(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_47(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_48(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "XX🏭❌ Attribute type parsing failedXX",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_49(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_50(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ ATTRIBUTE TYPE PARSING FAILED",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_51(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(None),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_52(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(None) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_53(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_54(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    None,
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_55(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=None,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_56(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=None,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_57(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=None,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_58(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_59(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_60(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_61(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_62(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "XX🏭❌ Missing type for attributeXX",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_63(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_64(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ MISSING TYPE FOR ATTRIBUTE",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_65(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(None)

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_66(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = None
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_67(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(None)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_68(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(None)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_69(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                None,
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_70(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=None,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_71(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=None,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_72(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=None,
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_73(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_74(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_75(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_76(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_77(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "XX🏭❌ Attribute validation failedXX",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_78(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_79(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ ATTRIBUTE VALIDATION FAILED",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_80(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(None),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_81(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(None) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_82(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug(None, r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_83(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=None, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_84(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=None)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_85(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug(r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_86(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_87(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug(
            "🏭⏳ Inferring attribute types",
            r_type=r_type,
        )
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_88(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("XX🏭⏳ Inferring attribute typesXX", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_89(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_90(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ INFERRING ATTRIBUTE TYPES", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_91(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = None
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_92(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(None)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_93(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = None
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_94(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error(None, r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_95(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=None, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_96(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=None)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_97(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error(r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_98(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_99(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error(
                "🏭❌ Type inference failed",
                r_type=r_type,
            )
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_100(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("XX🏭❌ Type inference failedXX", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_101(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_102(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ TYPE INFERENCE FAILED", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_103(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError(None)

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_104(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("XXCould not infer object type from attributes.XX")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_105(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_106(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("COULD NOT INFER OBJECT TYPE FROM ATTRIBUTES.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_107(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = None
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_108(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"XXresourceXX": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_109(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"RESOURCE": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_110(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = None

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_111(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(None)

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_112(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "XXresourceXX": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_113(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "RESOURCE": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_114(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject({"resource": CtyList(element_type=None)})

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_115(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject({"resource": CtyList(element_type=CtyObject(None))})

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_116(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {"resource": CtyList(element_type=CtyObject({r_type: CtyList(element_type=None)}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_117(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {"resource": CtyList(element_type=CtyObject({r_type: CtyList(element_type=CtyObject(None))}))}
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_118(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject({r_type: CtyList(element_type=CtyObject({r_name: CtyObject(None)}))})
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_119(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = None
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_120(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(None)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_121(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        logger.debug(None, r_type=r_type, r_name=r_name)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_122(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_123(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_124(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        logger.debug(r_type=r_type, r_name=r_name)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_125(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_126(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_127(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_128(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_129(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_130(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error(None, r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_131(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=None, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_132(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=None, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_133(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=None)
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_134(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error(r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_135(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_136(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_137(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error(
            "🏭❌ Resource creation failed",
            r_type=r_type,
            r_name=r_name,
        )
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_138(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("XX🏭❌ Resource creation failedXX", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_139(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_140(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ RESOURCE CREATION FAILED", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_141(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(None))
        raise HclFactoryError(f"Internal error creating resource CtyValue: {e}") from e


def x_create_resource_cty__mutmut_142(  # noqa: C901
    r_type: str,
    r_name: str,
    attributes_py: dict[str, Any],
    attributes_schema_py: dict[str, str] | None = None,
) -> CtyValue[Any]:
    """Create a Terraform resource CTY structure.

    Args:
        r_type: Resource type (e.g., "aws_instance")
        r_name: Resource name
        attributes_py: Resource attributes as Python dict
        attributes_schema_py: Optional type strings for attributes

    Returns:
        CTY value representing Terraform resource structure

    Raises:
        HclFactoryError: If validation fails

    Example:
        >>> resource = create_resource_cty(
        ...     r_type="aws_instance",
        ...     r_name="web",
        ...     attributes_py={"ami": "ami-123", "instance_type": "t2.micro"},
        ...     attributes_schema_py={"ami": "string", "instance_type": "string"}
        ... )
    """
    logger.debug("🏭⏳ Creating resource", r_type=r_type, r_name=r_name)

    if not r_type or not r_type.strip():
        logger.error("🏭❌ Empty resource type")
        raise HclFactoryError("Resource type 'r_type' cannot be empty.")

    if not r_name or not r_name.strip():
        logger.error("🏭❌ Empty resource name")
        raise HclFactoryError("Resource name 'r_name' cannot be empty.")

    attributes_cty_schema: dict[str, CtyType[Any]] = {}

    if attributes_schema_py is not None:
        for attr_name, attr_type_str in attributes_schema_py.items():
            try:
                attributes_cty_schema[attr_name] = parse_hcl_type_string(attr_type_str)
            except HclTypeParsingError as e:
                logger.error(
                    "🏭❌ Attribute type parsing failed",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                    type_str=attr_type_str,
                    error=str(e),
                )
                raise HclFactoryError(
                    f"Invalid type string for attribute '{attr_name}' ('{attr_type_str}') "
                    f"in resource '{r_type}.{r_name}': {e}"
                ) from e

        for attr_name in attributes_py:
            if attr_name not in attributes_cty_schema:
                logger.error(
                    "🏭❌ Missing type for attribute",
                    r_type=r_type,
                    r_name=r_name,
                    attr_name=attr_name,
                )
                raise HclFactoryError(
                    f"Missing type string in attributes_schema_py for attribute '{attr_name}' "
                    f"of resource '{r_type}.{r_name}'."
                )

        resource_attributes_obj_type = CtyObject(attributes_cty_schema)
        try:
            resource_attributes_obj_type.validate(attributes_py)
        except CtyValidationError as e:
            logger.error(
                "🏭❌ Attribute validation failed",
                r_type=r_type,
                r_name=r_name,
                error=str(e),
            )
            raise HclFactoryError(
                f"One or more attributes for resource '{r_type}.{r_name}' are not compatible "
                f"with the provided schema: {e}"
            ) from e
    else:
        logger.debug("🏭⏳ Inferring attribute types", r_type=r_type, r_name=r_name)
        inferred_attributes_cty = auto_infer_cty_type(attributes_py)
        if isinstance(inferred_attributes_cty.type, CtyObject):
            attributes_cty_schema = inferred_attributes_cty.type.attribute_types
        else:
            logger.error("🏭❌ Type inference failed", r_type=r_type, r_name=r_name)
            raise HclFactoryError("Could not infer object type from attributes.")

    root_py_struct = {"resource": [{r_type: [{r_name: attributes_py}]}]}
    root_schema = CtyObject(
        {
            "resource": CtyList(
                element_type=CtyObject(
                    {r_type: CtyList(element_type=CtyObject({r_name: CtyObject(attributes_cty_schema)}))}
                )
            )
        }
    )

    try:
        result = root_schema.validate(root_py_struct)
        return result  # type: ignore[no-any-return]
    except CtyError as e:
        logger.error("🏭❌ Resource creation failed", r_type=r_type, r_name=r_name, error=str(e))
        raise HclFactoryError(None) from e


x_create_resource_cty__mutmut_mutants: ClassVar[MutantDict] = {
    "x_create_resource_cty__mutmut_1": x_create_resource_cty__mutmut_1,
    "x_create_resource_cty__mutmut_2": x_create_resource_cty__mutmut_2,
    "x_create_resource_cty__mutmut_3": x_create_resource_cty__mutmut_3,
    "x_create_resource_cty__mutmut_4": x_create_resource_cty__mutmut_4,
    "x_create_resource_cty__mutmut_5": x_create_resource_cty__mutmut_5,
    "x_create_resource_cty__mutmut_6": x_create_resource_cty__mutmut_6,
    "x_create_resource_cty__mutmut_7": x_create_resource_cty__mutmut_7,
    "x_create_resource_cty__mutmut_8": x_create_resource_cty__mutmut_8,
    "x_create_resource_cty__mutmut_9": x_create_resource_cty__mutmut_9,
    "x_create_resource_cty__mutmut_10": x_create_resource_cty__mutmut_10,
    "x_create_resource_cty__mutmut_11": x_create_resource_cty__mutmut_11,
    "x_create_resource_cty__mutmut_12": x_create_resource_cty__mutmut_12,
    "x_create_resource_cty__mutmut_13": x_create_resource_cty__mutmut_13,
    "x_create_resource_cty__mutmut_14": x_create_resource_cty__mutmut_14,
    "x_create_resource_cty__mutmut_15": x_create_resource_cty__mutmut_15,
    "x_create_resource_cty__mutmut_16": x_create_resource_cty__mutmut_16,
    "x_create_resource_cty__mutmut_17": x_create_resource_cty__mutmut_17,
    "x_create_resource_cty__mutmut_18": x_create_resource_cty__mutmut_18,
    "x_create_resource_cty__mutmut_19": x_create_resource_cty__mutmut_19,
    "x_create_resource_cty__mutmut_20": x_create_resource_cty__mutmut_20,
    "x_create_resource_cty__mutmut_21": x_create_resource_cty__mutmut_21,
    "x_create_resource_cty__mutmut_22": x_create_resource_cty__mutmut_22,
    "x_create_resource_cty__mutmut_23": x_create_resource_cty__mutmut_23,
    "x_create_resource_cty__mutmut_24": x_create_resource_cty__mutmut_24,
    "x_create_resource_cty__mutmut_25": x_create_resource_cty__mutmut_25,
    "x_create_resource_cty__mutmut_26": x_create_resource_cty__mutmut_26,
    "x_create_resource_cty__mutmut_27": x_create_resource_cty__mutmut_27,
    "x_create_resource_cty__mutmut_28": x_create_resource_cty__mutmut_28,
    "x_create_resource_cty__mutmut_29": x_create_resource_cty__mutmut_29,
    "x_create_resource_cty__mutmut_30": x_create_resource_cty__mutmut_30,
    "x_create_resource_cty__mutmut_31": x_create_resource_cty__mutmut_31,
    "x_create_resource_cty__mutmut_32": x_create_resource_cty__mutmut_32,
    "x_create_resource_cty__mutmut_33": x_create_resource_cty__mutmut_33,
    "x_create_resource_cty__mutmut_34": x_create_resource_cty__mutmut_34,
    "x_create_resource_cty__mutmut_35": x_create_resource_cty__mutmut_35,
    "x_create_resource_cty__mutmut_36": x_create_resource_cty__mutmut_36,
    "x_create_resource_cty__mutmut_37": x_create_resource_cty__mutmut_37,
    "x_create_resource_cty__mutmut_38": x_create_resource_cty__mutmut_38,
    "x_create_resource_cty__mutmut_39": x_create_resource_cty__mutmut_39,
    "x_create_resource_cty__mutmut_40": x_create_resource_cty__mutmut_40,
    "x_create_resource_cty__mutmut_41": x_create_resource_cty__mutmut_41,
    "x_create_resource_cty__mutmut_42": x_create_resource_cty__mutmut_42,
    "x_create_resource_cty__mutmut_43": x_create_resource_cty__mutmut_43,
    "x_create_resource_cty__mutmut_44": x_create_resource_cty__mutmut_44,
    "x_create_resource_cty__mutmut_45": x_create_resource_cty__mutmut_45,
    "x_create_resource_cty__mutmut_46": x_create_resource_cty__mutmut_46,
    "x_create_resource_cty__mutmut_47": x_create_resource_cty__mutmut_47,
    "x_create_resource_cty__mutmut_48": x_create_resource_cty__mutmut_48,
    "x_create_resource_cty__mutmut_49": x_create_resource_cty__mutmut_49,
    "x_create_resource_cty__mutmut_50": x_create_resource_cty__mutmut_50,
    "x_create_resource_cty__mutmut_51": x_create_resource_cty__mutmut_51,
    "x_create_resource_cty__mutmut_52": x_create_resource_cty__mutmut_52,
    "x_create_resource_cty__mutmut_53": x_create_resource_cty__mutmut_53,
    "x_create_resource_cty__mutmut_54": x_create_resource_cty__mutmut_54,
    "x_create_resource_cty__mutmut_55": x_create_resource_cty__mutmut_55,
    "x_create_resource_cty__mutmut_56": x_create_resource_cty__mutmut_56,
    "x_create_resource_cty__mutmut_57": x_create_resource_cty__mutmut_57,
    "x_create_resource_cty__mutmut_58": x_create_resource_cty__mutmut_58,
    "x_create_resource_cty__mutmut_59": x_create_resource_cty__mutmut_59,
    "x_create_resource_cty__mutmut_60": x_create_resource_cty__mutmut_60,
    "x_create_resource_cty__mutmut_61": x_create_resource_cty__mutmut_61,
    "x_create_resource_cty__mutmut_62": x_create_resource_cty__mutmut_62,
    "x_create_resource_cty__mutmut_63": x_create_resource_cty__mutmut_63,
    "x_create_resource_cty__mutmut_64": x_create_resource_cty__mutmut_64,
    "x_create_resource_cty__mutmut_65": x_create_resource_cty__mutmut_65,
    "x_create_resource_cty__mutmut_66": x_create_resource_cty__mutmut_66,
    "x_create_resource_cty__mutmut_67": x_create_resource_cty__mutmut_67,
    "x_create_resource_cty__mutmut_68": x_create_resource_cty__mutmut_68,
    "x_create_resource_cty__mutmut_69": x_create_resource_cty__mutmut_69,
    "x_create_resource_cty__mutmut_70": x_create_resource_cty__mutmut_70,
    "x_create_resource_cty__mutmut_71": x_create_resource_cty__mutmut_71,
    "x_create_resource_cty__mutmut_72": x_create_resource_cty__mutmut_72,
    "x_create_resource_cty__mutmut_73": x_create_resource_cty__mutmut_73,
    "x_create_resource_cty__mutmut_74": x_create_resource_cty__mutmut_74,
    "x_create_resource_cty__mutmut_75": x_create_resource_cty__mutmut_75,
    "x_create_resource_cty__mutmut_76": x_create_resource_cty__mutmut_76,
    "x_create_resource_cty__mutmut_77": x_create_resource_cty__mutmut_77,
    "x_create_resource_cty__mutmut_78": x_create_resource_cty__mutmut_78,
    "x_create_resource_cty__mutmut_79": x_create_resource_cty__mutmut_79,
    "x_create_resource_cty__mutmut_80": x_create_resource_cty__mutmut_80,
    "x_create_resource_cty__mutmut_81": x_create_resource_cty__mutmut_81,
    "x_create_resource_cty__mutmut_82": x_create_resource_cty__mutmut_82,
    "x_create_resource_cty__mutmut_83": x_create_resource_cty__mutmut_83,
    "x_create_resource_cty__mutmut_84": x_create_resource_cty__mutmut_84,
    "x_create_resource_cty__mutmut_85": x_create_resource_cty__mutmut_85,
    "x_create_resource_cty__mutmut_86": x_create_resource_cty__mutmut_86,
    "x_create_resource_cty__mutmut_87": x_create_resource_cty__mutmut_87,
    "x_create_resource_cty__mutmut_88": x_create_resource_cty__mutmut_88,
    "x_create_resource_cty__mutmut_89": x_create_resource_cty__mutmut_89,
    "x_create_resource_cty__mutmut_90": x_create_resource_cty__mutmut_90,
    "x_create_resource_cty__mutmut_91": x_create_resource_cty__mutmut_91,
    "x_create_resource_cty__mutmut_92": x_create_resource_cty__mutmut_92,
    "x_create_resource_cty__mutmut_93": x_create_resource_cty__mutmut_93,
    "x_create_resource_cty__mutmut_94": x_create_resource_cty__mutmut_94,
    "x_create_resource_cty__mutmut_95": x_create_resource_cty__mutmut_95,
    "x_create_resource_cty__mutmut_96": x_create_resource_cty__mutmut_96,
    "x_create_resource_cty__mutmut_97": x_create_resource_cty__mutmut_97,
    "x_create_resource_cty__mutmut_98": x_create_resource_cty__mutmut_98,
    "x_create_resource_cty__mutmut_99": x_create_resource_cty__mutmut_99,
    "x_create_resource_cty__mutmut_100": x_create_resource_cty__mutmut_100,
    "x_create_resource_cty__mutmut_101": x_create_resource_cty__mutmut_101,
    "x_create_resource_cty__mutmut_102": x_create_resource_cty__mutmut_102,
    "x_create_resource_cty__mutmut_103": x_create_resource_cty__mutmut_103,
    "x_create_resource_cty__mutmut_104": x_create_resource_cty__mutmut_104,
    "x_create_resource_cty__mutmut_105": x_create_resource_cty__mutmut_105,
    "x_create_resource_cty__mutmut_106": x_create_resource_cty__mutmut_106,
    "x_create_resource_cty__mutmut_107": x_create_resource_cty__mutmut_107,
    "x_create_resource_cty__mutmut_108": x_create_resource_cty__mutmut_108,
    "x_create_resource_cty__mutmut_109": x_create_resource_cty__mutmut_109,
    "x_create_resource_cty__mutmut_110": x_create_resource_cty__mutmut_110,
    "x_create_resource_cty__mutmut_111": x_create_resource_cty__mutmut_111,
    "x_create_resource_cty__mutmut_112": x_create_resource_cty__mutmut_112,
    "x_create_resource_cty__mutmut_113": x_create_resource_cty__mutmut_113,
    "x_create_resource_cty__mutmut_114": x_create_resource_cty__mutmut_114,
    "x_create_resource_cty__mutmut_115": x_create_resource_cty__mutmut_115,
    "x_create_resource_cty__mutmut_116": x_create_resource_cty__mutmut_116,
    "x_create_resource_cty__mutmut_117": x_create_resource_cty__mutmut_117,
    "x_create_resource_cty__mutmut_118": x_create_resource_cty__mutmut_118,
    "x_create_resource_cty__mutmut_119": x_create_resource_cty__mutmut_119,
    "x_create_resource_cty__mutmut_120": x_create_resource_cty__mutmut_120,
    "x_create_resource_cty__mutmut_121": x_create_resource_cty__mutmut_121,
    "x_create_resource_cty__mutmut_122": x_create_resource_cty__mutmut_122,
    "x_create_resource_cty__mutmut_123": x_create_resource_cty__mutmut_123,
    "x_create_resource_cty__mutmut_124": x_create_resource_cty__mutmut_124,
    "x_create_resource_cty__mutmut_125": x_create_resource_cty__mutmut_125,
    "x_create_resource_cty__mutmut_126": x_create_resource_cty__mutmut_126,
    "x_create_resource_cty__mutmut_127": x_create_resource_cty__mutmut_127,
    "x_create_resource_cty__mutmut_128": x_create_resource_cty__mutmut_128,
    "x_create_resource_cty__mutmut_129": x_create_resource_cty__mutmut_129,
    "x_create_resource_cty__mutmut_130": x_create_resource_cty__mutmut_130,
    "x_create_resource_cty__mutmut_131": x_create_resource_cty__mutmut_131,
    "x_create_resource_cty__mutmut_132": x_create_resource_cty__mutmut_132,
    "x_create_resource_cty__mutmut_133": x_create_resource_cty__mutmut_133,
    "x_create_resource_cty__mutmut_134": x_create_resource_cty__mutmut_134,
    "x_create_resource_cty__mutmut_135": x_create_resource_cty__mutmut_135,
    "x_create_resource_cty__mutmut_136": x_create_resource_cty__mutmut_136,
    "x_create_resource_cty__mutmut_137": x_create_resource_cty__mutmut_137,
    "x_create_resource_cty__mutmut_138": x_create_resource_cty__mutmut_138,
    "x_create_resource_cty__mutmut_139": x_create_resource_cty__mutmut_139,
    "x_create_resource_cty__mutmut_140": x_create_resource_cty__mutmut_140,
    "x_create_resource_cty__mutmut_141": x_create_resource_cty__mutmut_141,
    "x_create_resource_cty__mutmut_142": x_create_resource_cty__mutmut_142,
}


def create_resource_cty(*args, **kwargs):
    result = _mutmut_trampoline(
        x_create_resource_cty__mutmut_orig, x_create_resource_cty__mutmut_mutants, args, kwargs
    )
    return result


create_resource_cty.__signature__ = _mutmut_signature(x_create_resource_cty__mutmut_orig)
x_create_resource_cty__mutmut_orig.__name__ = "x_create_resource_cty"

# 📄⚙️🔚
