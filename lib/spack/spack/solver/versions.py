# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import enum


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
    # lower provenance for installed git refs so concretizer prefers StandardVersion installs
    INSTALLED_GIT_VERSION = enum.auto()
    # Synthetic versions for virtual packages
    VIRTUAL_CONSTRAINT = enum.auto()
    # A runtime injected from another package (e.g. a compiler)
    RUNTIME = enum.auto()

    def __str__(self):
        return f"{self._name_.lower()}"
