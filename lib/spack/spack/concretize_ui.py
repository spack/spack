# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Frontends for concretization.

Defines the :class:`ConcretizerUI` contract (a headless no-op base) and the terminal
:class:`TerminalUI` implementation.
"""

import enum
import sys
from typing import Optional

from spack.spec import Spec
from spack.util import tty


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

    def on_group_started(self, *, group: str, is_default: bool) -> None:
        """A group of user specs is about to be concretized."""

    def on_concretization_started(self, *, kind: SolveKind, total: int, processes: int) -> None:
        """``total`` user specs are about to be concretized as ``kind`` prescribes, over
        ``processes`` processes. Called once per group of user specs, before any spec of that
        group is reported, with ``total`` equal to the number of ``on_spec_concretized`` calls
        that will follow for it.
        """

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, count: int, duration: float
    ) -> None:
        """A user spec has been concretized. ``count`` is how many specs of the group have been
        reported so far, including this one, and goes from 1 to the announced ``total``.
        ``duration`` is the time spent in the solve that produced this spec, so specs that come
        out of the same solve report the same duration.
        """

    def on_finished(self, *, error: Optional[BaseException]) -> None:
        """Concretization is over, successfully if ``error`` is None. Emitted exactly once per
        concretization, from a ``finally``, so a frontend that renders can rely on it to tear
        down whatever it painted.
        """


#: Frontend that reports nothing. Same class as the contract it implements, aliased so that call
#: sites can say which of the two roles they mean.
HeadlessUI = ConcretizerUI


class TerminalUI(ConcretizerUI):
    """Terminal frontend: announces groups and solves, and reports per-spec progress."""

    def __init__(self) -> None:
        self.kind = SolveKind.TOGETHER
        self.total = 0
        self.pending_group: Optional[str] = None

    def on_group_started(self, *, group: str, is_default: bool) -> None:
        # Held back until we know the group has specs to concretize
        self.pending_group = None if is_default else group

    def on_concretization_started(self, *, kind: SolveKind, total: int, processes: int) -> None:
        self.kind = kind
        self.total = total
        if total == 0:
            return
        if self.pending_group is not None:
            tty.msg(f"Concretizing the '{self.pending_group}' group of specs")
            self.pending_group = None
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
