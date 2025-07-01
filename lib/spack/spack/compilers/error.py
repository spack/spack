# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import warnings

from ..error import SpackAPIWarning, SpackError


class CompilerAccessError(SpackError):
    def __init__(self, compiler, paths):
        super().__init__(
            f"Compiler '{compiler.spec}' has executables that are missing"
            f" or are not executable: {paths}"
        )


class UnsupportedCompilerFlag(SpackError):
    """Raised when a compiler does not support a flag type (e.g. a flag to enforce a
    language standard).
    """

    def __init__(self, message, long_message=None):
        warnings.warn(
            "UnsupportedCompilerFlag is deprecated, use CompilerError instead",
            SpackAPIWarning,
            stacklevel=2,
        )
