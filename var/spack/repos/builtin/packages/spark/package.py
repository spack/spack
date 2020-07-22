# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack import *


class Spark(Package):
    """Apache Spark is a fast and general engine
    for large-scale data processing.
    """

    homepage = "http://spark.apache.org"

    variant('hadoop', default=False,
            description='Build with Hadoop')

    depends_on('java', type=('build', 'run'), when=('@3.0.0:'))
    depends_on('java@8', type=('build', 'run'), when=('@:2.4.99'))
    depends_on('hadoop', when='+hadoop', type=('build', 'run'))

    version('3.0.0', sha256='40f58f117efa83a1d0e66030d3561a8d7678f5473d1f3bb53e05c40d8d6e6781')
    version('2.4.5', sha256='40f58f117efa83a1d0e66030d3561a8d7678f5473d1f3bb53e05c40d8d6e6781')
    version('2.4.0', sha256='b1d6d6cb49d8253b36df8372a722292bb323bd16315d83f0b0bafb66a4154ef2')
    version('2.3.0', sha256='a7e29e78bd43aa6d137f0bb0afd54a3017865d471456c6d436ae79475bbeb161')
    version('2.1.0', sha256='3ca4ecb0eb9a00de5099cc2564ed957433a2d15d9d645a60470324621853c5ae')
    version('2.0.2', sha256='122ec1af0fcb23c0345f20f77d33cf378422ffe966efe4b9ef90e55cf7a46a3c')
    version('2.0.0', sha256='7c90bc4b7689df30f187e00845db8c7c9fb4045a0bcf2fa70a4954cc17d2c0d1')
    version('1.6.2', sha256='f6b43333ca80629bacbbbc2e460d21064f53f50880f3f0a3f68745fdf8b3137e')
    version('1.6.1', sha256='3d67678c5cb5eeba1cab125219fa2f9f17609368ea462e3993d2eae7c8f37207')
    version('1.6.0', sha256='9f62bc1d1f7668becd1fcedd5ded01ad907246df287d2525cfc562d88a3676da')

    def url_for_version(self, version):
        url = "http://archive.apache.org/dist/spark/spark-{0}/spark-{0}-bin-{1}.tgz"
        if self.spec.satisfies('@2.4.0: +hadoop'):
            checksums = {
                Version('3.0.0'): '98f6b92e5c476d7abb93cc179c2616aa5dc897da25753bd197e20ef54a28d945',
                Version('2.4.5'): '020be52524e4df366eb974d41a6e18fcb6efcaba9a51632169e917c74267dd81',
                Version('2.4.0'): 'c93c096c8d64062345b26b34c85127a6848cff95a4bb829333a06b83222a5cfa'
            }
            self.versions[version] = {'checksum': checksums[version]}
            return url.format(version, 'hadoop2.7')
        return url.format(version, 'without-hadoop')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('conf')
        install_dir('jars')
        install_dir('python')
        install_dir('R')
        install_dir('sbin')
        install_dir('yarn')

        # required for spark to recognize binary distribution
        install('RELEASE', prefix)

    @when('+hadoop')
    def setup_run_environment(self, env):
        hadoop = self.spec['hadoop'].command
        hadoop.add_default_env('JAVA_HOME', self.spec['java'].home)
        hadoop_classpath = hadoop('classpath', output=str)

        # Remove whitespaces, as they can compromise syntax in
        # module files
        hadoop_classpath = re.sub(r'[\s+]', '', hadoop_classpath)

        env.set('SPARK_DIST_CLASSPATH', hadoop_classpath)
