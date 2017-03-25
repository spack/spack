##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
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


class PyRtree(PythonPackage):
    """Python interface to the RTREE.4 Library."""
    homepage = "http://toblerity.org/rtree/"
    url      = "https://github.com/Toblerity/rtree/tarball/0.8.2"

    # Not an official release yet.  But changes in here are required
    # to work with Spack.  As it does with all packages, Spack
    # installs libspatialindex in a non-system location.  Without the
    # changes in this fork, py-rtree requires an environment variables
    # to be set *at runtime*, in order to find libspatialindex.  That
    # is not feasible within the Spack worldview.
    version('0.8.2.2', 'b1fe96a73153db49ea6ce45a063d82cb',
        url='https://github.com/citibeth/rtree/tarball/95a678cc7350857a1bb631bc41254efcd1fc0a0d')

    version('0.8.2.1', '394696ca849dd9f3a5ef24fb02a41ef4',
        url='https://github.com/citibeth/rtree/tarball/3a87d86f66a3955676b2507d3bf424ade938a22b')

    # Does not work with Spack
    # version('0.8.2', '593c7ac6babc397b8ba58f1636c1e0a0')

    depends_on('py-setuptools', type='build')
    depends_on('libspatialindex')

    def setup_environment(self, spack_env, run_env):
        lib = self.spec['libspatialindex'].prefix.lib
        spack_env.set('SPATIALINDEX_LIBRARY',
                      join_path(lib, 'libspatialindex.%s'   % dso_suffix))
        spack_env.set('SPATIALINDEX_C_LIBRARY',
                      join_path(lib, 'libspatialindex_c.%s' % dso_suffix))
