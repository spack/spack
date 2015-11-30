from spack import *
from glob import glob
class Bowtie2(Package):
    """Description"""
    homepage = "bowtie-bio.sourceforge.net/bowtie2/index.shtml"
    version('2.2.5','51fa97a862d248d7ee660efc1147c75f', url = "http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.5/bowtie2-2.2.5-source.zip")

    patch('bowtie2-2.5.patch',when='@2.2.5', level=0)

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
        for bow in glob("bowtie2*"):
            install(bow, prefix.bin)
        # install('bowtie2',prefix.bin)
        # install('bowtie2-align-l',prefix.bin)
        # install('bowtie2-align-s',prefix.bin)
        # install('bowtie2-build',prefix.bin)
        # install('bowtie2-build-l',prefix.bin)
        # install('bowtie2-build-s',prefix.bin)
        # install('bowtie2-inspect',prefix.bin)
        # install('bowtie2-inspect-l',prefix.bin)
        # install('bowtie2-inspect-s',prefix.bin)

