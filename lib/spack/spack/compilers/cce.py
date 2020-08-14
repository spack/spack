# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.compiler


class Cce(spack.compiler.Compiler):
    """Cray compiler environment compiler."""
    link_paths = {'cc': 'cce/cc',
                  'cxx': 'cce/case-insensitive/CC',
                  'f77': 'cce/ftn',
                  'fc': 'cce/ftn'}

    version_argument = '--version'
    verbose_flag = '-v'
    debug_flags = ['-g', '-G0', '-G1', '-G2', '-Gfast']
    openmp_flag = '-fopenmp'

    cxx11_flag = '-std=c++11'
    c99_flag   = '-std=c99'
    c11_flag   = '-std=c11'

    cc_pic_flag  = '-fPIC'
    cxx_pic_flag = '-fPIC'
    f77_pic_flag = '-fPIC'
    fc_pic_flag  = '-fPIC'
