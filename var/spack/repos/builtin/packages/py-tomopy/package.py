# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyTomopy(PythonPackage):
    """TomoPy is an open-source Python package for tomographic data
       processing and image reconstruction."""

    homepage = "http://tomopy.readthedocs.io/en/latest/index.html"
    url      = "https://github.com/tomopy/tomopy/archive/1.0.0.tar.gz"

    import_modules = [
        'tomopy', 'doc', 'tomopy.util', 'tomopy.sim', 'tomopy.recon',
        'tomopy.prep', 'tomopy.misc', 'tomopy.io', 'doc.demo'
    ]

    version('1.0.0', '986ac2c85a4af9ada0403b4c746d2cd4')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-pywavelets', type=('build', 'run'))
    depends_on('py-pyfftw', type=('build', 'run'))
    depends_on('py-dxchange', type=('build', 'run'))
