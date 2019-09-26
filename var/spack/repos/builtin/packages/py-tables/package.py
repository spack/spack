# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTables(PythonPackage):
    """PyTables is a package for managing hierarchical datasets and designed to
    efficiently and easily cope with extremely large amounts of data."""

    homepage = "http://www.pytables.org/"
    url      = "https://github.com/PyTables/PyTables/archive/v3.5.2.tar.gz"

    import_modules = [
        'tables', 'tables.misc', 'tables.nodes', 'tables.scripts'
    ]

    version('3.5.2', sha256='e4fc6f1194f02a8b10ff923e77364fb70710592f620d7de35f4d4e064dc70e91')
    version('3.4.4', '2cd52095ebb097f5bf58fa65dc6574bb')
    version('3.3.0', '056c161ae0fd2d6e585b766adacf3b0b')
    version('3.2.2', '7cbb0972e4d6580f629996a5bed92441',
            url='https://github.com/PyTables/PyTables/archive/v.3.2.2.tar.gz')

    variant('zlib', default=True, description='Support for zlib compression')
    variant('bzip2', default=False, description='Support for bzip2 compression')
    variant('lzo', default=False, description='Support for lzo compression')

    # requirements.txt
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy@1.9.3:', type=('build', 'run'))
    depends_on('py-numexpr@2.6.2:', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
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

    def setup_environment(self, spack_env, run_env):
        spack_env.set('HDF5_DIR', self.spec['hdf5'].prefix)
        if '+bzip2' in self.spec:
            spack_env.set('BZIP2_DIR', self.spec['bzip2'].prefix)
        if '+lzo' in self.spec:
            spack_env.set('LZO_DIR', self.spec['lzo'].prefix)
        if '^c-blosc' in self.spec:
            spack_env.set('BLOSC_DIR', self.spec['c-blosc'].prefix)
