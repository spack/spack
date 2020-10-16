# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lapackpp(CMakePackage):
    """LAPACK++: C++ API for the LAPACK Linear Algebra Package. Developed
       by the Innovative Computing Laboratory at the University of Tennessee,
       Knoxville."""

    homepage = "https://bitbucket.org/icl/lapackpp"
    git = "https://bitbucket.org/gragghia/lapackpp"
    url = 'https://bitbucket.org/icl/lapackpp/downloads/lapackpp-2020.09.00.tar.gz'
    maintainers = ['teonnik', 'Sely85', 'G-Ragghianti', 'mgates3']

    version('master', branch='master')
    version('2020.10.00', sha256='5f6ab3bd3794711818a3a50198efd29571520bf455e13ffa8ba50fa8376d7d1a')
    version('2020.09.00', sha256='b5d4defa8eb314f21b3788563da9d264e2b084f2eb6535f6c6798ba798a29ee5')

    variant('shared', default=True, description='Build shared library')

    # Needs to compile against a matching blaspp version
    depends_on('blaspp@master', when='lapackpp@master')
    depends_on('blaspp@2020.10.00', when='lapackpp@2020.10.00')
    depends_on('blaspp@2020.09.00', when='lapackpp@2020.09.00')
    depends_on('blas')
    depends_on('lapack')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in spec),
            '-Dbuild_tests=%s' % self.run_tests,
            '-DLAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(';'),
            '-DCMAKE_MESSAGE_LOG_LEVEL=TRACE'
        ]
