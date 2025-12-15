# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import enum
from typing import NamedTuple, Tuple, Union

from spack.version import GitVersion, StandardVersion


def concretization_version_order(version_info: Tuple[Union[GitVersion, StandardVersion], dict]):
    """Version order key for concretization, where preferred > not preferred,
    not deprecated > deprecated, finite > any infinite component; only if all are
    the same, do we use default version ordering."""
    version, info = version_info
    return (
        info.get("preferred", False),
        not info.get("deprecated", False),
        not version.isdevelop(),
        not version.is_prerelease(),
        version,
    )


class Provenance(enum.IntEnum):
    """Enumeration of the possible provenances of a version."""

    # A spec literal
    SPEC = enum.auto()
    # A dev spec literal
    DEV_SPEC = enum.auto()
    # The 'packages' section of the configuration
    PACKAGES_YAML = enum.auto()
    # A package requirement
    PACKAGE_REQUIREMENT = enum.auto()
    # A 'package.py' file
    PACKAGE_PY = enum.auto()
    # An installed spec
    INSTALLED = enum.auto()
    # An external spec declaration
    EXTERNAL = enum.auto()
    # lower provenance for installed git refs so concretizer prefers StandardVersion installs
    INSTALLED_GIT_VERSION = enum.auto()
    # A runtime injected from another package (e.g. a compiler)
    RUNTIME = enum.auto()

    def __str__(self):
        return f"{self._name_.lower()}"


class DeclaredVersion(NamedTuple):
    """Data class to contain information on declared versions used in the solve"""

    #: String representation of the version
    version: str
    #: Unique index assigned to this version
    idx: int
    #: Provenance of the version
    origin: Provenance
