# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import ver


class CceClassic(Compiler):
    """Cray compiler environment compiler."""
    # MacPorts builds gcc versions with prefixes and -mp-X.Y suffixes.
    link_paths = {'cc': 'cce/cc',
                  'cxx': 'cce/case-insensitive/CC',
                  'f77': 'cce/ftn',
                  'fc': 'cce/ftn'}

    version_argument = '-V'
    verbose_flag = '-v'
    debug_flags = ['-g', '-G0', '-G1', '-G2', '-Gfast']
    openmp_flag = '-h omp'

    cxx11_flag = '-h std=c++11'

    @property
    def c99_flag(self):
        if self.version >= ver('8.4'):
            return '-h std=c99,noconform,gnu'
        elif self.version >= ver('8.1'):
            return '-h c99,noconform,gnu'
        raise UnsupportedCompilerFlag(
            self, 'the C99 standard', 'c99_flag', '< 8.1'
        )

    @property
    def c11_flag(self):
        if self.version >= ver('8.5'):
            return '-h std=c11,noconform,gnu'
        raise UnsupportedCompilerFlag(
            self, 'the C11 standard', 'c11_flag', '< 8.5'
        )

    cc_pic_flag = '-h PIC'
    cxx_pic_flag = '-h PIC'
    f77_pic_flag = '-h PIC'
    fc_pic_flag = '-h PIC'
