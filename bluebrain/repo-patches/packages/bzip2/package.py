from spack import *
from spack.pkg.builtin.bzip2 import Bzip2 as BuiltinBzip2


class Bzip2(BuiltinBzip2):
    def patch(self):
        super().patch()
        filter_file(r'(-o bzip2 bzip2.o) -L. -lbz2', r'\1 libbz2.a', 'Makefile')

    def install(self, spec, prefix):
        # Build the dynamic library first
        if '+shared' in spec:
            make('-f', 'Makefile-libbz2_so')

        # Build the static library and everything else
        make()
        make('install', 'PREFIX={0}'.format(prefix))

        if '+shared' in spec:
            # install('bzip2-shared', join_path(prefix.bin, 'bzip2'))

            v1, v2, v3 = (self.spec.version.up_to(i) for i in (1, 2, 3))
            if 'darwin' in self.spec.architecture:
                lib = 'libbz2.dylib'
                lib1, lib2, lib3 = ('libbz2.{0}.dylib'.format(v)
                                    for v in (v1, v2, v3))
            else:
                lib = 'libbz2.so'
                lib1, lib2, lib3 = ('libbz2.so.{0}'.format(v)
                                    for v in (v1, v2, v3))

            install(lib3, join_path(prefix.lib, lib3))
            with working_dir(prefix.lib):
                for libname in (lib, lib1, lib2):
                    symlink(lib3, libname)

        with working_dir(prefix.bin):
            force_remove('bunzip2', 'bzcat')
            symlink('bzip2', 'bunzip2')
            symlink('bzip2', 'bzcat')
