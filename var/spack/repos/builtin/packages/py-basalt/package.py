# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBasalt(PythonPackage):
    """C++11 Graph Storage library with Python interface"""

    homepage = "https://github.com/tristan0x/basalt"
    url      = "git@github.com:tristan0x/basalt.git"
    
    version('develop', git=url, branch='master', submodules=True, clean=False)
    version('0.2.2', git=url, tag='v0.2.2', submodules=True, preferred=True, clean=False)
    version('0.2.1', git=url, tag='v0.2.1', submodules=True, clean=False)
    version('0.1.1', git=url, tag='v0.1.1', submodules=True, clean=False)

    depends_on('benchmark', type='build')
    depends_on('cmake@3.7:')
    depends_on('doxygen', type='build')
    depends_on('py-breathe', type='build')
    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-docopt', type=('build', 'run'))
    depends_on('py-exhale', type='build')
    depends_on('py-h5py~mpi', type=('build', 'run'))
    depends_on('py-humanize', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-progress', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-sphinx', type='build')
    depends_on('py-sphinx-rtd-theme', type='build')
    depends_on('python@3:')
    depends_on('rocksdb~static')

    def build_args(self, spec, prefix):
        return ['test']
