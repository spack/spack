# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Testdfsio(Package):
    """A corrected and enhanced version of Apache Hadoop TestDFSIO"""

    homepage = "https://github.com/tthx/testdfsio"
    url      = "https://github.com/tthx/testdfsio/archive/0.0.1.tar.gz"

    version('0.0.1', sha256='fe8cc47260ffb3e3ac90e0796ebfe73eb4dac64964ab77671e5d32435339dd09')

    depends_on('maven', type='build')
    depends_on('java@8', type=('build', 'run'))
    depends_on('hadoop@3.2.1:', type='run')

    def install(self, spec, prefix):
        mvn = which('mvn')
        mvn('clean', 'package', '-Dmaven.test.skip=true')
        install_tree('.', prefix)
