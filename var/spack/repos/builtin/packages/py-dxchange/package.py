# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyDxchange(PythonPackage):
    """DXchange provides an interface with tomoPy and raw tomographic data
       collected at different synchrotron facilities."""

    homepage = "https://github.com/data-exchange/dxchange"
    url      = "https://github.com/data-exchange/dxchange/archive/v0.1.2.tar.gz"

    version('0.1.6', sha256='8ce7c1ce3bdb483f285ba7483657691907e93c57c85067fe7bfa5756c2fc429f')
    version('0.1.5', sha256='023652ac8f29cf486bbcc0112d980b255c1b7b3d5e23e555b7e4b7e373117387')
    version('0.1.4', sha256='995d510956632adf6161dd45224c38319123c1341b6acbed3c8c3d43f9fb6a06')
    version('0.1.3', sha256='252be2283878384b59a23482eab870f51d63b9205d34e26e4f319d2bced90519')
    version('0.1.2', sha256='d005b036b6323d0dffd5944c3da0b8a90496d96277654e72b53717058dd5fd87')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
    depends_on('py-spefile', type=('build', 'run'))
    depends_on('py-edffile', type=('build', 'run'))
    depends_on('py-tifffile', type=('build', 'run'))
    depends_on('py-dxfile', type=('build', 'run'))
    depends_on('py-olefile', type=('build', 'run'))
    depends_on('py-astropy', type=('build', 'run'))
