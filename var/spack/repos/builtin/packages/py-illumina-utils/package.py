# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIlluminaUtils(PythonPackage):
    """A library and collection of scripts to work with Illumina paired-end
    data (for CASAVA 1.8+)."""

    homepage = "https://github.com/meren/illumina-utils"
    url      = "https://pypi.io/packages/source/i/illumina-utils/illumina-utils-2.2.tar.gz"

    version('2.3', 'c0af71723e52ab2b14660d2138620e39')
    version('2.2', '9e19cf112ccc38a903fc41f431804d21')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-python-levenshtein', type=('build', 'run'))
