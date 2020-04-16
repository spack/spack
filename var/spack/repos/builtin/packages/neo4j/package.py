# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Neo4j(Package):
    """Neo4j is the world’s leading Graph Database. It is a high performance
    graph store with all the features expected of a mature and robust
    database, like a friendly query language and ACID transactions. The
    programmer works with a flexible network structure of nodes and
    relationships rather than static tables--yet enjoys all the benefits of
    enterprise-quality database. For many applications, Neo4j offers orders
    of magnitude performance benefits compared to relational DBs."""

    homepage = "http://neo4j.com/"
    url      = "https://github.com/neo4j/neo4j/archive/4.0.3.tar.gz"

    version('4.0.3',  sha256='19d79052657665dd661bbe906b3552b88108bf379d39fa007b883fff718cabee')
    version('3.5.16', sha256='1304fcd56b0f08f35b05d8b546fd844637ba1ffa5e00bb1e9a81a06b6242cb88')

    depends_on('maven', type='build')

    def install(self, spec, prefix):
        maven = which('mvn')
        maven('clean', 'install', '-DskipTests')
        install_tree('.', prefix)
