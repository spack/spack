from spack import *

class Samtools(Package):
    """SAM Tools provide various utilities for manipulating alignments in the SAM format, 
       including sorting, merging, indexing and generating
       alignments in a per-position format"""

    homepage = "www.htslib.org"
    version('1.2','988ec4c3058a6ceda36503eebecd4122',url = "https://github.com/samtools/samtools/releases/download/1.2/samtools-1.2.tar.bz2")

    depends_on("zlib")
    depends_on("mpc")
    parallel=False
    patch("samtools1.2.patch",level=0)

    def install(self, spec, prefix):
        make("prefix=%s" % prefix, "install")

