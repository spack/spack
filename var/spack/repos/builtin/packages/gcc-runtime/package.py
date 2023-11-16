# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from macholib import MachO, mach_o

from llnl.util import tty

from spack.package import *
from spack.util.elf import parse_elf


class GccRuntime(Package):
    """Package for GCC compiler runtime libraries"""

    homepage = "https://gcc.gnu.org"
    has_code = False

    maintainers("haampie")

    license("GPL-3.0-or-later WITH GCC-exception-3.1")

    requires("%gcc")

    LIBRARIES = [
        "asan",
        "atomic",
        "gcc_s",
        "gfortran",
        "gomp",
        "hwasan",
        "itm",
        "lsan",
        "quadmath",
        "ssp",
        "stdc++",
        "tsan",
        "ubsan",
    ]

    for v in [
        "13.2",
        "13.1",
        "12.3",
        "12.2",
        "12.1",
        "11.4",
        "11.3",
        "11.2",
        "11.1",
        "10.5",
        "10.4",
        "10.3",
        "10.2",
        "10.1",
        "9.5",
        "9.4",
        "9.3",
        "9.2",
        "9.1",
        "8.5",
        "8.4",
        "8.3",
        "8.2",
        "8.1",
        "7.5",
        "7.4",
        "7.3",
        "7.2",
        "7.1",
        "6.5",
        "6.4",
        "6.3",
        "6.2",
        "6.1",
        "5.5",
        "5.4",
        "5.3",
        "5.2",
        "5.1",
        "4.9.4",
        "4.9.3",
        "4.9.2",
        "4.9.1",
        "4.9.0",
        "4.8.5",
        "4.8.4",
        "4.8.3",
        "4.8.2",
        "4.8.1",
        "4.8.0",
        "4.7.4",
        "4.7.3",
        "4.7.2",
        "4.7.1",
        "4.7.0",
        "4.6.4",
        "4.6.3",
        "4.6.2",
        "4.6.1",
        "4.6.0",
        "4.5.4",
        "4.5.3",
        "4.5.2",
        "4.5.1",
        "4.5.0",
    ]:
        version(v)
        requires(f"%gcc@{v}", when=f"@{v}")

    def install(self, spec, prefix):
        if spec.platform in ["linux", "cray", "freebsd"]:
            libraries = self._get_libraries_elf()
        elif spec.platform == "darwin":
            libraries = self._get_libraries_macho()
        else:
            raise RuntimeError("Unsupported platform")

        mkdir(prefix.lib)

        if not libraries:
            tty.warn("Could not detect any shared GCC runtime libraries")
            return

        for path, name in libraries:
            install(path, os.path.join(prefix.lib, name))

    def _get_libraries_elf(self):
        """Get the GCC runtime libraries for ELF binaries"""
        cc = Executable(self.compiler.cc)
        lib_regex = re.compile(rb"\blib[a-z-_]+\.so\.\d+\b")
        path_and_install_name = []

        for name in self.LIBRARIES:
            # Look for the dynamic library that gcc would use to link,
            # that is with .so extension and without abi suffix.
            path = cc(f"-print-file-name=lib{name}.so", output=str).strip()

            # gcc reports an absolute path on success
            if not os.path.isabs(path):
                continue

            # Now there are two options:
            # 1. the file is an ELF file
            # 2. the file is a linker script referencing the actual library
            with open(path, "rb") as f:
                try:
                    # Try to parse as an ELF file
                    soname = parse_elf(f, dynamic_section=True).dt_soname_str.decode("utf-8")
                except Exception:
                    # On failure try to "parse" as ld script; the actual
                    # library needs to be mentioned by filename.
                    f.seek(0)
                    script_matches = lib_regex.findall(f.read())
                    if len(script_matches) != 1:
                        continue
                    soname = script_matches[0].decode("utf-8")

            # Now locate and install the runtime library
            runtime_path = cc(f"-print-file-name={soname}", output=str).strip()

            if not os.path.isabs(runtime_path):
                continue

            path_and_install_name.append((runtime_path, soname))

        return path_and_install_name

    def _get_libraries_macho(self):
        """Same as _get_libraries_elf but for Mach-O binaries"""
        cc = Executable(self.compiler.cc)
        path_and_install_name = []

        for name in self.LIBRARIES:
            if name == "gcc_s":
                # On darwin, libgcc_s is versioned and can't be linked as -lgcc_s,
                # but needs a suffix we don't know, so we parse it from the link line.
                match = re.search(
                    r"\s-l(gcc_s\.[0-9.]+)\s", cc("-xc", "-", "-shared-libgcc", "-###", error=str)
                )
                if match is None:
                    continue
                name = match.group(1)

            path = cc(f"-print-file-name=lib{name}.dylib", output=str).strip()

            if not os.path.isabs(path):
                continue

            macho = MachO.MachO(path)

            # Get the LC_ID_DYLIB load command
            for load_command, _, data in macho.headers[-1].commands:
                if load_command.cmd == mach_o.LC_ID_DYLIB:
                    # Strip off @rpath/ prefix, or even an absolute path.
                    dylib_name = os.path.basename(data.rstrip(b"\x00").decode())
                    break
            else:
                continue

            # Locate by dylib name
            runtime_path = cc(f"-print-file-name={dylib_name}", output=str).strip()

            if not os.path.isabs(runtime_path):
                continue

            path_and_install_name.append((runtime_path, dylib_name))

        return path_and_install_name

    @property
    def libs(self):
        # Currently these libs are not linkable with -l, they all have a suffix.
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])
