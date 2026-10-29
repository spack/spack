# Copyright Spack Project Developers. See COPYRIGHT file for details.: object
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Extra support for type checking in Spack.

Protocols here that have runtime overhead should be set to ``object`` when
``TYPE_CHECKING`` is not enabled, as they can incur unreasonable runtime overheads.

In particular, Protocols intended for use on objects that have many ``isinstance()``
calls can be very expensive.

"""

from typing import TYPE_CHECKING, Any

from spack.vendor.typing_extensions import Protocol

if TYPE_CHECKING:

    class SupportsRichComparison(Protocol):
        """Objects that support =, !=, <, <=, >, and >=.

        Parameters use the ``__name`` convention to mark them positional-only, so that builtins
        like ``str`` (whose operator parameters are positional-only) satisfy the protocol."""

        def __eq__(self, __other: Any) -> bool:
            raise NotImplementedError

        def __ne__(self, __other: Any) -> bool:
            raise NotImplementedError

        def __lt__(self, __other: Any) -> bool:
            raise NotImplementedError

        def __le__(self, __other: Any) -> bool:
            raise NotImplementedError

        def __gt__(self, __other: Any) -> bool:
            raise NotImplementedError

        def __ge__(self, __other: Any) -> bool:
            raise NotImplementedError

else:
    SupportsRichComparison = object
