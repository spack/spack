from spack import *
import os

# Only build certain parts of dwarf because the other ones break.
dwarf_dirs = ['libdwarf', 'dwarfdump2']

class Libdwarf(Package):
    homepage = "http://www.example.com"
    url      = "http://reality.sgiweb.org/davea/libdwarf-20130207.tar.gz"
    md5      = "64b42692e947d5180e162e46c689dfbf"

    depends_on("libelf")

    def clean(self):
        for dir in dwarf_dirs:
            with working_dir(dir):
                if os.path.exists('Makefile'):
                    make('clean')


    def install(self, prefix):
        make.add_default_arg('ARFLAGS=rcs')

        for dir in dwarf_dirs:
            with working_dir(dir):
                #configure("--prefix=%s" % prefix, '--enable-shared')
                configure("--prefix=%s" % prefix)
                make()

        # Dwarf doesn't provide an install.  Annoying.
        mkdirp(bin, include, lib, man1)
        with working_dir('libdwarf'):
            install('libdwarf.a',  lib)
            #install('libdwarf.so', lib)
            install('libdwarf.h',  include)
            install('dwarf.h',     include)

        with working_dir('dwarfdump2'):
            install('dwarfdump',     bin)
            install('dwarfdump.conf', lib)
            install('dwarfdump.1',    man1)
