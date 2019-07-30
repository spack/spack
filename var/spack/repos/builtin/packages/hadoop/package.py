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
    url      = "http://mirror.easyname.ch/apache/hadoop/common/hadoop-3.1.3/hadoop-3.1.3.tar.gz"

    version('3.1.3', sha256='1e8b7ca4e3911f8ec999595f71921390e9ad7a27255fbd36af1f3a1628b67e2b')
    version('2.9.2', '82db6a62febd8c2976d75b8bd5513315')

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
