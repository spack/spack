# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyShapely(PythonPackage):
    """Manipulation and analysis of geometric objects in the Cartesian plane.
    """

    homepage = "https://github.com/Toblerity/Shapely"
    url      = "https://pypi.io/packages/source/S/Shapely/Shapely-1.6.4.post2.tar.gz"

    maintainers = ['adamjstewart']
    import_modules = [
        'shapely', 'shapely.geometry', 'shapely.algorithms',
        'shapely.examples', 'shapely.speedups', 'shapely.vectorized',
    ]

    version('1.6.4.post2', sha256='c4b87bb61fc3de59fc1f85e71a79b0c709dc68364d9584473697aad4aa13240f')
    version('1.6.4', sha256='b10bc4199cfefcf1c0e5d932eac89369550320ca4bdf40559328d85f1ca4f655')

    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('geos')
    depends_on('geos@3.3:', when='@1.3:')
    depends_on('py-pytest', type='test')

    def setup_build_environment(self, env):
        env.set('GEOS_CONFIG',
                join_path(self.spec['geos'].prefix.bin, 'geos-config'))
