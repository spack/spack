# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Maven(Package):
    """Apache Maven is a software project management and comprehension tool."""

    homepage = "https://maven.apache.org/index.html"
    url = "https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.3.9/apache-maven-3.3.9-bin.tar.gz"

    version('3.5.0', sha256='beb91419245395bd69a4a6edad5ca3ec1a8b64e41457672dc687c173a495f034')
    version('3.3.9', sha256='6e3e9c949ab4695a204f74038717aa7b2689b1be94875899ac1b3fe42800ff82')

    depends_on('java')

    def install(self, spec, prefix):
        # install pre-built distribution
        install_tree('.', prefix)
