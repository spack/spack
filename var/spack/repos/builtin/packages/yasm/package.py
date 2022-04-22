# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat

from llnl.util.filesystem import chmod_x

from spack import *


class Yasm(AutotoolsPackage):
    """Yasm is a complete rewrite of the NASM-2.11.06 assembler. It
       supports the x86 and AMD64 instruction sets, accepts NASM and
       GAS assembler syntaxes and outputs binary, ELF32 and ELF64
       object formats."""

    homepage = "https://yasm.tortall.net"
    url      = "https://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz"
    git      = "https://github.com/yasm/yasm.git"

    version('develop', branch='master')
    version('1.3.0', sha256='3dce6601b495f5b3d45b59f7d2492a340ee7e84b5beca17e48f862502bd5603f')

    depends_on('autoconf', when='@develop')
    depends_on('automake', when='@develop')
    depends_on('libtool', when='@develop')
    depends_on('m4', when='@develop')

    @run_after('configure')
    def make_genversion_executable(self):
        with working_dir(self.stage.source_path):
            st = os.stat('./genversion')
            chmod_x('genversion', st.st_mode | stat.S_IXUSR)
