##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from spack.compiler import *

class Pgi(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['pgcc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['pgCC']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['pgf77']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['pgf95', 'pgf90']

    # Named wrapper links within spack.build_env_path
    link_paths = { 'cc'  : 'pgi/pgcc',
                   'cxx' : 'pgi/case-insensitive/pgCC',
                   'f77' : 'pgi/pgf77',
                   'fc'  : 'pgi/pgf90' }

    @classmethod
    def default_version(cls, comp):
        """The '-V' option works for all the PGI compilers.
           Output looks like this::

               pgf95 10.2-0 64-bit target on x86-64 Linux -tp nehalem-64
               Copyright 1989-2000, The Portland Group, Inc.  All Rights Reserved.
               Copyright 2000-2010, STMicroelectronics, Inc.  All Rights Reserved.
        """
        return get_compiler_version(
            comp, '-V', r'pg[^ ]* ([^ ]+) \d\d\d?-bit target')

