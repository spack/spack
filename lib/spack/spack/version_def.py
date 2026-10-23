# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Version definitions as represented on a package class."""

from typing import Dict, Optional

import spack.util.crypto as crypto
from spack.version import ConcreteVersion


class VersionDefinition:
    """Class representing a version definition.

    Includes the version and all of the arguments provided with it in its package definition.
    """

    version: ConcreteVersion
    precedence: int
    kwargs: Dict

    def __init__(self, version: ConcreteVersion, precedence: int, kwargs: Dict):
        self.version = version
        self.precedence = precedence
        self.kwargs = kwargs

    def get_checksum(self) -> Optional[str]:
        """Get the checksum for this version def, if one exists in the kwargs."""
        return next(
            (v for k, v in self.kwargs.items() if k in crypto.hashes), self.kwargs.get("checksum")
        )
