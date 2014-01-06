from spack import *
import os

# Only build certain parts of dwarf because the other ones break.
dwarf_dirs = ['libdwarf', 'dwarfdump2']

class Libdwarf(Package):
    homepage = "http://www.prevanders.net/dwarf.html"
    url      = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
    list_url = homepage

    versions = { 20130729 : "64b42692e947d5180e162e46c689dfbf",
                 20130207 : 'foobarbaz',
                 20111030 : 'foobarbaz',
                 20070703 : 'foobarbaz' }

    depends_on("libelf")

    def install(self, spec, prefix):
        pass
