# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack import *

class BisonWin(Package):
    """Bison is a general-purpose parser generator that converts
    an annotated context-free grammar into a deterministic LR or
    generalized LR (GLR) parser employing LALR(1) parser tables."""

    homepage = "https://github.com/lexxmark/winflexbison#readme"
    url = "https://github.com/lexxmark/winflexbison/archive/v2.5.25.tar.gz"

    executables = ['^bison$']

    version('3.8.2', sha256='06c9e13bdf7eb24d4ceb6b59205a4f67c2c7e7213119644430fe82fbd14a0abb')
    version('3.7.4', sha256='fbabc7359ccd8b4b36d47bfe37ebbce44805c052526d5558b95eda125d1677e2')
    version('3.7.1', sha256='1dd952839cf0d5a8178c691eeae40dc48fa50d18dcce648b1ad9ae0195367d13')
    version('3.5',   sha256='0b36200b9868ee289b78cefd1199496b02b76899bbb7e84ff1c0733a991313d1')
    version('3.4.1', sha256='7007fc89c216fbfaff5525359b02a7e5b612694df5168c74673f67055f015095')
    version('3.3.2', sha256='0fda1d034185397430eb7b0c9e140fb37e02fbfc53b90252fa5575e382b6dbd1')
    version('3.3.1', sha256='60DAAF23F47673C349D6AB6421FE3E05B1FA3DBA6EA4B65A37883D186C4975C2')
    version('3.1',   sha256='')
    version('3.0.5', sha256='cd399d2bee33afa712bac4b1f4434e20379e9b4099bce47189e09a7675a2d566')
    version('3.0.4', sha256='b67fd2daae7a64b5ba862c66c07c1addb9e6b1b05c5f2049392cfd8a2172952e')
    version('2.7',   sha256='19bbe7374fd602f7a6654c131c21a15aebdc06cc89493e8ff250cb7f9ed0a831')

    provides('bison', when="platform=windows")

    build_directory = 'spack-build'
    cmake_dir = os.path.join(build_directory, 'CMakeBuild')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'bison \(GNU Bison\)\s+(\S+)', output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        """ Override url_for_version so that we can
        have an opaque alias for winflexbison versions
        that match standard bison versions
        """
        win_ver_map = {
            "3.8.2": "2.5.25",
            "3.7.4": "2.5.24",
            "3.7.1": "2.5.23",
            "3.5"  : "2.5.22",
            "3.4.1": "2.5.21",
            "3.3.2": "2.5.18",
            "3.3.1": "2.5.17",
            "3.1"  : "2.5.16",
            "3.0.5": "2.5.15",
            "3.0.4": "2.5.14",
            "2.7"  : "2.4.12"
        }
        return "https://github.com/lexxmark/winflexbison/archive/refs/tags/v{}.tar.gz".format(win_ver_map[str(version)])

    def configure(self, spec, prefix):
        """
        For this command rather than relying on a fragile system of guessing
        which instance of Visual Studio the current MSVC compiler is associated with,
        we manually call CMake here to avoid WinFlexBison's build batch script's explicit invocation
        of the generator. This allows CMake to lean on Spack's behind the scenes invocation
        of the VCVARS, and default to the proper Windows Visual Studio Makefiles
        """
        with working_dir(self.cmake_dir, create=True):
            cmake('-DCMAKE_INSTALL_PREFIX={}'.format(prefix), '..')

    def build(self, spec, prefix):
        """
        As we eschewed the use of the provided batch builder, we must continue to mimic it's contents here
        """
        with working_dir(self.cmake_dir):
            cmake('--build', '.', '--config', 'Release')

    def install(self, spec, prefix):
        """
        As we eschewed the use of the provided batch builder, we must continue to mimic it's contents here
        """
        with working_dir(self.cmake_dir):
            cmake('--build', '.', '--target', 'install')
