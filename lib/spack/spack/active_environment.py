# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Module that tracks which environment is currently active."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import spack.environment

#: Currently activated environment. Do not set directly: use the setter below.
_active_environment: Optional["spack.environment.Environment"] = None


def active_environment() -> Optional["spack.environment.Environment"]:
    """Returns the active environment, if any."""
    return _active_environment
