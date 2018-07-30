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


class PyRtree(PythonPackage):
    """Python interface to the RTREE.4 Library."""
    homepage = "http://toblerity.org/rtree/"
    url      = "https://pypi.io/packages/source/R/Rtree/Rtree-0.8.3.tar.gz"

    version('0.8.3', 'a27cb05a85eed0a3605c45ebccc432f8')

    depends_on('py-setuptools', type='build')
    depends_on('libspatialindex')

    def setup_environment(self, spack_env, run_env):
        lib = self.spec['libspatialindex'].prefix.lib
        spack_env.set('SPATIALINDEX_LIBRARY',
                      join_path(lib, 'libspatialindex.%s'   % dso_suffix))
        spack_env.set('SPATIALINDEX_C_LIBRARY',
                      join_path(lib, 'libspatialindex_c.%s' % dso_suffix))
