# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.lang

from .cray import Cray
from .darwin import Darwin
from .linux import Linux
from .test import Test
from .windows import Windows

#: List of all the platform classes known to Spack
platforms = [Cray, Darwin, Linux, Windows, Test]


@llnl.util.lang.memoized
def _host():
    """Detect and return the platform for this machine or None if detection fails."""
    for platform_cls in sorted(platforms, key=lambda plt: plt.priority):
        if platform_cls.detect():
            return platform_cls()
    return None


def _wrapper_extension():
    if str(_host()) == 'windows':
        return ".sh"
    else:
        return ""


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
