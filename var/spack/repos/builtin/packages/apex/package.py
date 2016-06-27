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
from spack import *
from spack.util.environment import *

class Apex(Package):
    homepage = "http://github.com/khuck/xpress-apex"
    url      = "http://github.com/khuck/xpress-apex/archive/v0.1.tar.gz"

    version('0.1', '8b95f0c0313da1575960d3ad69f18e75')

    depends_on("binutils+libiberty")
    depends_on("boost@1.54:")
    depends_on("cmake@2.8.12:")
    depends_on("activeharmony@4.5:")
    depends_on("ompt-openmp")

    def install(self, spec, prefix):

        path=get_path("PATH")
        path.remove(spec["binutils"].prefix.bin)
        path_set("PATH", path)
        with working_dir("build", create=True):
            cmake('-DBOOST_ROOT=%s' % spec['boost'].prefix,
                '-DUSE_BFD=TRUE', 
                '-DBFD_ROOT=%s' % spec['binutils'].prefix,
                '-DUSE_ACTIVEHARMONY=TRUE', 
                '-DACTIVEHARMONY_ROOT=%s' % spec['activeharmony'].prefix,
                '-DUSE_OMPT=TRUE', 
                '-DOMPT_ROOT=%s' % spec['ompt-openmp'].prefix,
                '..', *std_cmake_args)
            make()
            make("install")
