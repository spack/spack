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
from spack import *


class Gperftools(AutotoolsPackage):
    """Google's fast malloc/free implementation, especially for
       multi-threaded applications.  Contains tcmalloc, heap-checker,
       heap-profiler, and cpu-profiler.

    """
    homepage = "https://github.com/gperftools/gperftools"
    url      = "https://github.com/gperftools/gperftools/releases/download/gperftools-2.7/gperftools-2.7.tar.gz"

    version('2.7', '1ee8c8699a0eff6b6a203e59b43330536b22bbcbe6448f54c7091e5efb0763c9')
    version('2.4', '982a37226eb42f40714e26b8076815d5ea677a422fb52ff8bfca3704d9c30a2d')
    version('2.3', '093452ad45d639093c144b4ec732a3417e8ee1f3744f2b0f8d45c996223385ce')

    depends_on("unwind")
