# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('1.10.0', sha256='1f78036c38753880e16fb755516c8070187a78fe4b2e99b59eda5b81b58eccaf')
    version('1.9.9',  sha256='d6a0c93777ab27db36212d77c5733ac80d17fe24e83f947df23a8e0ad4ac48cc')
    version('1.9.8',  sha256='5f4daf56e66fc7a71de772920ca27c15eac80cf1fcf41f3b4f2d535724942681')
    version('1.9.7',  sha256='648b3f3787bb0cb6226978b6d4898eb7e21ae391385357a5f824972dd910a1c8')
    version('1.9.6',  sha256='550d2aaf828785e30870c227056942c2a552da961db6010cedb2fbcfa8e3268d')

    depends_on('java')

    def install(self, spec, prefix):
        env['ANT_HOME'] = self.prefix
        bash = which('bash')
        bash('./build.sh', 'install-lite')
