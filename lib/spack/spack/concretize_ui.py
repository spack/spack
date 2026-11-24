# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Frontends for concretization.

Defines the :class:`ConcretizerUI` contract (a headless no-op base) and the terminal
:class:`TerminalUI` implementation.

Concretization is reported as two nested spans, each with a ``started``/``finished`` pair:

1. the concretization, one per request to concretize a set of specs;
2. the group, inside which the configuration that drives concretization is fixed. Environments
   define groups of user specs, a request without one has a single, default, group.

Every span that opens closes exactly once, including when an exception passes through it. A close
signals teardown and reports no outcome, so no callback takes an exception: anything raised
propagates to the caller, which decides how to handle it.
"""

import contextlib
import enum
import sys
from typing import Iterator

from spack.spec import Spec
from spack.util import tty

#: Name of the group of user specs that every concretization has. An environment can define more,
#: a request without one has only this.
DEFAULT_USER_SPEC_GROUP = "default"


class SolveKind(enum.Enum):
    """How the specs to be concretized are distributed over solves."""

    #: A single solve produces every spec
    TOGETHER = "together"
    #: One solve per set of specs that can be unified
    WHEN_POSSIBLE = "when_possible"
    #: One solve per spec, possibly in parallel
    SEPARATELY = "separately"


class ConcretizerUI:
    """Interface between concretization and a frontend. The methods are no-ops, which makes this
    class usable as a headless frontend.

    Every event is emitted in the process that owns the frontend, and from a single thread.
    Frontends therefore need no locking, and no capture of child output.
    """

    def on_concretization_started(self) -> None:
        """A concretization is about to start. Frontends use it to scope the state they keep
        for one request.
        """

    def on_concretization_finished(self) -> None:
        """The concretization that started is over."""

    def on_group_started(self, *, group: str, kind: SolveKind, total: int, processes: int) -> None:
        """The ``group`` of user specs is about to be concretized as ``kind`` prescribes, over
        ``processes`` processes. ``total`` is the number of ``on_spec_concretized`` calls that
        will follow for this group, which frontends may use to show a percentage.
        """

    def on_group_finished(self) -> None:
        """The group that started is over."""

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, count: int, duration: float
    ) -> None:
        """A user spec has been concretized. ``count`` is how many specs of the group have been
        reported so far, including this one, and goes from 1 to the announced ``total``.
        ``duration`` is the time spent in the solve that produced this spec, so specs that come
        out of the same solve report the same duration.
        """


#: Frontend that reports nothing. Same class as the contract it implements, aliased so that call
#: sites can say which of the two roles they mean.
HeadlessUI = ConcretizerUI


@contextlib.contextmanager
def concretization_span(ui: ConcretizerUI) -> Iterator[None]:
    """Report the start and the end of a concretization. The end is reported even when the body
    raises, so that a frontend can tear down what it painted. The exception propagates to the
    caller without being passed to the frontend.
    """
    ui.on_concretization_started()
    try:
        yield
    finally:
        ui.on_concretization_finished()


@contextlib.contextmanager
def group_span(
    ui: ConcretizerUI, *, group: str, kind: SolveKind, total: int, processes: int
) -> Iterator[None]:
    """Report the start and the end of one group of user specs. As for ``concretization_span``,
    the end is reported even when the body raises.
    """
    ui.on_group_started(group=group, kind=kind, total=total, processes=processes)
    try:
        yield
    finally:
        ui.on_group_finished()


class TerminalUI(ConcretizerUI):
    """Terminal frontend: announces groups and solves, and reports per-spec progress."""

    def __init__(self) -> None:
        self.kind = SolveKind.TOGETHER
        self.total = 0

    def on_group_started(self, *, group: str, kind: SolveKind, total: int, processes: int) -> None:
        self.kind = kind
        self.total = total
        if total == 0:
            return
        if group != DEFAULT_USER_SPEC_GROUP:
            tty.msg(f"Concretizing the '{group}' group of specs")
        if kind is not SolveKind.SEPARATELY:
            return
        msg = "Starting concretization"
        if processes > 1:
            msg += f" pool with {processes} processes"
        tty.msg(msg)

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, count: int, duration: float
    ) -> None:
        if self.kind is SolveKind.TOGETHER:
            return
        percentage = int(count / self.total * 100)
        tty.verbose(
            f"{duration:6.1f}s [{percentage:3d}%] {concrete.cformat('{hash:7}')} "
            f"{abstract.colored_str}",
            stream=sys.stdout,
        )
        sys.stdout.flush()
