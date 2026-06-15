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


class Context(enum.Enum):
    """Enum used to indicate the context in which an environment has to be setup: build,
    run or test."""

    BUILD = 1
    RUN = 2
    TEST = 3

    def __str__(self):
        return ("build", "run", "test")[self.value - 1]

    @classmethod
    def from_string(cls, s: str):
        if s == "build":
            return Context.BUILD
        elif s == "run":
            return Context.RUN
        elif s == "test":
            return Context.TEST
        raise ValueError(f"context should be one of 'build', 'run', 'test', got {s}")
