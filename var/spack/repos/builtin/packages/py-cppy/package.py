# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCppy(PythonPackage):
    """C++ headers for C extension development"""

    homepage = "https://github.com/nucleic/cppy"
    pypi     = "cppy/cppy-1.1.0.tar.gz"

    maintainers = ['iarspider']

    version('1.1.0', sha256='4eda6f1952054a270f32dc11df7c5e24b259a09fddf7bfaa5f33df9fb4a29642')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
