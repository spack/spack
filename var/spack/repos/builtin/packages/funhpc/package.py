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


class Funhpc(CMakePackage):
    """FunHPC: Functional HPC Programming"""

    homepage = "https://github.com/eschnett/FunHPC.cxx"
    url      = "https://github.com/eschnett/FunHPC.cxx/archive/version/0.1.0.tar.gz"
    git      = "https://github.com/eschnett/FunHPC.cxx.git"

    version('develop', branch='master')
    version('1.3.0', '71a1e57c4d882cdf001f29122edf7fc6')
    version('1.2.0', 'ba2bbeea3091e999b6b85eaeb1b67a83')
    version('1.1.1', '7b9ef638b02fffe35b75517e8eeff580')
    version('1.1.0', '897bd968c42cd4f14f86fcf67da70444')
    version('1.0.0', 'f34e71ccd5548b42672e692c913ba5ee')
    version('0.1.1', 'f0248710f2de88ed2a595ad40d99997c')
    version('0.1.0', '00f7dabc08ed1ab77858785ce0809f50')

    variant('pic', default=True,
            description="Produce position-independent code")

    depends_on('cereal')
    depends_on('googletest')
    depends_on('hwloc')
    depends_on('jemalloc')
    depends_on('mpi')
    depends_on('qthreads')

    def cmake_args(self):
        spec = self.spec
        options = ["-DGTEST_ROOT=%s" % spec['googletest'].prefix]
        if '+pic' in spec:
            options += ["-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true"]
        return options

    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAILURE=1")
