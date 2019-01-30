# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Yasm(AutotoolsPackage):
    """Yasm is a complete rewrite of the NASM-2.11.06 assembler. It
       supports the x86 and AMD64 instruction sets, accepts NASM and
       GAS assembler syntaxes and outputs binary, ELF32 and ELF64
       object formats."""

    homepage = "http://yasm.tortall.net"
    url      = "http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz"
    git      = "https://github.com/yasm/yasm.git"

    version('develop', branch='master')
    version('1.3.0', 'fc9e586751ff789b34b1f21d572d96af')

    depends_on('autoconf', when='@develop')
    depends_on('automake', when='@develop')
    depends_on('libtool', when='@develop')
    depends_on('m4', when='@develop')
