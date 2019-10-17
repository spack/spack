# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hadoop(Package):
    """The Apache Hadoop software library is a framework that
    allows for the distributed processing of large data sets
    across clusters of computers using simple programming models.
    """

    homepage = "http://hadoop.apache.org/"
    url      = "http://apache-mirror.8birdsvideo.com/hadoop/common/hadoop-3.1.2/hadoop-3.1.2-src.tar.gz"

    version('3.1.2', sha256='02f277c9fc75d4b13c7697ed6be30dba41667841ab5e37442855267c39bec6b6')

    depends_on('java', type='run')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('etc')
        install_dir('include')
        install_dir('lib')
        install_dir('libexec')
        install_dir('sbin')
        install_dir('share')
