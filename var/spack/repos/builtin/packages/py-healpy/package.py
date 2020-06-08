# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHealpy(PythonPackage):
    """healpy is a Python package to handle pixelated data on the sphere."""

    homepage = "https://github.com/healpy/healpy"
    url      = "https://github.com/healpy/healpy/archive/1.12.10.tar.gz"

    version('1.12.10', sha256='8576cc3240f1da3ba8428699c3231d8e24dd86a754c36b0a12cb087ac5793d69')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))
    depends_on('py-pip')
    depends_on('py-wheel')
    depends_on('py-numpy')
    depends_on('py-matplotlib')
    depends_on('py-astropy')
    depends_on('cfitsio')
    depends_on('healpix-cxx')

    # def build_args(self, spec, prefix):
    #     # FIXME: Add arguments other than --prefix
    #     # FIXME: If not needed delete this function
    #     args = []
    #     return args
