# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMerlinwf(PythonPackage):
    """Merlin Workflow for HPC."""

    homepage = "https://github.com/LLNL/merlin"
    url      = "https://pypi.io/packages/source/m/merlinwf/merlinwf-1.2.2.tar.gz"
    git      = "https://github.com/LLNL/merlin.git"

    version('1.2.2', sha256='37b92b1781e6409ba27a24ca04a41e10c9e6fdb1e8e40a6951ca0d214fbb42e3')
    version('1.1.1', sha256='306055a987e42a79ce348a3f9d71293ed8a9b7f5909c26b6fd233d6a176fff6d')
    version('1.0.5', sha256='d66f50eac84ff9d7aa484f2d9655dc60f0352196d333284d81b6623a6f0aa180')
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
    depends_on('py-importlib-resources', when="^python@3.0:3.6.99", type=('build', 'run'))
    depends_on('py-maestrowf@1.1.7dev0:', when="@1.2.0:", type=('build', 'run'))
    depends_on('py-maestrowf@1.1.6:', when="@:1.1.99", type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-parse', type=('build', 'run'))
    depends_on('py-psutil@5.1.0:', type=('build', 'run'))
    depends_on('py-pyyaml@5.1.2:', type=('build', 'run'))
    depends_on('py-tabulate', type=('build', 'run'))

    # Optional packages
    depends_on('py-mysql-connector-python-rf', when='+mysql', type=('build', 'run'))
    depends_on('pymysql', when='+mysql', type=('build', 'run'))
