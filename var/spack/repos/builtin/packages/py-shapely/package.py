# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyShapely(PythonPackage):
    """Manipulation and analysis of geometric objects in the Cartesian plane.
    """

    homepage = "https://github.com/Toblerity/Shapely"
    url      = "https://pypi.io/packages/source/S/Shapely/Shapely-1.6.4.tar.gz"

    version('1.6.4', '7581ef2d0fb346f9ed157f3efc75f6a4')

    depends_on('python@2.6.0:2.8,3.4.0:', type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython@0.19:',   type='build')
    depends_on('py-numpy@1.4.1:',   type=('build', 'run'))
    depends_on('geos@3.3:')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GEOS_CONFIG', self.spec['geos'].prefix)
        spack_env.prepend_path('LD_LIBRARY_PATH', self.spec['geos'].prefix.lib)
