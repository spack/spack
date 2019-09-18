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
    version('2018.05.001.rc1', 'ccd77bd8036988ee624f43c04992bcdd')
    version('2017.11.001', '4a437be40cc966efb07aaab84c20cd6e')
    version('2017.05.003', '7c8e5e58cafab212badaf4216695700f')
    version('2017.05.002', 'd0abc1ac1f493f93bf5e30ec8ab155dc')
    version('2016.11.001.pre', '5656fd066cf0dcd071dbcaf20a639b37')
    version('2016.05.004', 'c0dd3a53055536fc3a2a221e78d8b376')
    version('2016.05.003', '88a9f3f3bfb63e16509dd1be089dcf2c')
    version('2015.11.001', 'de0f35b7ee7c971fd0dca35c900b87e6')

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

    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        spack_env.set('CC', spec['mpi'].mpicc)
        spack_env.set('FC', spec['mpi'].mpifc)
        spack_env.set('CXX', spec['mpi'].mpicxx)

        spack_env.append_flags('LDFLAGS', spec['lapack'].libs.search_flags)
        spack_env.append_flags('LIBS', spec['lapack'].libs.link_flags)
        spack_env.set('SCALAPACK_LDFLAGS', spec['scalapack'].libs.joined())

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
                'FCFLAGS=-O2 -march=native -ffree-line-length-none',
                'CFLAGS=-O2 -march=native'
            ])
        if '+openmp' in self.spec:
            options.append('--enable-openmp')
        return options
