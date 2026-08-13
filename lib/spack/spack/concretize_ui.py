# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Frontends for concretization.

Defines the :class:`ConcretizerUI` contract (a headless no-op base) and the interactive
:class:`TerminalUI` implementation. Concretization reports facts through this interface, and the
frontend decides whether, where, and how to render them.
"""

import sys

from spack.spec import Spec
from spack.util import tty


class ConcretizerUI:
    """Interface between concretization and a frontend. The methods are no-ops, which makes this
    class usable as a headless frontend.
    """

    def on_group_started(self, *, group: str, is_default: bool) -> None:
        """A group of user specs is about to be concretized."""

    def on_batch_started(self, *, total: int, processes: int) -> None:
        """A batch of ``total`` independent solves is about to start, distributed over
        ``processes`` processes.
        """

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, index: int, total: int, duration: float
    ) -> None:
        """A user spec has been concretized. ``index`` is the 0-based completion order, and
        ``duration`` is the time spent solving, or the time spent in the current round for
        ``unify: when_possible``.
        """


class TerminalUI(ConcretizerUI):
    """Terminal frontend: announces groups and batches, and reports per-spec progress."""

    def on_group_started(self, *, group: str, is_default: bool) -> None:
        if is_default:
            return
        tty.msg(f"Concretizing the '{group}' group of specs")

    def on_batch_started(self, *, total: int, processes: int) -> None:
        msg = "Starting concretization"
        if processes > 1:
            msg += f" pool with {processes} processes"
        tty.msg(msg)

    def on_spec_concretized(
        self, abstract: Spec, *, concrete: Spec, index: int, total: int, duration: float
    ) -> None:
        percentage = int((index + 1) / total * 100)
        tty.verbose(
            f"{duration:6.1f}s [{percentage:3d}%] {concrete.cformat('{hash:7}')} "
            f"{abstract.colored_str}",
            stream=sys.stdout,
        )
        sys.stdout.flush()
