# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib

from ._functions import _host, by_name, platforms, prevent_cray_detection, reset
from ._platform import Platform
from .cray import Cray
from .darwin import Darwin
from .linux import Linux
from .test import Test
from .windows import Windows

__all__ = [
    'Platform',
    'Cray',
    'Darwin',
    'Linux',
    'Test',
    'Windows',
    'platforms',
    'host',
    'by_name',
    'reset',
    'prevent_cray_detection'
]

#: The "real" platform of the host running Spack. This should not be changed
#: by any method and is here as a convenient way to refer to the host platform.
real_host = _host

#: The current platform used by Spack. May be swapped by the use_platform
#: context manager.
host = _host


class _PickleableCallable(object):
    """Class used to pickle a callable that may substitute either
    _platform or _all_platforms. Lambda or nested functions are
    not pickleable.
    """
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self):
        return self.return_value


@contextlib.contextmanager
def use_platform(new_platform):
    global host

    import spack.compilers
    import spack.config

    msg = '"{0}" must be an instance of Platform'
    assert isinstance(new_platform, Platform), msg.format(new_platform)

    original_host_fn = host

    try:
        host = _PickleableCallable(new_platform)

        # Clear configuration and compiler caches
        spack.config.config.clear_caches()
        spack.compilers._cache_config_files = []

        yield new_platform

    finally:
        host = original_host_fn

        # Clear configuration and compiler caches
        spack.config.config.clear_caches()
        spack.compilers._cache_config_files = []
