# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PyBasemap(PythonPackage):
    """The matplotlib basemap toolkit is a library for plotting
    2D data on maps in Python."""

    homepage = "http://matplotlib.org/basemap/"

    version('1.2.0', 'f8e64bd150590223701a48d60408e939')
    version('1.0.7', '48c0557ced9e2c6e440b28b3caff2de8')

    # Per Github issue #3813, setuptools is required at runtime in order
    # to make mpl_toolkits a namespace package that can span multiple
    # directories (i.e., matplotlib and basemap)
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pyproj@:1.99', type=('build', 'run'), when='@:1.2.0')
    depends_on('py-pyproj', type=('build', 'run'))
    depends_on('py-pyshp', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('geos')

    def url_for_version(self, version):
        if version >= Version('1.2.0'):
            return 'https://github.com/matplotlib/basemap/archive/v{0}rel.tar.gz'.format(version)
        else:
            return 'https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-{0}/basemap-{0}.tar.gz'.format(version)

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GEOS_DIR', self.spec['geos'].prefix)

    def install(self, spec, prefix):
        """Install everything from build directory."""
        args = self.install_args(spec, prefix)

        self.setup_py('install', *args)

        # namespace packages should not create an __init__.py file. This has
        # been reported to the basemap project in
        # https://github.com/matplotlib/basemap/issues/456
        for root, dirs, files in os.walk(spec.prefix.lib):
            for filename in files:
                if (filename == '__init__.py' and
                    os.path.basename(root) == 'mpl_toolkits'):
                    os.remove(os.path.join(root, filename))
