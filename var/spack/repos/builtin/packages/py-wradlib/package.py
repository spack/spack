# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWradlib(PythonPackage):
    """wradlib is designed to assist you in the most important steps of
    processing weather radar data. These may include: reading common data
    formats, georeferencing, converting reflectivity to rainfall intensity,
    identifying and correcting typical error sources (such as clutter or
    attenuation) and visualising the data."""

    homepage = "https://docs.wradlib.org"
    git = "https://github.com/wradlib/wradlib.git"

    version('1.5', branch='release/1.5')
    version('1.4', branch='release/1.4')
    version('1.3', branch='release/1.3')
    version('1.2', branch='release/1.2')
    version('1.1', branch='release/1.1')
    version('1.0', branch='release/1.0')

    depends_on('py-setuptools', type='build')

    # https://docs.wradlib.org/en/stable/index.html
    conflicts('^python@:2.999', when='@1.3:')

    # recommended versions from https://docs.wradlib.org/en/stable/installation.html#dependencies
    depends_on('py-numpy@1.16:', type=('build', 'run'))
    depends_on('py-matplotlib@3.0.2:', type=('build', 'run'))
    depends_on('py-scipy@1.2.0:', type=('build', 'run'))
    depends_on('py-h5py@2.9:', type=('build', 'run'))
    depends_on('py-netcdf4@1.4.2:', type=('build', 'run'))
    depends_on('py-xarray@0.11.3:', type=('build', 'run'))
    depends_on('py-xmltodict@0.11:', type=('build', 'run'))
    depends_on('py-pygdal@2.4.0:', type=('build', 'run'))
    depends_on('py-semver', type=('build', 'run'))
    depends_on('py-deprecation', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
