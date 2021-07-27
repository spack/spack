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
    version('0.2.4', tag='v0.2.4', submodules=True, get_full_repo=True)
    version('0.1.1', tag='v0.1.1', submodules=True, get_full_repo=True)

    depends_on('benchmark', type='build')
    depends_on('cmake@3.7:')
    depends_on('doxygen', type='build')
    depends_on('py-breathe', type='build')
    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-exhale', type='build')
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-humanize', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-progress', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-sphinx', type='build')
    depends_on('py-sphinx-rtd-theme', type='build')
    depends_on('python@3:')
    depends_on('rocksdb~static+snappy')

    def build_args(self, spec, prefix):
        return ['test', '--no-doc-test']
