# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Frontends for concretization.

Defines the :class:`ConcretizerUI` contract (a headless no-op base) and the terminal
:class:`TerminalUI` implementation.
"""

import enum
import sys

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
        """A user spec has been concretized. ``count`` is the 0-based position of this event among
        the ones reported for the group, and ``duration`` is the time spent in the solve that
        produced this spec. Specs that come out of the same solve report the same duration.
        """


#: Frontend that reports nothing. Same class as the contract it implements, aliased so that call
#: sites can say which of the two roles they mean.
HeadlessUI = ConcretizerUI


class TerminalUI(ConcretizerUI):
    """Terminal frontend: announces groups and solves, and reports per-spec progress."""

    def __init__(self) -> None:
        self.kind = SolveKind.TOGETHER
        self.total = 0

    def on_group_started(self, *, group: str, is_default: bool) -> None:
        if is_default:
            return
        tty.msg(f"Concretizing the '{group}' group of specs")

    def on_concretization_started(self, *, kind: SolveKind, total: int, processes: int) -> None:
        self.kind = kind
        self.total = total
        if kind is not SolveKind.SEPARATELY or total == 0:
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
        percentage = int((count + 1) / max(self.total, count + 1) * 100)
        tty.verbose(
            f"{duration:6.1f}s [{percentage:3d}%] {concrete.cformat('{hash:7}')} "
            f"{abstract.colored_str}",
            stream=sys.stdout,
        )
        sys.stdout.flush()
