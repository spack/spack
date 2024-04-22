# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform as py_platform
import re
import shlex
from typing import Optional

from spack.version import StandardVersion

from ._operating_system import OperatingSystem


def kernel_version() -> StandardVersion:
    """Return the kernel version."""
    # Strip '+' characters just in case we're running a version built from git/etc
    return StandardVersion.from_string(re.sub(r"\+", r"", py_platform.release()))


def _parse_os_release(contents: str) -> Optional[str]:
    for expression in shlex.split(contents, posix=True):
        if "=" not in expression:
            continue
        name, value = expression.split("=", 1)
        if name.lower() != "id":
            continue
        value = value.lower().replace(" ", "_")
        if value:
            return value
    return None


def _detect_distro() -> Optional[str]:
    try:
        with open("/etc/os-release") as f:
            return _parse_os_release(f.read())
    except OSError:
        return None


class LinuxDistro(OperatingSystem):
    """Detect the Linux distro name"""

    def __init__(self):
        super().__init__(_detect_distro() or "unknown", "")
