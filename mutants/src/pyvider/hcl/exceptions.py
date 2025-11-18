#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated

from attrs import define, field
from provide.foundation.errors import FoundationError

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


class HclError(FoundationError):
    """Base class for errors related to HCL processing in Pyvider."""

    pass


@define(frozen=True, slots=True, auto_exc=True)
class HclParsingError(HclError):
    """
    Raised when HCL parsing or schema validation fails.

    This is an attrs-based exception class for structured error reporting.
    """

    message: str = field()
    source_file: str | None = field(default=None)
    line: int | None = field(default=None)
    column: int | None = field(default=None)

    def __str__(self) -> str:
        """Provides a detailed error message including source location if available."""
        if self.source_file and self.line is not None and self.column is not None:
            return f"{self.message} (at {self.source_file}, line {self.line}, column {self.column})"
        elif self.source_file and self.line is not None:
            return f"{self.message} (at {self.source_file}, line {self.line})"
        elif self.source_file:
            return f"{self.message} (at {self.source_file})"
        return self.message


# 📄⚙️🔚
