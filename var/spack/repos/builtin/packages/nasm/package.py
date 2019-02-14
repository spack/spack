# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nasm(AutotoolsPackage):
    """NASM (Netwide Assembler) is an 80x86 assembler designed for
    portability and modularity. It includes a disassembler as well."""

    homepage = "http://www.nasm.us"
    url = "https://src.fedoraproject.org/repo/pkgs/nasm/nasm-2.13.03.tar.bz2/sha512/d7a6b4cee8dfd603d8d4c976e5287b5cc542fa0b466ff989b743276a6e28114e64289bf02a7819eca63142a5278aa6eed57773007e5f589e15768e6456a8919d/nasm-2.13.03.tar.bz2"
    list_url = "http://www.nasm.us/pub/nasm/releasebuilds"
    list_depth = 1

    version('2.13.03', '0c581d482f39d5111879ca9601938f74')
    version('2.11.06', '2b958e9f5d200641e6fc9564977aecc5')

    # Fix compilation with GCC 8
    # https://bugzilla.nasm.us/show_bug.cgi?id=3392461
    patch('https://src.fedoraproject.org/rpms/nasm/raw/0cc3eb244bd971df81a7f02bc12c5ec259e1a5d6/f/0001-Remove-invalid-pure_func-qualifiers.patch', level=1, sha256='ac9f315d204afa6b99ceefa1fe46d4eed2b8a23c7315d32d33c0f378d930e950', when='@2.13.03 %gcc@8:')
~
