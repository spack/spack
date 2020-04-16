# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ZookeeperBenchmark(Package):
    """It is designed to measure the per-request latency of a ZooKeeper
    ensemble for a predetermined length of time"""

    homepage = "http://zookeeper.apache.org"
    git      = "https://github.com/brownsys/zookeeper-benchmark.git"

    version('master', branch='master')

    variant('zooKeeperVersion', default='3.3.6', description='The client code corresponding to the ZooKeeper version will be found using maven.')

    depends_on('maven', type='build')
    depends_on('zookeeper', type=('build', 'run'))

    def install(self, spec, prefix):
        zookeeper_version = self.spec['zookeeper'].version.string
        mvn = which('mvn')
        mvn('-DZooKeeperVersion=' + zookeeper_version, 'package')
        install_tree('.', prefix)
