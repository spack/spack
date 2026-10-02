# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import TYPE_CHECKING, Any


class Bunch:
    """Carries a bunch of named attributes (from Alex Martelli bunch)"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    if TYPE_CHECKING:
        # attributes are dynamic: tell type checkers any attribute may be read or set
        def __getattr__(self, name: str) -> Any: ...

        def __setattr__(self, name: str, value: Any) -> None: ...


class Args(Bunch):
    """Subclass of Bunch to write argparse args more naturally."""

    def __init__(self, *flags, **kwargs):
        super().__init__(flags=tuple(flags), kwargs=kwargs)
