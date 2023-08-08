# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import platform as py_platform
import re
import sys
from subprocess import PIPE, run
from typing import Optional, Tuple

import spack.util.elf
from spack.version import StandardVersion, Version

from ._operating_system import OperatingSystem


def kernel_version():
    """Return the kernel version as a Version object.
    Note that the kernel version is distinct from OS and/or
    distribution versions. For instance:
    >>> distro.id()
    'centos'
    >>> distro.version()
    '7'
    >>> platform.release()
    '5.10.84+'
    """
    # Strip '+' characters just in case we're running a
    # version built from git/etc
    clean_version = re.sub(r"\+", r"", py_platform.release())
    return Version(clean_version)


def _confstr() -> Optional[Tuple[str, StandardVersion]]:
    """On glibc the version is available in the CS_GNU_LIBC_VERSION,
    this is a runtime, not compile-time constant, so should be fast
    and correct."""
    try:
        result = os.confstr("CS_GNU_LIBC_VERSION")
        if not result:
            return None
        name, version_str = result.split(maxsplit=1)
        version = StandardVersion.from_string(version_str)
    except Exception:
        return None

    if name != "glibc":
        return None

    return name, version


def _dynamic_linker() -> Optional[Tuple[str, StandardVersion]]:
    """On musl libc the dynamic linker is executable and can dump
    its version. We retrieve the dynamic linker from the current
    Python interpreter."""
    try:
        with open(sys.executable, "rb") as f:
            elf = spack.util.elf.parse_elf(f, interpreter=True)
    except (OSError, spack.util.elf.ElfParsingError):
        return None

    # Statically linked Python
    if not elf.has_pt_interp:
        return None

    dynamic_linker_path = elf.pt_interp_str.decode("utf-8")

    # Not musl
    if "ld-musl" not in os.path.basename(dynamic_linker_path):
        return None

    try:
        output = run([dynamic_linker_path], check=False, stdout=PIPE, stderr=PIPE).stderr.decode(
            "utf-8"
        )
    except Exception:
        return None
    return _parse_musl_output(output)


def _ldd() -> Optional[Tuple[str, StandardVersion]]:
    """Try to derive the libc version from the output of ldd."""
    # It would be slightly better to parse the verdef section of libc.so
    # for glibc, but that requires locating the library. Instead we just
    # rely on ldd being in PATH and hope it's the right one.
    try:
        output = run(["ldd", "--version"], check=False, stdout=PIPE, stderr=PIPE)
        stdout = output.stdout.decode("utf-8")
        stderr = output.stderr.decode("utf-8")
    except Exception:
        return None

    # musl libc prints to stderr, returns with error code
    if stderr.startswith("musl"):
        return _parse_musl_output(stderr)

    # Otherwise, glibc.
    if not re.search("gnu|glibc", stdout, re.IGNORECASE):
        return None

    version_str = re.match(r".+\(.+\) (.+)", stdout)
    if not version_str:
        return None
    try:
        version = StandardVersion.from_string(version_str.group(1))
        return "glibc", version
    except Exception:
        return None


def _parse_musl_output(output: str) -> Optional[Tuple[str, StandardVersion]]:
    version_str = re.search(r"^Version (.+)$", output, re.MULTILINE)
    if not version_str:
        return None
    try:
        return "musl", StandardVersion.from_string(version_str.group(1))
    except Exception:
        return None


def _distro() -> Optional[Tuple[str, StandardVersion]]:
    """Last resort is to use the distro module, which actually
    figures out the distribution name and version, instead of
    the libc flavor. This is a fallback in case the other methods
    fail, and it's also the slowest, since it may call lsb_release,
    which is a Python script on some distros, so the startup cost
    of another Python interpreter is paid."""
    try:
        # This will throw an error if imported on a non-Linux platform.
        import distro

        distname: str = distro.id()
        version_str: str = distro.version()
    except ImportError:
        return None

    # Grabs major version from tuple on redhat; on other platforms
    # grab the first legal identifier in the version field.  On
    # debian you get things like 'wheezy/sid'; sid means unstable.
    # We just record 'wheezy' and don't get quite so detailed.
    components = re.split(r"[^\w-]", version_str)

    if "ubuntu" in distname:
        version_str = ".".join(components[0:2])
    else:
        version_str = components[0]

    try:
        version = StandardVersion.from_string(version_str)
    except Exception:
        return None

    return distname, version


class LinuxDistro(OperatingSystem):
    """This class will represent the autodetected operating system
    for a Linux System. Since there are many different flavors of
    Linux, this class will attempt to encompass them all through
    autodetection using the python module platform and the method
    platform.dist()
    """

    def __init__(self):
        for f in (_confstr, _dynamic_linker, _ldd, _distro):
            result = f()
            if result:
                super().__init__(*result)
                return

        super().__init__("unknown", "")
