# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import warnings

import pytest

from spack.util.parallel import ErrorFromWorker, Task, imap_unordered


class CustomWarning(UserWarning):
    """Warning class defined in this module, to check the category survives the round trip."""


def _quiet(x):
    return x * 2


def _warns_once(x):
    warnings.warn("the same diagnostic from every worker")
    return x


def _warns_then_raises(x):
    warnings.warn("emitted before the failure", CustomWarning)
    raise ValueError("worker failed")


def test_task_returns_value_and_no_warnings():
    """A task that warns about nothing reports an empty list of warnings."""
    value, recorded = Task(_quiet)(21)

    assert value == 42
    assert recorded == []


def test_task_captures_warnings_instead_of_emitting_them(recwarn):
    """Warnings raised by the wrapped function are captured, not emitted in the caller's scope."""
    value, recorded = Task(_warns_once)(1)

    assert value == 1
    assert len(recorded) == 1
    assert recorded[0].message == "the same diagnostic from every worker"
    assert recorded[0].category is UserWarning
    # The warning was captured by the task, so it never reached this process' machinery
    assert len(recwarn) == 0


def test_task_captures_warnings_raised_before_an_error():
    """A task that fails still reports the warnings raised before the exception."""
    value, recorded = Task(_warns_then_raises)(1)

    assert isinstance(value, ErrorFromWorker)
    assert "worker failed" in str(value)
    assert len(recorded) == 1
    assert recorded[0].message == "emitted before the failure"
    assert recorded[0].category is CustomWarning


@pytest.mark.enable_parallelism
@pytest.mark.not_on_windows("processes pools are disabled on Windows")
def test_imap_unordered_deduplicates_warnings_across_workers():
    """A warning raised by every worker is re-emitted once in this process, so that a solve per
    spec doesn't repeat the same diagnostic once per spec.

    The deduplication is the one the "default" filter action performs through the warning
    registry, so this sets that action explicitly instead of using ``pytest.warns``, which forces
    "always" and bypasses the registry.
    """
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("default")
        results = list(imap_unordered(_warns_once, list(range(8)), processes=4, maxtaskperchild=1))

    assert sorted(results) == list(range(8))
    assert len(recorded) == 1
    assert "the same diagnostic" in str(recorded[0].message)
    # Provenance is preserved, so the warning is not attributed to spack.util.parallel
    assert recorded[0].filename == __file__


@pytest.mark.enable_parallelism
@pytest.mark.not_on_windows("processes pools are disabled on Windows")
def test_imap_unordered_reports_warnings_from_a_failing_worker():
    """Warnings raised before a worker fails are re-emitted, before the error is raised."""
    with pytest.warns(CustomWarning, match="emitted before the failure"):
        with pytest.raises(RuntimeError, match="worker failed"):
            list(imap_unordered(_warns_then_raises, list(range(2)), processes=2))
