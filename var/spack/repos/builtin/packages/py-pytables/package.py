# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytables(PythonPackage):
    """PyTables is a package for managing hierarchical datasets and designed to
    efficiently and easily cope with extremely large amounts of data."""
    homepage = "http://www.pytables.org/"
    url      = "https://github.com/PyTables/PyTables/archive/v3.3.0.tar.gz"

    version('3.5.1', sha256='fda2e5071ce064ae1e808623e4c6166e6ab5f0f6152043991c5151d4e2622f2e')
    version('3.4.4', '2cd52095ebb097f5bf58fa65dc6574bb')
    version('3.3.0', '056c161ae0fd2d6e585b766adacf3b0b')
    version('3.2.2', '7cbb0972e4d6580f629996a5bed92441',
            url='https://github.com/PyTables/PyTables/archive/v.3.2.2.tar.gz')

    variant('blosc', default=True, description='Use spack provided c-blosc.')
    variant('lzo', default=False, description='Use optional lzo')
    variant('bzip2', default=False, description='Use optional bzip2')

    depends_on('hdf5@1.8.0:1.8.999', when="@:3.3.99")
    depends_on('hdf5@1.8.0:1.10.999', when="@3.4.0:")
    depends_on('c-blosc', when='+blosc')
    depends_on('lzo', when='+lzo')
    depends_on('py-numpy@1.8.0:', type=('build', 'run'))
    depends_on('py-numexpr@2.5.2:', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        spack_env.set('HDF5_DIR', self.spec['hdf5'].prefix)
        spack_env.set('BLOSC_DIR', self.spec['c-blosc'].prefix)
        spack_env.set('LZO_DIR', self.spec['lzo'].prefix)
        spack_env.set('BZIP2_DIR', self.spec['bzip2'].prefix)
