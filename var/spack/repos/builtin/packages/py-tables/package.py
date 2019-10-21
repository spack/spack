# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTables(PythonPackage):
    """PyTables is a package for managing hierarchical datasets and designed to
    efficiently and easily cope with extremely large amounts of data."""

    homepage = "http://www.pytables.org/"
    url      = "https://github.com/PyTables/PyTables/archive/v3.6.0.tar.gz"

    import_modules = [
        'tables', 'tables.misc', 'tables.nodes', 'tables.scripts'
    ]

    version('3.6.0', sha256='2dcd077f42b195f48aa00f5a720b79189ea92fba0d16ad35e2881e403ba6914e')
    version('3.5.2', sha256='e4fc6f1194f02a8b10ff923e77364fb70710592f620d7de35f4d4e064dc70e91')
    version('3.4.4', sha256='c9682c0f35d8175e12bbd38d925bdb606d47b7c8e358ba056a9dbf3b1f183114')
    version('3.3.0', sha256='dceb15fef556a2775121bcc695561df4ff0e09248e0ce3a2d58f5244a9f61421')
    version('3.2.2', sha256='2626e874caa6b3fcf2bfc28b9dd6a40a3f859c72e19ce0764a60a6d77e350008',
            url='https://github.com/PyTables/PyTables/archive/v.3.2.2.tar.gz')

    variant('zlib', default=True, description='Support for zlib compression')
    variant('bzip2', default=False, description='Support for bzip2 compression')
    variant('lzo', default=False, description='Support for lzo compression')

    # requirements.txt
    depends_on('python@3.5:', when='@3.4:', type=('build', 'run'))
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.21:', type='build')
    depends_on('py-numpy@1.9.3:', type=('build', 'run'))
    depends_on('py-numexpr@2.6.2:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', when='@:3.5', type=('build', 'run'))
    depends_on('py-mock@2.0:', type='test')
    # tables/req_versions.py
    depends_on('hdf5@1.8.4:1.8.999', when='@:3.3.99')
    depends_on('hdf5@1.8.4:', when='@3.4.0:')
    # Versions prior to 3.3 must build with the internal blosc due to a lock
    # problem in a multithreaded environment.
    depends_on('c-blosc@1.4.1:', when='@3.3.0:')
    depends_on('zlib', when='+zlib')
    depends_on('bzip2', when='+bzip2')
    depends_on('lzo', when='+lzo')

    def setup_build_environment(self, env):
        env.set('HDF5_DIR', self.spec['hdf5'].prefix)
        if '+bzip2' in self.spec:
            env.set('BZIP2_DIR', self.spec['bzip2'].prefix)
        if '+lzo' in self.spec:
            env.set('LZO_DIR', self.spec['lzo'].prefix)
        if '^c-blosc' in self.spec:
            env.set('BLOSC_DIR', self.spec['c-blosc'].prefix)
