# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""A stable skeleton of the pyclingo python API for solve results."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Literal, overload
from typing_extensions import Self


class SolveResult:
    exhausted: bool
    interrupted: bool
    satisfiable: bool | None
    unknown: bool
    unsatisfiable: bool | None

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...


class SolveHandle:
    def cancel(self) -> None: ...

    def get(self) -> SolveResult: ...

    def wait(self, timeout: float | None = None) -> bool: ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_ty: type[BaseException] | None,
        exc_val: BaseException | None,
        tb: TracebackType | None,
    ) -> bool | None:
        ...


class Control:
    @overload
    def solve(self, *args: Any, async_: Literal[True], **kwargs: Any) -> SolveHandle:
        ...

    @overload
    def solve(self, *args: Any, async_: Literal[False], **kwargs: Any) -> SolveResult:
        ...

    def interrupt(self) -> None:
        ...
