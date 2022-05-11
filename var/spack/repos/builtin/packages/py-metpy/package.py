# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetpy(PythonPackage):
    """Collection of tools for reading, visualizing and performing calculations
    with weather data."""

    homepage = "https://github.com/Unidata/MetPy"
    pypi     = "MetPy/MetPy-1.0.1.tar.gz"
    maintainers = ['dopplershift']

    # Importing 'metpy.io' results in downloads, so skip it.
    # https://github.com/Unidata/MetPy/issues/1888
    import_modules = ['metpy', 'metpy._vendor', 'metpy.calc', 'metpy.interpolate']

    version('1.0.1', sha256='16fa9806facc24f31f454b898741ec5639a72ba9d4ff8a19ad0e94629d93cb95')
    version('1.0', sha256='11b043aaa4e3d35db319e96bb9967eb9f73da653e155bca2d62f838108b100dc',
            deprecated=True)

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-importlib-metadata@1.0.0:', when='^python@:3.7', type=('build', 'run'))
    depends_on('py-importlib-resources@1.3.0:', when='^python@:3.8', type=('build', 'run'))
    depends_on('py-matplotlib@2.1.0:', type=('build', 'run'))
    depends_on('py-numpy@1.16.0:', type=('build', 'run'))
    depends_on('py-pandas@0.22.0:', when='@1.0', type=('build', 'run'))
    depends_on('py-pandas@0.24.0:', when='@1.0.1', type=('build', 'run'))
    depends_on('py-pint@0.10.1:', type=('build', 'run'))
    depends_on('py-pooch@0.1:', type=('build', 'run'))
    depends_on('py-pyproj@2.3.0:', type=('build', 'run'))
    depends_on('py-scipy@1.0:', type=('build', 'run'))
    depends_on('py-traitlets@4.3.0:', type=('build', 'run'))
    depends_on('py-xarray@0.14.1:', type=('build', 'run'))
