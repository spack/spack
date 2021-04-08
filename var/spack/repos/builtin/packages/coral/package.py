# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Coral(CMakePackage):
    """CORAL is an abstraction layer with an SQL-free API to access data stored using relational
       database technologies. It is used directly by experiment-specific applications and
       internally by COOL."""

    homepage = "https://coral-cool.docs.cern.ch/"
    git      = "https://gitlab.cern.ch/lcgcoral/coral.git"

    version('3.3.3', tag='CORAL_3_3_3')
    variant('binary_tag', default='x86_64-centos7-gcc8-opt')

    depends_on('ninja')
    depends_on('ccache')
    depends_on('boost')
    depends_on('cppunit')
    depends_on('expat')
    depends_on('frontier-client')
    depends_on('libaio')
    depends_on('mariadb')
    depends_on('python')
#    depends_on('qmtest')
    depends_on('xerces-c')
    depends_on('sqlite')
    depends_on('gperftools')
    depends_on('igprof')
    depends_on('libunwind')
    depends_on('valgrind')
    depends_on('sqlplus')

    def cmake_args(self):
        args = ['-DBINARY_TAG=' + self.spec.variants['binary_tag'].value]
        if self.spec['python'].version >= Version("3.0.0"):
            args.append('-DLCG_python3=on')

        return args
