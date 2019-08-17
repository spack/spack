# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySagaPython(PythonPackage):
    """A light-weight access layer for distributed computing infrastructure"""

    homepage = "http://radical.rutgers.edu"
    url      = "https://pypi.io/packages/source/s/saga-python/saga-python-0.41.3.tar.gz"

    version('0.41.3', '3f92e16a53635ffe529fca4bae3b705d')

    depends_on('py-setuptools',      type='build')
    depends_on('py-apache-libcloud', type=('build', 'run'))
    depends_on('py-radical-utils',   type=('build', 'run'))
