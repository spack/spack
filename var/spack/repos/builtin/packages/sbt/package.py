# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sbt(Package):
    """Scala Build Tool"""

    homepage = 'http://www.scala-sbt.org'
    url      = "https://github.com/sbt/sbt/releases/download/v1.1.4/sbt-1.1.4.tgz"

    version('1.1.6', 'd307b131ed041c783ac5ed7bbb4768dc')
    version('1.1.5', 'b771480feb07f98fa8cd6d787c8d4485')
    version('1.1.4', 'c71e5fa846164d14d4cd450520d66c6a')
    version('0.13.17', 'c52c6152cc7aadfd1f0736a1a5d0a5b8')

    depends_on('java')

    def install(self, spec, prefix):
        install_tree('bin',  prefix.bin)
        install_tree('conf', prefix.conf)
