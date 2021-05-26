# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCoveralls(PythonPackage):
    """coveralls.io is a service for publishing your coverage stats online."""

    homepage = "https://coveralls-python.readthedocs.io/en/latest/index.html"
    pypi     = "coveralls/coveralls-3.0.1.tar.gz"

    maintainers = ['dorton21']

    version('3.0.1', sha256='cbb942ae5ef3d2b55388cb5b43e93a269544911535f1e750e1c656aef019ce60')

    depends_on('py-setuptools', type='build')
    depends_on('py-mock', type=('build', 'run'))
    depends_on('py-responses', type=('build', 'run'))
    depends_on('py-pytest', type='test')
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-coverage', type=('build', 'run'))
    depends_on('py-docopt', type=('build', 'run'))
