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


class SupportsRichComparison(Protocol):
    """Objects that support =, !=, <, <=, >, and >=."""

    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    def __ne__(self, other: Any) -> bool:
        raise NotImplementedError

    def __lt__(self, other: Any) -> bool:
        raise NotImplementedError

    def __le__(self, other: Any) -> bool:
        raise NotImplementedError

    def __gt__(self, other: Any) -> bool:
        raise NotImplementedError

    def __ge__(self, other: Any) -> bool:
        raise NotImplementedError


if not TYPE_CHECKING:
    SupportRichComparison = object
