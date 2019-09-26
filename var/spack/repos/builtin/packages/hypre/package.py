# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys


class Hypre(Package):
    """Hypre is a library of high performance preconditioners that
       features parallel multigrid methods for both structured and
       unstructured grid problems."""

    homepage = "http://computing.llnl.gov/project/linear_solvers/software.php"
    url      = "https://github.com/hypre-space/hypre/archive/v2.14.0.tar.gz"
    git      = "https://github.com/hypre-space/hypre.git"

    maintainers = ['ulrikeyang', 'osborn9', 'balay']

    version('develop', branch='master')
    version('2.17.0', sha256='4674f938743aa29eb4d775211b13b089b9de84bfe5e9ea00c7d8782ed84a46d7')
    version('2.16.0', sha256='33f8a27041e697343b820d0426e74694670f955e21bbf3fcb07ee95b22c59e90')
    version('2.15.1', sha256='50d0c0c86b4baad227aa9bdfda4297acafc64c3c7256c27351f8bae1ae6f2402')
    version('2.15.0', sha256='2d597472b473964210ca9368b2cb027510fff4fa2193a8c04445e2ed4ff63045')
    version('2.14.0', sha256='705a0c67c68936bb011c50e7aa8d7d8b9693665a9709b584275ec3782e03ee8c')
    version('2.13.0', sha256='3979602689c3b6e491c7cf4b219cfe96df5a6cd69a5302ccaa8a95ab19064bad')
    version('2.12.1', sha256='824841a60b14167a0051b68fdb4e362e0207282348128c9d0ca0fd2c9848785c')
    version('2.11.2', 'd507943a1a3ce5681c3308e2f3a6dd34')
    version('2.11.1', '3f02ef8fd679239a6723f60b7f796519')
    version('2.10.1', 'dc048c4cabb3cd549af72591474ad674')
    version('2.10.0b', '768be38793a35bb5d055905b271f5b8e')
    version('xsdk-0.2.0', tag='xsdk-0.2.0', git='https://github.com/LLNL/hypre.git')

    # Versions 2.13.0 and later can be patched to build shared
    # libraries on Darwin; the patch for this capability does not
    # apply to version 2.12.1 and earlier due to changes in the build system
    # between versions 2.12.1 and 2.13.0.
    variant('shared', default=(sys.platform != 'darwin'),
            description="Build shared library (disables static library)")
    # SuperluDist have conflicting headers with those in Hypre
    variant('internal-superlu', default=True,
            description="Use internal Superlu routines")
    variant('superlu-dist', default=False,
            description='Activates support for SuperluDist')
    variant('int64', default=False,
            description="Use 64bit integers")
    variant('mpi', default=True, description='Enable MPI support')
    variant('debug', default=False,
            description='Build debug instead of optimized version')

    # Patch to add ppc64le in config.guess
    patch('ibm-ppc64le.patch', when='@:2.11.1')

    # Patch to build shared libraries on Darwin
    patch('darwin-shared-libs-for-hypre-2.13.0.patch', when='+shared@2.13.0 platform=darwin')
    patch('darwin-shared-libs-for-hypre-2.14.0.patch', when='+shared@2.14.0 platform=darwin')
    patch('superlu-dist-link-2.15.0.patch', when='+superlu-dist @2.15:2.16.0')
    patch('superlu-dist-link-2.14.0.patch', when='+superlu-dist @:2.14.0')

    depends_on("mpi", when='+mpi')
    depends_on("blas")
    depends_on("lapack")
    depends_on('superlu-dist', when='+superlu-dist+mpi')

    # Patch to build shared libraries on Darwin does not apply to
    # versions before 2.13.0
    conflicts("+shared@:2.12.99 platform=darwin")

    def url_for_version(self, version):
        if version >= Version('2.12.0'):
            url = 'https://github.com/hypre-space/hypre/archive/v{0}.tar.gz'
        else:
            url = 'http://computing.llnl.gov/project/linear_solvers/download/hypre-{0}.tar.gz'

        return url.format(version)

    def install(self, spec, prefix):
        # Note: --with-(lapack|blas)_libs= needs space separated list of names
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs

        configure_args = [
            '--prefix=%s' % prefix,
            '--with-lapack-libs=%s' % ' '.join(lapack.names),
            '--with-lapack-lib-dirs=%s' % ' '.join(lapack.directories),
            '--with-blas-libs=%s' % ' '.join(blas.names),
            '--with-blas-lib-dirs=%s' % ' '.join(blas.directories)
        ]

        if '+mpi' in self.spec:
            os.environ['CC'] = spec['mpi'].mpicc
            os.environ['CXX'] = spec['mpi'].mpicxx
            os.environ['F77'] = spec['mpi'].mpif77
            configure_args.append('--with-MPI')
        else:
            configure_args.append('--without-MPI')

        if '+int64' in self.spec:
            configure_args.append('--enable-bigint')

        if '+shared' in self.spec:
            configure_args.append("--enable-shared")

        if '~internal-superlu' in self.spec:
            configure_args.append("--without-superlu")
            # MLI and FEI do not build without superlu on Linux
            configure_args.append("--without-mli")
            configure_args.append("--without-fei")

        if 'superlu-dist' in self.spec:
            configure_args.append('--with-dsuperlu-include=%s' %
                                  spec['superlu-dist'].prefix.include)
            configure_args.append('--with-dsuperlu-lib=%s' %
                                  spec['superlu-dist'].libs)
            configure_args.append('--with-dsuperlu')

        if '+debug' in self.spec:
            configure_args.append("--enable-debug")
        else:
            configure_args.append("--disable-debug")

        # Hypre's source is staged under ./src so we'll have to manually
        # cd into it.
        with working_dir("src"):
            configure(*configure_args)

            make()
            if self.run_tests:
                make("check")
                make("test")
                Executable(join_path('test', 'ij'))()
                sstruct = Executable(join_path('test', 'struct'))
                sstruct()
                sstruct('-in', 'test/sstruct.in.default', '-solver', '40',
                        '-rhsone')
            make("install")

    @property
    def headers(self):
        """Export the main hypre header, HYPRE.h; all other headers can be found
        in the same directory.
        Sample usage: spec['hypre'].headers.cpp_flags
        """
        hdrs = find_headers('HYPRE', self.prefix.include, recursive=False)
        return hdrs or None

    @property
    def libs(self):
        """Export the hypre library.
        Sample usage: spec['hypre'].libs.ld_flags
        """
        is_shared = '+shared' in self.spec
        libs = find_libraries('libHYPRE', root=self.prefix, shared=is_shared,
                              recursive=True)
        return libs or None
