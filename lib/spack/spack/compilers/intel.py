##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
from spack.compiler import *
import llnl.util.tty as tty
from spack.version import ver


class Intel(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['icc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['icpc']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['ifort']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['ifort']

    # Named wrapper links within spack.build_env_path
    link_paths = {'cc': 'intel/icc',
                  'cxx': 'intel/icpc',
                  'f77': 'intel/ifort',
                  'fc': 'intel/ifort'}

    PrgEnv = 'PrgEnv-intel'
    PrgEnv_compiler = 'intel'

    @property
    def openmp_flag(self):
        if self.version < ver('16.0'):
            return "-openmp"
        else:
            return "-qopenmp"

    @property
    def cxx11_flag(self):
        if self.version < ver('11.1'):
            tty.die("Only intel 11.1 and above support c++11.")
        elif self.version < ver('13'):
            return "-std=c++0x"
        else:
            return "-std=c++11"

    @property
    def pic_flag(self):
        return "-fPIC"

    @classmethod
    def default_version(cls, comp):
        """The '--version' option seems to be the most consistent one
        for intel compilers.  Output looks like this::

            icpc (ICC) 12.1.5 20120612
            Copyright (C) 1985-2012 Intel Corporation.  All rights reserved.

        or::

            ifort (IFORT) 12.1.5 20120612
            Copyright (C) 1985-2012 Intel Corporation.  All rights reserved.
        """
        return get_compiler_version(
            comp, '--version', r'\((?:IFORT|ICC)\) ([^ ]+)')

    @property
    def stdcxx_libs(self):
        return ('-cxxlib', )
