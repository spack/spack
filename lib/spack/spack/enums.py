# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Enumerations used throughout Spack"""

import enum


class InstallRecordStatus(enum.Flag):
    """Enum flag to facilitate querying status from the DB"""

    INSTALLED = enum.auto()
    DEPRECATED = enum.auto()
    MISSING = enum.auto()
    ANY = INSTALLED | DEPRECATED | MISSING


class ConfigScopePriority(enum.IntEnum):
    """Priorities of the different kind of config scopes used by Spack"""

    DEFAULTS = 0
    CONFIG_FILES = 1
    ENVIRONMENT = 2
    CUSTOM = 3
    COMMAND_LINE = 4
    # Topmost scope reserved for internal use
    ENVIRONMENT_SPEC_GROUPS = 5


class PropagationPolicy(enum.Enum):
    """Enum to specify the behavior of a propagated dependency"""

    NONE = enum.auto()
    PREFERENCE = enum.auto()


class DeprecationSeverity(enum.IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    @classmethod
    def _missing_(cls, value):
        severity = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        if not isinstance(value, str) or value not in severity:
            raise ValueError(f"{value!r} is not a valid DeprecationSeverity")
        return cls(severity[value])


class DeprecationReason(enum.Enum):
    CVE = "cve"
    RENAME = "rename"
    UNAVAILABLE = "unavailable"
    MAINTENANCE = "maintenance"
