#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""HCL parsing with enhanced error context."""

from __future__ import annotations

from collections.abc import Callable
from inspect import signature as _mutmut_signature
from pathlib import Path
from typing import Annotated, Any, ClassVar

import hcl2
from provide.foundation import logger

from pyvider.hcl.exceptions import HclParsingError

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


def x_parse_with_context__mutmut_orig(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_1(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = None

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_2(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(None) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_3(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "XXstring inputXX"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_4(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "STRING INPUT"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_5(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"
    logger.debug(None, source=source_str)

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_6(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_7(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"
    logger.debug(source=source_str)

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_8(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_9(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_10(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_11(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_12(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(None)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_13(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            None,
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_14(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=None,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_15(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=None,
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_16(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=None,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_17(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_18(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_19(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_20(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_21(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_22(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_23(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_24(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(None),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_25(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=False,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_26(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=None,
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_27(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=None,
        ) from e


def x_parse_with_context__mutmut_28(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_29(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
        ) from e


def x_parse_with_context__mutmut_30(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(None),
            source_file=str(source_file) if source_file else None,
        ) from e


def x_parse_with_context__mutmut_31(content: str, source_file: Path | None = None) -> Any:
    """Parse HCL content with enhanced error context.

    This function parses HCL content and provides rich error context if parsing fails.
    It returns the raw parsed data (dict/list), not CTY values.

    Args:
        content: HCL content string to parse
        source_file: Optional source file path for error reporting

    Returns:
        Raw parsed data (typically dict or list)

    Raises:
        HclParsingError: If parsing fails, with source location information

    Example:
        >>> content = 'name = "example"'
        >>> data = parse_with_context(content)
        >>> data['name']
        'example'
    """
    source_str = str(source_file) if source_file else "string input"

    try:
        return hcl2.loads(content)  # type: ignore[attr-defined]
    except Exception as e:
        logger.error(
            source=source_str,
            error=str(e),
            exc_info=True,
        )
        raise HclParsingError(
            message=str(e),
            source_file=str(None) if source_file else None,
        ) from e


x_parse_with_context__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_with_context__mutmut_1": x_parse_with_context__mutmut_1,
    "x_parse_with_context__mutmut_2": x_parse_with_context__mutmut_2,
    "x_parse_with_context__mutmut_3": x_parse_with_context__mutmut_3,
    "x_parse_with_context__mutmut_4": x_parse_with_context__mutmut_4,
    "x_parse_with_context__mutmut_5": x_parse_with_context__mutmut_5,
    "x_parse_with_context__mutmut_6": x_parse_with_context__mutmut_6,
    "x_parse_with_context__mutmut_7": x_parse_with_context__mutmut_7,
    "x_parse_with_context__mutmut_8": x_parse_with_context__mutmut_8,
    "x_parse_with_context__mutmut_9": x_parse_with_context__mutmut_9,
    "x_parse_with_context__mutmut_10": x_parse_with_context__mutmut_10,
    "x_parse_with_context__mutmut_11": x_parse_with_context__mutmut_11,
    "x_parse_with_context__mutmut_12": x_parse_with_context__mutmut_12,
    "x_parse_with_context__mutmut_13": x_parse_with_context__mutmut_13,
    "x_parse_with_context__mutmut_14": x_parse_with_context__mutmut_14,
    "x_parse_with_context__mutmut_15": x_parse_with_context__mutmut_15,
    "x_parse_with_context__mutmut_16": x_parse_with_context__mutmut_16,
    "x_parse_with_context__mutmut_17": x_parse_with_context__mutmut_17,
    "x_parse_with_context__mutmut_18": x_parse_with_context__mutmut_18,
    "x_parse_with_context__mutmut_19": x_parse_with_context__mutmut_19,
    "x_parse_with_context__mutmut_20": x_parse_with_context__mutmut_20,
    "x_parse_with_context__mutmut_21": x_parse_with_context__mutmut_21,
    "x_parse_with_context__mutmut_22": x_parse_with_context__mutmut_22,
    "x_parse_with_context__mutmut_23": x_parse_with_context__mutmut_23,
    "x_parse_with_context__mutmut_24": x_parse_with_context__mutmut_24,
    "x_parse_with_context__mutmut_25": x_parse_with_context__mutmut_25,
    "x_parse_with_context__mutmut_26": x_parse_with_context__mutmut_26,
    "x_parse_with_context__mutmut_27": x_parse_with_context__mutmut_27,
    "x_parse_with_context__mutmut_28": x_parse_with_context__mutmut_28,
    "x_parse_with_context__mutmut_29": x_parse_with_context__mutmut_29,
    "x_parse_with_context__mutmut_30": x_parse_with_context__mutmut_30,
    "x_parse_with_context__mutmut_31": x_parse_with_context__mutmut_31,
}


def parse_with_context(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_with_context__mutmut_orig, x_parse_with_context__mutmut_mutants, args, kwargs
    )
    return result


parse_with_context.__signature__ = _mutmut_signature(x_parse_with_context__mutmut_orig)
x_parse_with_context__mutmut_orig.__name__ = "x_parse_with_context"

# 📄⚙️🔚
