# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


def check(condition, msg):
    """Raise an install error if condition is False."""
    if not condition:
        raise InstallError(msg)


class NeedsRelocation(Package):
    """A dumy package that encodes its prefix."""

    homepage = "https://www.cmake.org"
    url = "https://cmake.org/files/v3.4/cmake-3.4.3.tar.gz"

    version("0.0.0", md5="12345678qwertyuiasdfghjkzxcvbnm0")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        exe = join_path(prefix.bin, "exe")
        with open(exe, "w", encoding="utf-8") as f:
            f.write(prefix)
        set_executable(exe)

        mkdirp(prefix.lib)

        static_lib_with_prefix = join_path(prefix.lib, "static_lib_with_prefix.a")
        with open(static_lib_with_prefix, "wb") as f:
            f.write(f"!<arch>\n{prefix}".encode("utf-8"))

        static_lib_without_prefix = join_path(prefix.lib, "static_lib_without_prefix.a")
        with open(static_lib_without_prefix, "wb") as f:
            f.write(b"!<arch>\nnothing_to_relocate")
