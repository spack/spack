# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.lang

from ._platform import Platform
from .cray import Cray
from .darwin import Darwin
from .linux import Linux
from .test import Test

__all__ = [
    'Platform',
    'Cray',
    'Darwin',
    'Linux',
    'Test'
]

#: List of all the platform classes known to Spack
platforms = [Cray, Darwin, Linux, Test]


def host():
    """Detect and return the platform for this machine or None if detection fails."""
    for platform_cls in sorted(platforms, key=lambda plt: plt.priority):
        if platform_cls.detect():
            return platform_cls()
    return None


@llnl.util.lang.memoized
def cls_by_name(name):
    """Return a platform class that corresponds to the given name or None
    if there is no match.

    Args:
        name (str): name of the platform
    """
    for platform_cls in sorted(platforms, key=lambda plt: plt.priority):
        if name.replace("_", "").lower() == platform_cls.__name__.lower():
            return platform_cls
    return None


def by_name(name):
    """Return a platform object that corresponds to the given name or None
    if there is no match.

    Args:
        name (str): name of the platform
    """
    platform_cls = cls_by_name(name)
    return platform_cls() if platform_cls else None
