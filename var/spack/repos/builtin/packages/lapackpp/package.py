# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.util.package import *

# Each LAPACK++ version requires a specific BLAS++ version
_versions = [
    # LAPACK++,     BLAS++
    ['master',     'master'],
    ['2020.10.00', '2020.10.00'],
    ['2020.10.01', '2020.10.01'],
    ['2020.10.02', '2020.10.02'],
    ['2021.04.00', '2021.04.01:'],  # or later
]


class Lapackpp(CMakePackage):
    """LAPACK++: C++ API for the LAPACK Linear Algebra Package. Developed
       by the Innovative Computing Laboratory at the University of Tennessee,
       Knoxville."""

    homepage = "https://bitbucket.org/icl/lapackpp"
    git = homepage
    url = 'https://bitbucket.org/icl/lapackpp/downloads/lapackpp-2020.09.00.tar.gz'
    maintainers = ['teonnik', 'Sely85', 'G-Ragghianti', 'mgates3']

    version('master', branch='master')
    version('2021.04.00', sha256='67abd8de9757dba86eb5d154cdb91f176b6c8b2b7d8e2a669ba0c221c4bb60ed')
    version('2020.10.02', sha256='8dde9b95d75b494c4f8b893d68034e95b7a7541981359acb97b6c1c4a9c45cd9')
    version('2020.10.01', sha256='ecd659730b4c3cfb8d2595f9bbb6af65d96b79397db654f17fe045bdfea841c0')
    version('2020.10.00', sha256='5f6ab3bd3794711818a3a50198efd29571520bf455e13ffa8ba50fa8376d7d1a')

    variant('shared', default=True, description='Build shared library')

    # Match each LAPACK++ version to a specific BLAS++ version
    for (lpp_ver, bpp_ver) in _versions:
        depends_on('blaspp@' + bpp_ver, when='@' + lpp_ver)

    depends_on('blas')
    depends_on('lapack')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in spec),
            '-Dbuild_tests=%s'       % self.run_tests,
            '-DLAPACK_LIBRARIES=%s'  % spec['lapack'].libs.joined(';')
        ]

        if spec['blas'].name == 'cray-libsci':
            args.append(self.define('BLA_VENDOR', 'CRAY'))

        return args

    def check(self):
        # If the tester fails to build, ensure that the check() fails.
        if os.path.isfile(join_path(self.build_directory, 'test', 'tester')):
            with working_dir(self.build_directory):
                make('check')
        else:
            raise Exception('The tester was not built!')

    def flag_handler(self, name, flags):
        if (self.spec['blas'].name == 'cray-libsci') and name == 'cxxflags':
            flags.append('-DLAPACK_FORTRAN_ADD_')
        return (None, None, flags)
