#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""pyvider-hcl: HCL parsing with CTY type system integration.

This package provides HCL (HashiCorp Configuration Language) parsing capabilities
with seamless integration into the pyvider ecosystem through the CTY type system."""

from pyvider.hcl._version import __version__
from pyvider.hcl.exceptions import HclError, HclParsingError
from pyvider.hcl.factories import (
    HclFactoryError,
    HclTypeParsingError,
    create_resource_cty,
    create_variable_cty,
)
from pyvider.hcl.output import pretty_print_cty
from pyvider.hcl.parser import auto_infer_cty_type, parse_hcl_to_cty, parse_with_context
from pyvider.hcl.terraform import parse_terraform_config

__all__ = [
    "HclError",
    "HclFactoryError",
    "HclParsingError",
    "HclTypeParsingError",
    "__version__",
    "auto_infer_cty_type",
    "create_resource_cty",
    "create_variable_cty",
    "parse_hcl_to_cty",
    "parse_terraform_config",
    "parse_with_context",
    "pretty_print_cty",
]
from collections.abc import Callable
from inspect import signature as _mutmut_signature
from typing import Annotated, ClassVar

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


# 📄⚙️🔚
