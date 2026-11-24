# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module implements Version and version-ish objects. These are:

* :class:`~spack.version.version_types.StandardVersion`: A single version of a package.
* :class:`~spack.version.version_types.ClosedOpenRange`: A range of versions of a package.
* :class:`~spack.version.version_types.VersionList`: A ordered list of Version and VersionRange
  elements.
"""

from .common import (
    EmptyRangeError,
    VersionChecksumError,
    VersionError,
    VersionLookupError,
    infinity_versions,
    is_git_commit_sha,
    is_git_version,
)
from .version_types import (
    ClosedOpenRange,
    ConcreteVersion,
    GitVersion,
    StandardVersion,
    Version,
    VersionList,
    VersionRange,
    VersionType,
    _next_version,
    _prev_version,
    from_string,
    ver,
)

#: This version contains all possible versions.
any_version: VersionList = VersionList([":"])

__all__ = [
    "ClosedOpenRange",
    "ConcreteVersion",
    "EmptyRangeError",
    "GitVersion",
    "StandardVersion",
    "Version",
    "VersionChecksumError",
    "VersionError",
    "VersionList",
    "VersionLookupError",
    "VersionRange",
    "VersionType",
    "_next_version",
    "_prev_version",
    "any_version",
    "from_string",
    "infinity_versions",
    "is_git_commit_sha",
    "is_git_version",
    "ver",
]
