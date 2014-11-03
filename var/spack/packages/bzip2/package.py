from spack import *

class Bzip2(Package):
    """bzip2 is a freely available, patent free high-quality data
       compressor. It typically compresses files to within 10% to 15%
       of the best available techniques (the PPM family of statistical
       compressors), whilst being around twice as fast at compression
       and six times faster at decompression."""
    homepage = "http://www.bzip.org"
    url      = "http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz"

    version('1.0.6', '00b516f4704d4a7cb50a1d97e6e8e15b')

    def install(self, spec, prefix):
        # No configure system -- have to filter the makefile for this package.
        filter_file(r'CC=gcc', 'CC=cc', 'Makefile', string=True)

        make()
        make("install", "PREFIX=%s" % prefix)
