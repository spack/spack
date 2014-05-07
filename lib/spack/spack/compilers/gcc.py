##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack.compiler import Compiler

class Gcc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['gcc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['g++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['gfortran']

    # Subclasses use possible names of Fortran 90 compiler
    f90_names = ['gfortran']

    def __init__(self, cc, cxx, f77, f90):
        super(Gcc, self).__init__(cc, cxx, f77, f90)
