# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyFlattenDict(PythonPackage):
    """A flexible utility for flattening and unflattening dict-lik objects
    in Python"""

    homepage = "https://github.com/ianlini/flatten-dict"
    pypi     = "flatten-dict/flatten-dict-0.3.0.tar.gz"

    version('0.3.0', sha256='0ccc43f15c7c84c5ef387ad19254f6769a32d170313a1bcbf4ce582089313d7e')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-pathlib2', type=('build', 'run'))
