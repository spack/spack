# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
