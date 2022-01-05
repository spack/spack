# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBasalt(PythonPackage):
    """C++11 Graph Storage library with Python interface"""

    homepage = "https://github.com/BlueBrain/basalt"
    git      = "https://github.com/BlueBrain/basalt.git"

    version('develop', branch='master', submodules=True, get_full_repo=True)
    version('0.2.9', tag='v0.2.9', submodules=True, get_full_repo=True)

    depends_on('cmake@3.7:')
    depends_on('rocksdb~static+snappy')

    depends_on('python@3:')
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-wheel', type='build')

    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))

    def build_args(self, spec, prefix):
        return ['test', '--no-doc-test']
