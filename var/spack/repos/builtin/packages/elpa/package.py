# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Elpa(AutotoolsPackage):
    """Eigenvalue solvers for Petaflop-Applications (ELPA)"""

    homepage = 'http://elpa.mpcdf.mpg.de/'
    url = 'http://elpa.mpcdf.mpg.de/elpa-2015.11.001.tar.gz'

    version('2018.11.001',
            sha256='cc27fe8ba46ce6e6faa8aea02c8c9983052f8e73a00cfea38abf7613cb1e1b16')
    version('2018.05.001.rc1', sha256='598c01da20600a4514ea4d503b93e977ac0367e797cab7a7c1b0e0e3e86490db')
    version('2017.11.001', sha256='59f99c3abe2190fac0db8a301d0b9581ee134f438669dbc92551a54f6f861820')
    version('2017.05.003', sha256='bccd49ce35a323bd734b17642aed8f2588fea4cc78ee8133d88554753bc3bf1b')
    version('2017.05.002', sha256='568b71024c094d667b5cbb23045ad197ed5434071152ac608dae490ace5eb0aa')
    version('2016.11.001.pre', sha256='69b67f0f6faaa2b3b5fd848127b632be32771636d2ad04583c5269d550956f92')
    version('2016.05.004', sha256='08c59dc9da458bab856f489d779152e5506e04f0d4b8d6dcf114ca5fbbe46c58', preferred=True)
    version('2016.05.003', sha256='c8da50c987351514e61491e14390cdea4bdbf5b09045261991876ed5b433fca4')
    version('2015.11.001', sha256='c0761a92a31c08a4009c9688c85fc3fc8fde9b6ce05e514c3e1587cf045e9eba')

    variant('openmp', default=False, description='Activates OpenMP support')
    variant('optflags', default=True, description='Build with optimization flags')

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('scalapack')

    def url_for_version(self, version):
        t = 'http://elpa.mpcdf.mpg.de/html/Releases/{0}/elpa-{0}.tar.gz'
        if version < Version('2016.05.003'):
            t = 'http://elpa.mpcdf.mpg.de/elpa-{0}.tar.gz'
        return t.format(str(version))

    # override default implementation which returns static lib
    @property
    def libs(self):
        libname = 'libelpa_openmp' if '+openmp' in self.spec else 'libelpa'
        return find_libraries(
            libname, root=self.prefix, shared=True, recursive=True
        )

    @property
    def headers(self):
        suffix = '_openmp' if self.spec.satisfies('+openmp') else ''
        incdir = os.path.join(
            self.spec.prefix.include,
            'elpa{suffix}-{version!s}'.format(
                suffix=suffix, version=self.spec.version))

        hlist = find_all_headers(incdir)
        hlist.directories = [incdir]
        return hlist

    build_directory = 'spack-build'

    def setup_build_environment(self, env):
        spec = self.spec

        env.set('CC', spec['mpi'].mpicc)
        env.set('FC', spec['mpi'].mpifc)
        env.set('CXX', spec['mpi'].mpicxx)

        env.append_flags('LDFLAGS', spec['lapack'].libs.search_flags)
        env.append_flags('LIBS', spec['lapack'].libs.link_flags)
        env.set('SCALAPACK_LDFLAGS', spec['scalapack'].libs.joined())

    def configure_args(self):
        # TODO: set optimum flags for platform+compiler combo, see
        # https://github.com/hfp/xconfigure/tree/master/elpa
        # also see:
        # https://src.fedoraproject.org/cgit/rpms/elpa.git/
        # https://packages.qa.debian.org/e/elpa.html
        options = []
        # without -march=native there is configure error for 2017.05.02
        # Could not compile test program, try with --disable-sse, or
        # adjust the C compiler or CFLAGS
        if '+optflags' in self.spec:
            options.extend([
                'FCFLAGS=-O2 -ffree-line-length-none',
                'CFLAGS=-O2'
            ])
        if '+openmp' in self.spec:
            options.append('--enable-openmp')
        return options
