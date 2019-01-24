# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Maven(Package):
    """Apache Maven is a software project management and comprehension tool."""

    homepage = "https://maven.apache.org/index.html"
    url = "https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.3.9/apache-maven-3.3.9-bin.tar.gz"

    version('3.5.0', '35c39251d2af99b6624d40d801f6ff02')
    version('3.3.9', '516923b3955b6035ba6b0a5b031fbd8b')

    depends_on('java')

    def install(self, spec, prefix):
        # install pre-built distribution
        install_tree('.', prefix)
