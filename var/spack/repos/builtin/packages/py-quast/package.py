# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQuast(PythonPackage):
    """Quality Assessment Tool for Genome Assemblies"""

    homepage = "http://cab.spbu.ru/software/quast"
    url      = "https://github.com/ablab/quast/archive/quast_4.6.1.tar.gz"

    version('4.6.3', '16d77acb2e0f6436b58d9df7b732fb76')
    version('4.6.1', '37ccd34e0040c17aa6f990353a92475c')
    version('4.6.0', 'c04d62c50ec4d9caa9d7388950b8d144')

    depends_on('boost@1.56.0')
    depends_on('perl@5.6.0:')
    depends_on('python@2.5:,3.3:')
    depends_on('py-setuptools',    type='build')
    depends_on('py-matplotlib',    type=('build', 'run'))
    depends_on('java',             type=('build', 'run'))
    depends_on('perl-time-hires',  type=('build', 'run'))
    depends_on('gnuplot',          type=('build', 'run'))
    depends_on('mummer',           type=('build', 'run'))
    depends_on('bedtools2',        type=('build', 'run'))
    depends_on('bwa',              type=('build', 'run'))
    depends_on('glimmer',          type=('build', 'run'))
