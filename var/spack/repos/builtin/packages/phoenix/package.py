# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Phoenix(Package):
    """Apache Phoenix is a SQL skin over HBase delivered as a client-embedded
    JDBC driver targeting low latency queries over HBase data."""

    homepage = "https://github.com"
    git      = "https://github.com/apache/phoenix.git"

    version('master', branch='master')

    depends_on('java@8:', type=('build', 'run'))
    depends_on('maven', type='build')

    def install(self, spec, prefix):
        mvn = which('mvn')
        mvn('package', '-DskipTests')
        install_tree('.', prefix)
