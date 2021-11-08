# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack import *


class Spark(Package):
    """Apache Spark is a fast and general engine
    for large-scale data processing.
    """

    homepage = "https://spark.apache.org"
    url = "https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0-bin-without-hadoop.tgz"

    variant('hadoop', default=True,
            description='Build with Hadoop')

    depends_on('java', type=('build', 'run'), when=('@3.0.0:'))
    depends_on('java@8', type=('build', 'run'), when=('@:2.4.99'))
    depends_on('hadoop@:2.999', when='+hadoop', type=('build', 'run'))

    version('3.1.2', sha256='3a79e324d12f46de44d042641d9340ba03f8ccb3db6f2496a9ccb65431dbb593')
    version('3.1.1', sha256='4e0846207bf10311de43451bc99309086fce7990aaf54bf3038608b1981afbe7')
    version('3.0.0', sha256='98f6b92e5c476d7abb93cc179c2616aa5dc897da25753bd197e20ef54a28d945')

    patch("spark-daemon-quote-log.patch")

    def url_for_version(self, version):
        url = "http://archive.apache.org/dist/spark/spark-{0}/spark-{0}-bin-{1}.tgz"
        return url.format(version, 'hadoop2.7')

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

    def setup_run_environment(self, env):
        hadoop = self.spec['hadoop'].command
        hadoop.add_default_env('JAVA_HOME', self.spec['java'].home)
        hadoop_classpath = hadoop('classpath', output=str)

        # Remove whitespaces, as they can compromise syntax in
        # module files
        hadoop_classpath = re.sub(r'[\s+]', '', hadoop_classpath)

        env.set('SPARK_DIST_CLASSPATH', hadoop_classpath)
