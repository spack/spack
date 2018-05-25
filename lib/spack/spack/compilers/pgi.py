##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
