# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPybedtools(PythonPackage):
    """Python wrapper -- and more -- for Aaron Quinlan's BEDTools"""

    homepage = "http://daler.github.io/pybedtools"
    url      = "https://github.com/daler/pybedtools/archive/v0.6.9.tar.gz"

    version('0.6.9', sha256='2639e80917999e76572017fd93757e8d7ceb384f0b92647ccfdd23a0d60def7c')

    depends_on('bedtools2', type='run')
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
