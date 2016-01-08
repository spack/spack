from spack import *
from glob import glob

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

        make('-f', 'Makefile-libbz2_so')
        make('clean')
        make("install", "PREFIX=%s" % prefix)

        bzip2_exe = join_path(prefix.bin, 'bzip2')
        install('bzip2-shared', bzip2_exe)
        for libfile in glob('libbz2.so*'):
            install(libfile, prefix.lib)

        bunzip2 = join_path(prefix.bin, 'bunzip2')
        remove(bunzip2)
        symlink(bzip2_exe, bunzip2)

        bzcat   = join_path(prefix.bin, 'bzcat')
        remove(bzcat)
        symlink(bzip2_exe, bzcat)
