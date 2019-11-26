# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMerlinwf(PythonPackage):
    """Merlin Workflow for HPC."""

    homepage = "https://github.com/LLNL/merlin.git"
    url      = "https://pypi.io/packages/source/m/merlinwf/merlinwf-1.0.0.tar.gz"
    git      = "https://github.com/LLNL/merlin.git"

    version('1.0.0', sha256='')
    version('master', branch='master')
    version('develop', branch='develop')

    variant('mysql', default=False, description="Support for mysql results backend")

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-pytest', type='test')

    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-celery@4.3.0:+redis', type=('build', 'run'))
    depends_on('py-coloredlogs@10.0:', type=('build', 'run'))
    depends_on('py-cryptography', type=('build', 'run'))
    depends_on('py-maestrowf@1.1.15:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-parse', type=('build', 'run'))
    depends_on('py-psutil@5.1.0:', type=('build', 'run'))
    depends_on('py-pyyaml@5.1.2:', type=('build', 'run'))
    depends_on('py-importlib-rerources', when="^python@3.0:3.6.99", type=('build', 'run'))

    # Optional packages
    depends_on('py-mysql-connector-python-rf', when='+mysql', type=('build', 'run'))
    depends_on('pymysql', when='+mysql', type=('build', 'run'))

    def test(self):
        pytest = which('pytest')
        pytest()
