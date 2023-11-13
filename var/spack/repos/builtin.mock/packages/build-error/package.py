# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
import sys
import tempfile

import llnl.util.filesystem as fs

from spack.package import *


class BuildError(Package):
    """This package has an install method that fails in a build script."""

    homepage = "http://www.example.com/trivial_install"
    url = "http://www.unit-test-should-replace-this-url/trivial_install-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        working_dir = tempfile.mkdtemp()

        if sys.platform == "win32":
            configure = pathlib.Path(working_dir) / "configure.bat"
            configure.write_text(
                """
    @ECHO off
    ECHO checking build system type... x86_64-apple-darwin16.6.0
    ECHO checking host system type... x86_64-apple-darwin16.6.0
    ECHO checking for gcc... /Users/gamblin2/src/spack/lib/spack/env/clang/clang
    ECHO checking whether the C compiler works... yes
    ECHO checking for C compiler default output file name... a.out
    ECHO checking for suffix of executables...
    ECHO configure: error: in /path/to/some/file:
    ECHO configure: error: cannot run C compiled programs.
    EXIT /B 1
                  """
            )

        else:
            configure = pathlib.Path(working_dir) / "configure"
            configure.write_text(
                """#!/bin/sh\n
    echo 'checking build system type... x86_64-apple-darwin16.6.0'
    echo 'checking host system type... x86_64-apple-darwin16.6.0'
    echo 'checking for gcc... /Users/gamblin2/src/spack/lib/spack/env/clang/clang'
    echo 'checking whether the C compiler works... yes'
    echo 'checking for C compiler default output file name... a.out'
    echo 'checking for suffix of executables...'
    echo 'configure: error: in /path/to/some/file:'
    echo 'configure: error: cannot run C compiled programs.'
    exit 1
    """
            )
        fs.set_executable(str(configure))
        Executable(str(configure))(f"--prefix={str(self.prefix)}")
