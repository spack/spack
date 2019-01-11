# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAstropy(PythonPackage):
    """The Astropy Project is a community effort to develop a single core
    package for Astronomy in Python and foster interoperability between
    Python astronomy packages."""

    homepage = 'http://www.astropy.org/'
    url = 'https://pypi.io/packages/source/a/astropy/astropy-1.1.2.tar.gz'

    version('1.1.2',     'cbe32023b5b1177d1e2498a0d00cda51')
    version('1.1.post1', 'b52919f657a37d45cc45f5cb0f58c44d')

    # Required dependencies
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    # Optional dependencies
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-beautifulsoup4', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('libxml2')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pytz', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-markupsafe', type=('build', 'run'))

    # System dependencies
    depends_on('cfitsio')
    depends_on('expat')

    def build_args(self, spec, prefix):
        return ['--use-system-cfitsio', '--use-system-expat']
