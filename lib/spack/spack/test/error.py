# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for the base class of every Spack error."""

import pickle

import pytest

import spack.error
import spack.solver.asp
from spack.spec import Spec


def test_error_keeps_its_state_through_a_pipe():
    """Tests that an error carries everything it holds to another process, and not just what
    its constructor takes.
    """
    error = spack.error.SpackError("boom", "details")
    # Saved by a child build process, so that the parent can print it
    error.traceback = "Traceback from the child\n"

    replayed = pickle.loads(pickle.dumps(error))

    assert type(replayed) is spack.error.SpackError
    assert (replayed.message, replayed.long_message) == ("boom", "details")
    assert replayed.traceback == "Traceback from the child\n"


@pytest.mark.parametrize(
    "factory",
    [
        lambda: spack.solver.asp.UnsatisfiableSpecError("boom"),
        lambda: spack.solver.asp.InternalConcretizerError("boom"),
        lambda: spack.solver.asp.SolverError(Spec("pkg-a")),
        lambda: spack.solver.asp.OutputDoesNotSatisfyInputError(
            [(Spec("pkg-a"), Spec("pkg-b")), (Spec("pkg-c"), None)]
        ),
    ],
    ids=["unsatisfiable", "internal", "solver", "output-does-not-satisfy-input"],
)
def test_errors_with_their_own_constructor_survive_a_pipe(factory):
    """Tests that an error whose __init__ takes something other than (message, long_message)
    round trips: rebuilding it by calling its class cannot work.
    """
    error = factory()

    replayed = pickle.loads(pickle.dumps(error))

    assert type(replayed) is type(error)
    assert str(replayed) == str(error)


def test_output_does_not_satisfy_input_keeps_its_specs():
    """Tests that the specs survive, and not just the message built from them: they are what
    spack.main._handle_solver_bug reports, and dumps to JSON for bug reports.
    """
    unsolved = [(Spec("pkg-a"), Spec("pkg-b")), (Spec("pkg-c"), None)]
    error = spack.solver.asp.OutputDoesNotSatisfyInputError(unsolved)

    replayed = pickle.loads(pickle.dumps(error))

    assert [(str(i), str(o) if o else None) for i, o in replayed.input_to_output] == [
        ("pkg-a", "pkg-b"),
        ("pkg-c", None),
    ]
