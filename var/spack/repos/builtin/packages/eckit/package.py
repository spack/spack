# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eckit(CMakePackage):
    """ecKit is a cross-platform c++ toolkit that supports development of tools
    and applications at ECMWF."""

    homepage = 'https://github.com/ecmwf/eckit'
    url = 'https://github.com/ecmwf/eckit/archive/refs/tags/1.16.0.tar.gz'

    maintainers = ['skosukhin']

    version('1.16.0', sha256='9e09161ea6955df693d3c9ac70131985eaf7cf24a9fa4d6263661c6814ebbaf1')

    variant('tools', default=True, description='Build the command line tools')
    variant('mpi', default=True, description='Enable MPI support')
    variant('admin', default=True,
            description='Build utilities for administration tools')
    variant('sql', default=True, description='Build SQL engine')
    variant('linalg',
            values=any_combination_of('eigen', 'armadillo', 'mkl', 'lapack'),
            description='List of supported linear algebra backends')
    variant('compression',
            values=any_combination_of('bzip2', 'snappy', 'lz4', 'aec'),
            description='List of supported compression backends')
    variant('xxhash', default=True,
            description='Enable xxHash support for hashing')
    variant('ssl', default=False,
            description='Enable MD4 and SHA1 support with OpenSSL')
    variant('curl', default=False,
            description='Enable URL data transferring with cURL')
    variant('jemalloc', default=False,
            description='Link against jemalloc memory allocator')
    variant('unicode', default=True,
            description='Enable support for Unicode characters in Yaml/JSON'
                        'parsers')
    variant('aio', default=True, description='Enable asynchronous IO')

    depends_on('cmake@3.12:', type='build')
    depends_on('ecbuild@3.5:', type='build')

    depends_on('mpi', when='+mpi')

    depends_on('yacc', type='build', when='+admin')
    depends_on('flex', type='build', when='+admin')
    depends_on('ncurses', when='+admin')

    depends_on('yacc', type='build', when='+sql')
    depends_on('flex', type='build', when='+sql')

    depends_on('eigen', when='linalg=eigen')
    depends_on('armadillo', when='linalg=armadillo')
    depends_on('mkl', when='linalg=mkl')
    depends_on('lapack', when='linalg=lapack')

    depends_on('bzip2', when='compression=bzip2')
    depends_on('snappy', when='compression=snappy')
    depends_on('lz4', when='compression=lz4')
    depends_on('libaec', when='compression=aec')

    depends_on('openssl', when='+ssl')

    depends_on('curl', when='+curl')

    depends_on('jemalloc', when='+jemalloc')

    # The package enables LAPACK backend (together with MKL backend)
    # when='linalg=mkl'. This leads to two identical installations when:
    #   eckit linalg=mkl
    #   eckit linalg=mkl,lapack
    # We prevent that by introducing the following conflict:
    conflicts('linalg=lapack', when='linalg=mkl',
              msg='"linalg=lapack" is implied when "linalg=mkl" and '
                  'must not be specified additionally')

    def cmake_args(self):
        args = [
            # Some features that we want to build are experimental:
            self.define('ENABLE_EXPERIMENTAL', True),
            self.define_from_variant('ENABLE_BUILD_TOOLS', 'tools'),
            # We let ecBuild find the MPI library. We could help it by setting
            # CMAKE_C_COMPILER to mpicc but that might give CMake a wrong
            # impression that no additional flags are needed to link to
            # libpthread, which will lead to problems with libraries that are
            # linked with the C++ compiler. We could additionally set
            # CMAKE_CXX_COMPILER to mpicxx. That would solve the problem with
            # libpthread but lead to overlinking to MPI libraries, which we
            # currently prefer to avoid since ecBuild does the job in all known
            # cases.
            self.define_from_variant('ENABLE_MPI', 'mpi'),
            self.define_from_variant('ENABLE_ECKIT_CMD', 'admin'),
            self.define_from_variant('ENABLE_ECKIT_SQL', 'sql'),
            self.define('ENABLE_EIGEN', 'linalg=eigen' in self.spec),
            self.define('ENABLE_ARMADILLO', 'linalg=armadillo' in self.spec),
            self.define('ENABLE_MKL', 'linalg=mkl' in self.spec),
            self.define('ENABLE_BZIP2', 'compression=bzip2' in self.spec),
            self.define('ENABLE_SNAPPY', 'compression=snappy' in self.spec),
            self.define('ENABLE_LZ4', 'compression=lz4' in self.spec),
            self.define('ENABLE_AEC', 'compression=aec' in self.spec),
            self.define_from_variant('ENABLE_XXHASH', 'xxhash'),
            self.define_from_variant('ENABLE_SSL', 'ssl'),
            self.define_from_variant('ENABLE_CURL', 'curl'),
            self.define_from_variant('ENABLE_JEMALLOC', 'jemalloc'),
            self.define_from_variant('ENABLE_UNICODE', 'unicode'),
            self.define_from_variant('ENABLE_AIO', 'aio'),
            self.define('ENABLE_TESTS', self.run_tests),
            # Unconditionally disable additional unit/performance tests, since
            # they download additional data (~1.6GB):
            self.define('ENABLE_EXTRA_TESTS', False),
            # No reason to check for doxygen and generate the documentation
            # since it is not installed:
            self.define('ENABLE_DOCS', False),
            # Disable features that are currently not needed:
            self.define('ENABLE_CUDA', False),
            self.define('ENABLE_VIENNACL', False),
            # Ceph/Rados storage support requires https://github.com/ceph/ceph
            # and will be added later:
            self.define('ENABLE_RADOS', False),
            # rsync support requires https://github.com/librsync/librsync and
            # will be added later:
            self.define('ENABLE_RSYNC', False),
            # Disable "prototyping code that may never see the light of day":
            self.define('ENABLE_SANDBOX', False)
        ]

        if 'linalg=mkl' not in self.spec:
            # ENABLE_LAPACK is ignored if MKL backend is enabled
            # (the LAPACK backend is still built though):
            args.append(
                self.define('ENABLE_LAPACK', 'linalg=lapack' in self.spec))

        return args
