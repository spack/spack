# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Claw(CMakePackage):
    """CLAW Compiler targets performance portability problem in climate and
       weather application written in Fortran. From a single source code, it
       generates architecture specific code decorated with OpenMP or OpenACC"""

    homepage = 'https://claw-project.github.io/'
    git      = 'https://github.com/claw-project/claw-compiler.git'
    maintainers = ['clementval']

    version('1.2.0', commit='fc9c50fe02be97b910ff9c7015064f89be88a3a2', submodules=True)
    version('1.1.0', commit='16b165a443b11b025a77cad830b1280b8c9bcf01', submodules=True)

    depends_on('cmake@3.0:', type='build')
    depends_on('java@7:')
    depends_on('ant@1.9:')
    depends_on('libxml2')
    depends_on('bison')

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append('-DOMNI_CONF_OPTION=--with-libxml2={0}'.
                    format(spec['libxml2'].prefix))

        args.append('-DCMAKE_Fortran_COMPILER={0}'.
                    format(self.compiler.fc))

        return args
