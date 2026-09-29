# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import contextlib
from typing import Callable, List

from ._functions import _host, by_name, platforms, reset
from ._platform import Platform
from .darwin import Darwin
from .freebsd import FreeBSD
from .linux import Linux
from .test import Test
from .windows import Windows

__all__ = [
    "Platform",
    "Darwin",
    "Linux",
    "FreeBSD",
    "Test",
    "Windows",
    "platforms",
    "host",
    "by_name",
    "reset",
    "using_libc_compatibility",
]

#: The "real" platform of the host running Spack. This should not be changed
#: by any method and is here as a convenient way to refer to the host platform.
real_host = _host

#: The current platform used by Spack. May be swapped by the use_platform
#: context manager.
host: Callable[[], Platform] = _host

#: Callbacks invoked when the current platform changes through the use_platform context manager.
#: Higher-level modules that cache host-dependent state (e.g. spack.config) register a callback
#: here to invalidate it.
on_host_changed: List[Callable[[], None]] = []


class _PickleableCallable:
    """Class used to pickle a callable that may substitute either
    _platform or _all_platforms. Lambda or nested functions are
    not pickleable.
    """

    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self):
        return self.return_value


def using_libc_compatibility() -> bool:
    """Returns True if we are using libc compatibility on this platform."""
    return host().name == "linux"


@contextlib.contextmanager
def use_platform(new_platform):
    global host

    assert isinstance(new_platform, Platform), f'"{new_platform}" must be an instance of Platform'

    original_host_fn = host

    try:
        host = _PickleableCallable(new_platform)
        for callback in on_host_changed:
            callback()
        yield new_platform

    finally:
        host = original_host_fn
        for callback in on_host_changed:
            callback()
