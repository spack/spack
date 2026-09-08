# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Errors raised by the concretizer.

This module holds no solver state, so that both the solver and the types it produces can
depend on it without importing each other.
"""

from typing import List, Optional, Tuple

import spack.error
import spack.spec


def format_unsolved(
    unsolved_specs: List[Tuple[spack.spec.Spec, Optional[spack.spec.Spec]]],
) -> str:
    """Create a message providing info on unsolved user specs and for each one show the
    associated candidate spec from the solver (if there is one).
    """
    msg = "Unsatisfied input specs:"
    for input_spec, candidate in unsolved_specs:
        msg += f"\n\tInput spec: {str(input_spec)}"
        if candidate:
            msg += f"\n\tCandidate spec: {candidate.long_spec}"
        else:
            msg += "\n\t(No candidate specs from solver)"
    return msg


class UnsatisfiableSpecError(spack.error.UnsatisfiableSpecError):
    """There was an issue with the spec that was requested (i.e. a user error)."""

    def __init__(self, msg):
        super(spack.error.UnsatisfiableSpecError, self).__init__(msg)
        self.provided = None
        self.required = None
        self.constraint_type = None


class InternalConcretizerError(spack.error.UnsatisfiableSpecError):
    """Errors that indicate a bug in Spack."""

    def __init__(self, msg):
        super(spack.error.UnsatisfiableSpecError, self).__init__(msg)
        self.provided = None
        self.required = None
        self.constraint_type = None


class OutputDoesNotSatisfyInputError(InternalConcretizerError):
    def __init__(
        self, input_to_output: List[Tuple[spack.spec.Spec, Optional[spack.spec.Spec]]]
    ) -> None:
        self.input_to_output = input_to_output
        super().__init__(
            "internal solver error: the solver completed but produced specs"
            " that do not satisfy the request. Please report a bug at "
            f"https://github.com/spack/spack/issues\n\t{format_unsolved(input_to_output)}"
        )


class SolverError(InternalConcretizerError):
    """For cases where the solver is unable to produce a solution.

    Such cases are unexpected because we allow for solutions with errors,
    so for example user specs that are over-constrained should still
    get a solution.
    """

    def __init__(self, provided):
        msg = (
            "Spack concretizer internal error. Please submit a bug report at "
            "https://github.com/spack/spack and include the command and environment "
            "if applicable."
            f"\n    {provided} is unsatisfiable"
        )

        super().__init__(msg)

        # Add attribute expected of the superclass interface
        self.required = None
        self.constraint_type = None
        self.provided = provided


class InvalidSpliceError(spack.error.SpackError):
    """For cases in which the splice configuration is invalid."""


class SpliceSerializationError(spack.error.SpackError):
    """Attempt to serialize a SpecDict that contains spliced specs (currently unsupported)."""


class DeprecatedVersionError(spack.error.SpackError):
    """Raised when user directly requests a deprecated version."""


class InvalidVersionError(spack.error.SpackError):
    """Raised when a version can't be satisfied by any possible versions."""


class InvalidDependencyError(spack.error.SpackError):
    """Raised when an explicit dependency is not a possible dependency."""
