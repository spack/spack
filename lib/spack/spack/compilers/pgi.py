# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler, get_compiler_version


class Pgi(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['pgcc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['pgc++', 'pgCC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['pgfortran', 'pgf77']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['pgfortran', 'pgf95', 'pgf90']

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'pgi/pgcc',
                  'cxx': 'pgi/pgc++',
                  'f77': 'pgi/pgfortran',
                  'fc': 'pgi/pgfortran'}

    PrgEnv = 'PrgEnv-pgi'
    PrgEnv_compiler = 'pgi'

    @property
    def openmp_flag(self):
        return "-mp"

    @property
    def cxx11_flag(self):
        return "-std=c++11"

    @property
    def pic_flag(self):
        return "-fpic"

    @classmethod
    def default_version(cls, comp):
        """The ``-V`` option works for all the PGI compilers.
        Output looks like this::

            pgcc 15.10-0 64-bit target on x86-64 Linux -tp sandybridge
            The Portland Group - PGI Compilers and Tools
            Copyright (c) 2015, NVIDIA CORPORATION.  All rights reserved.

        on x86-64, and::

            pgcc 17.4-0 linuxpower target on Linuxpower
            PGI Compilers and Tools
            Copyright (c) 2017, NVIDIA CORPORATION.  All rights reserved.

        on PowerPC.
        """
        return get_compiler_version(
            comp, '-V', r'pg[^ ]* ([0-9.]+)-[0-9]+ [^ ]+ target on ')
