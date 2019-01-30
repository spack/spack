# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCdo(PythonPackage):
    """The cdo package provides an interface to the Climate Data
    Operators from Python."""

    homepage = "https://pypi.python.org/pypi/cdo"
    url      = "https://pypi.io/packages/source/c/cdo/cdo-1.3.2.tar.gz"

    version('1.3.2', '4b3686ec1b9b891f166c1c466c6db745')

    depends_on('cdo')

    depends_on('py-setuptools', type='build')
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-netcdf4', type=('build', 'run'))
