# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ant(Package):
    """Apache Ant is a Java library and command-line tool whose mission is to
       drive processes described in build files as targets and extension points
       dependent upon each other
    """

    homepage = "http://ant.apache.org/"
    url = "https://archive.apache.org/dist/ant/source/apache-ant-1.9.7-src.tar.gz"

    version('1.10.0', '2260301bb7734e34d8b96f1a5fd7979c')
    version('1.9.9',  '22c9d40dabafbec348aaada226581239')
    version('1.9.8',  '16253d516d5c33c4af9ef8fafcf1004b')
    version('1.9.7',  'a2fd9458c76700b7be51ef12f07d4bb1')
    version('1.9.6',  '29b7507c9053e301d2b85091f2aec6f0')

    depends_on('java')

    def install(self, spec, prefix):
        env['ANT_HOME'] = self.prefix
        bash = which('bash')
        bash('./build.sh', 'install-lite')
