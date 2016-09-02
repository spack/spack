from spack import *
import shutil


class Sbt(Package):
    """Scala Build Tool"""

    homepage = "http://http://www.scala-sbt.org"
    url      = "http://http://www.scala-sbt.org/download.html"

    version('0.13.12', 'cec3071d46ef13334c8097cc3467ff28',
            url='https://dl.bintray.com/sbt/native-packages/sbt/0.13.12/sbt-0.13.12.tgz')

    depends_on('jdk')

    def install(self, spec, prefix):
        shutil.copytree('bin', join_path(prefix, 'bin'), symlinks=True)
        shutil.copytree('conf', join_path(prefix, 'conf'), symlinks=True)
