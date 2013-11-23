from spack import *
import os

# Only build certain parts of dwarf because the other ones break.
dwarf_dirs = ['libdwarf', 'dwarfdump2']

class Libdwarf(Package):
    homepage = "http://www.prevanders.net/dwarf.html"
    url      = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
    list_url = homepage

    md5      = "64b42692e947d5180e162e46c689dfbf"

    versions = [20070703, 20111030, 20130207]

    depends_on("libelf")


    def clean(self):
        for dir in dwarf_dirs:
            with working_dir(dir):
                if os.path.exists('Makefile'):
                    make('clean')


    def install(self, prefix):
        # dwarf build does not set arguments for ar properly
        make.add_default_arg('ARFLAGS=rcs')

        # Dwarf doesn't provide an install, so we have to do it.
        mkdirp(bin, include, lib, man1)

        with working_dir('libdwarf'):
            configure("--prefix=%s" % prefix, '--enable-shared')
            make()

            install('libdwarf.a',  lib)
            install('libdwarf.so', lib)
            install('libdwarf.h',  include)
            install('dwarf.h',     include)

        with working_dir('dwarfdump2'):
            configure("--prefix=%s" % prefix)

            # This makefile has strings of copy commands that
            # cause a race in parallel
            make(parallel=False)

            install('dwarfdump',     bin)
            install('dwarfdump.conf', lib)
            install('dwarfdump.1',    man1)


    @platform('macosx_10.8_x86_64')
    def install(self, prefix):
        raise UnsupportedPlatformError(
            "libdwarf doesn't currently build on Mac OS X.")
