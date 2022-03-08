from spack import *
from spack.pkg.builtin.spark import Spark as BuiltinSpark


class Spark(BuiltinSpark):
    __doc__ = BuiltinSpark.__doc__

    url = "https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0-bin-3.2.0.tgz"

    version('3.2.1', sha256='224e058cb0c6fb68b39896427a3ccd11ae2246e9bf465b5e29e4fb192d39a59c')
    version('3.1.3', sha256='2411de04bec186b8651b27a5f16e4b511103c3c1e3f20fbb98b1f8804e61b77f')

    depends_on('hadoop@3.3:', when='@3.2:+hadoop', type=('build', 'run'))

    def url_for_version(self, version):
        hadoop_version = 'hadoop3.2'
        url = "http://archive.apache.org/dist/spark/spark-{0}/spark-{0}-bin-{1}.tgz"
        return url.format(version, hadoop_version)

    patch("spark-daemon-quote-log.patch")
