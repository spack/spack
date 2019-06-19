# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nasm(AutotoolsPackage):
    """NASM (Netwide Assembler) is an 80x86 assembler designed for
    portability and modularity. It includes a disassembler as well."""

    homepage = "https://www.nasm.us"
    url      = "https://www.nasm.us/pub/nasm/releasebuilds/2.14.02/nasm-2.14.02.tar.xz"
    list_url = "https://www.nasm.us/pub/nasm/releasebuilds"
    list_depth = 1

    version('2.14.02', sha256='e24ade3e928f7253aa8c14aa44726d1edf3f98643f87c9d72ec1df44b26be8f5')
    version('2.13.03', 'd5ca2ad7121ccbae69dd606b1038532c')
    version('2.11.06', '2b958e9f5d200641e6fc9564977aecc5')

    # Fix compilation with GCC 8
    # https://bugzilla.nasm.us/show_bug.cgi?id=3392461
    patch('https://src.fedoraproject.org/rpms/nasm/raw/0cc3eb244bd971df81a7f02bc12c5ec259e1a5d6/f/0001-Remove-invalid-pure_func-qualifiers.patch', level=1, sha256='ac9f315d204afa6b99ceefa1fe46d4eed2b8a23c7315d32d33c0f378d930e950', when='@2.13.03 %gcc@8:')
