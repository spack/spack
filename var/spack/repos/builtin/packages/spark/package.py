from spack import *

import distutils
from distutils import dir_util


class Spark(Package):
    """
    Apache Spark is a fast and general engine
    for large-scale data processing.
    """

    homepage = "http://spark.apache.org"
    url      = "http://spark.apache.org/downloads.html"

    variant('hadoop', default=False,
            description='Build with Hadoop')

    depends_on('jdk')
    depends_on('hadoop', when='+hadoop')

    version('2.0.0', '8a5307d973da6949a385aefb6ff747bb',
            url = 'http://mirrors.ocf.berkeley.edu/apache/spark/spark-2.0.0/spark-2.0.0-bin-without-hadoop.tgz')
    version('1.6.2', '304394fbe2899211217f0cd9e9b2b5d9',
            url = 'http://mirrors.ocf.berkeley.edu/apache/spark/spark-1.6.2/spark-1.6.2-bin-without-hadoop.tgz')
    version('1.6.1', 'fcf4961649f15af1fea78c882e65b001',
            url = 'http://mirrors.ocf.berkeley.edu/apache/spark/spark-1.6.1/spark-1.6.1-bin-without-hadoop.tgz')

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree('.', prefix)

    @when('+hadoop')
    def setup_environment(self, spack_env, run_env):
        hadoop_bin = Executable(join_path(self.spec['hadoop'].prefix.bin, 'hadoop'))
        hadoop_classpath = hadoop_bin('classpath', return_output=True)
        run_env.set('SPARK_DIST_CLASSPATH', hadoop_classpath)
