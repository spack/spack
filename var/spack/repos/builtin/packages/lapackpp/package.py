# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Lapackpp(CMakePackage):
    """LAPACK++: C++ API for the Basic Linear Algebra Subroutines. Developed
       by the Innovative Computing Laboratory at the University of Tennessee,
       Knoxville."""

    homepage = "https://bitbucket.org/icl/lapackpp"
    url = 'https://bitbucket.org/icl/lapackpp/downloads/lapackpp-2020.09.00.tar.gz'
    maintainers = ['teonnik', 'Sely85', 'G-Ragghianti', 'mgates3']

    version('develop', git=homepage)
    version('2020.09.00', sha256='b5d4defa8eb314f21b3788563da9d264e2b084f2eb6535f6c6798ba798a29ee5')

    variant('shared', default=True,
            description='Build a shared version of the library')

    # Needs to compile against a matching blaspp version
    depends_on('blaspp')
    depends_on('cblas')
    depends_on('lapack')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-Dbuild_tests:BOOL={0}'.format(
                'ON' if self.run_tests else 'OFF'),
            '-DBLAS_LIBRARIES=%s' % spec['lapack'].libs.joined(';')
        ]

    def check(self):
        with working_dir(join_path(self.build_directory, 'test')):
            if os.system('./run_tests.py --quick'):
                raise Exception('Tests were not all successful!')
