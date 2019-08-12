# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Veclibfort(Package):
    """Lightweight but flexible shim designed to rectify the incompatibilities
    between the Accelerate/vecLib BLAS and LAPACK libraries shipped with macOS
    and FORTRAN code compiled with modern compilers such as GNU Fortran."""

    homepage = "https://github.com/mcg1969/vecLibFort"
    url      = "https://github.com/mcg1969/vecLibFort/archive/0.4.2.tar.gz"
    git      = "https://github.com/mcg1969/vecLibFort.git"

    version('develop', branch='master')
    version('0.4.2', '83395ffcbe8a2122c3f726a5c3a7cf93')

    variant('shared', default=True,
            description="Build shared libraries as well as static libs.")

    # virtual dependency
    provides('blas')
    provides('lapack')

    @property
    def libs(self):
        shared = True if '+shared' in self.spec else False
        return find_libraries(
            'libvecLibFort', root=self.prefix, shared=shared, recursive=True
        )

    @property
    def headers(self):
        # veclibfort does not come with any headers. Return an empty list
        # to avoid `spec['blas'].headers` from crashing.
        return HeaderList([])

    def install(self, spec, prefix):
        if sys.platform != 'darwin':
            raise InstallError('vecLibFort can be installed on macOS only')

        filter_file(r'^PREFIX=.*', '', 'Makefile')

        make_args = []

        if spec.satisfies('%gcc@6:'):
            make_args += ['CFLAGS=-flax-vector-conversions']

        make_args += ['PREFIX=%s' % prefix, 'install']

        make(*make_args)

        # test
        fc = which('fc')
        flags = ['-o', 'tester', '-O', 'tester.f90']
        flags.extend(spec['veclibfort'].libs.ld_flags.split())
        fc(*flags)
        Executable('./tester')()
