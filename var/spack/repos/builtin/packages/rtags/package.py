# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rtags(CMakePackage):
    """RTags is a client/server application that indexes C/C++ code"""

    homepage = "https://github.com/Andersbakken/rtags/"
    url      = "https://andersbakken.github.io/rtags-releases/rtags-2.17.tar.gz"

    version('2.17', '95b24d7729678645a027d83be114d624')
    # version('2.12', '84988aaff27915a79d4b4b57299f9a51')  # no available

    depends_on("llvm@3.3: +clang")
    depends_on("zlib")
    depends_on("openssl")
    depends_on("lua@5.3:")
    depends_on("bash-completion")
    depends_on("pkgconfig", type='build')

    patch("add_string_iterator_erase_compile_check.patch", when='@2.12')

    def cmake_args(self):
        args = ['-DCMAKE_EXPORT_COMPILE_COMMANDS=1',
                '-DRTAGS_NO_ELISP_FILES=1',
                ]
        return args
