from spack import *

class Bzip2(Package):
    """bzip2 is a freely available, patent free high-quality data
       compressor. It typically compresses files to within 10% to 15%
       of the best available techniques (the PPM family of statistical
       compressors), whilst being around twice as fast at compression
       and six times faster at decompression.

    """
    homepage = "http://www.bzip.org"
    url      = "http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz"

    version('1.0.6', '00b516f4704d4a7cb50a1d97e6e8e15b')


    def patch(self):
        mf = FileFilter('Makefile-libbz2_so')
        mf.filter(r'^CC=gcc', 'CC=cc')

        # Below stuff patches the link line to use RPATHs on Mac OS X.
        if 'darwin' in self.spec.architecture:
            v = self.spec.version
            v1, v2, v3 = (v.up_to(i) for i in (1,2,3))

            mf.filter('$(CC) -shared -Wl,-soname -Wl,libbz2.so.{0} -o libbz2.so.{1} $(OBJS)'.format(v2, v3),
                      '$(CC) -dynamiclib -Wl,-install_name -Wl,@rpath/libbz2.{0}.dylib -current_version {1} -compatibility_version {2} -o libbz2.{3}.dylib $(OBJS)'.format(v1, v2, v3, v3), string=True)

            mf.filter('$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.so.{0}'.format(v3),
                      '$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.{0}.dylib'.format(v3), string=True)
            mf.filter('rm -f libbz2.so.{0}'.format(v2),
                      'rm -f libbz2.{0}.dylib'.format(v2), string=True)
            mf.filter('ln -s libbz2.so.{0} libbz2.so.{1}'.format(v3, v2),
                      'ln -s libbz2.{0}.dylib libbz2.{1}.dylib'.format(v3, v2), string=True)


    def install(self, spec, prefix):
        make('-f', 'Makefile-libbz2_so')
        make('clean')
        make("install", "PREFIX=%s" % prefix)

        install('bzip2-shared', join_path(prefix.bin, 'bzip2'))

        v1, v2, v3 = (self.spec.version.up_to(i) for i in (1,2,3))
        if 'darwin' in self.spec.architecture:
            lib = 'libbz2.dylib'
            lib1, lib2, lib3 = ('libbz2.{0}.dylib'.format(v) for v in (v1, v2, v3))
        else:
            lib = 'libbz2.so'
            lib1, lib2, lib3 = ('libbz2.so.{0}'.format(v) for v in (v1, v2, v3))

        install(lib3, join_path(prefix.lib, lib3))
        with working_dir(prefix.lib):
            for l in (lib, lib1, lib2):
                symlink(lib3, l)

        with working_dir(prefix.bin):
            force_remove('bunzip2', 'bzcat')
            symlink('bzip2', 'bunzip2')
            symlink('bzip2', 'bzcat')
