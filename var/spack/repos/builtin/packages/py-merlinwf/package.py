# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMerlinwf(PythonPackage):
    """Merlin Workflow for HPC."""

    homepage = "https://github.com/LLNL/merlin"
    url      = "https://pypi.io/packages/source/m/merlinwf/merlinwf-1.2.3.tar.gz"
    git      = "https://github.com/LLNL/merlin.git"

    version('1.2.3', sha256='6b13a315f3e8e2894ea05d9cc072639f02eaf71ae0fdbd2bafebd1c20c8470ab')
    version('1.1.1', sha256='306055a987e42a79ce348a3f9d71293ed8a9b7f5909c26b6fd233d6a176fff6d')
    version('1.0.5', sha256='d66f50eac84ff9d7aa484f2d9655dc60f0352196d333284d81b6623a6f0aa180')
    version('master', branch='master')
    version('develop', branch='develop')

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
