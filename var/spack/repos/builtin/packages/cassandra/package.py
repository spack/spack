# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cassandra(Package):
    """
    Apache Cassandra is a highly-scalable partitioned row store. Rows are
    organized into tables with a required primary key.
    """

    homepage = "https://github.com/apache/cassandra"
    url      = "https://archive.apache.org/dist/cassandra/4.0.1/apache-cassandra-4.0.1-bin.tar.gz"

    version('4.0.1',   sha256='ed7022e30d9b77d9ce1072f8de95ab01ef7c5c6ed30f304e413dd5a3f92a52f8')
    version('3.11.11', sha256='a5639af781005410995a96f512d505c1def7b70cf5bbbec52e7cd5ff31b6cea3')
    version('3.11.6',  sha256='ce34edebd1b6bb35216ae97bd06d3efc338c05b273b78267556a99f85d30e45b', deprecated=True)
    version('3.11.5',  sha256='a765adcaa42a6c881f5e79d030854d082900992cc11da40eee413bb235970a6a', deprecated=True)
    version('2.2.19',  sha256='5496c0254a66b6d50bde7999d1bab9129b0406b71ad3318558f4d7dbfbed0ab9')

    depends_on('java@9:', type=('build', 'run'), when='@4.0.0:')
    depends_on('java@:8', type=('build', 'run'), when='@:3.11.11')

    def install(self, spec, prefix):
        install_tree('.', prefix)
