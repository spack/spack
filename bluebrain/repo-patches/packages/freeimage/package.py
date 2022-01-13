from spack import *
from spack.pkg.builtin.freeimage import Freeimage as BuiltinFreeimage


class Freeimage(BuiltinFreeimage):
    def edit(self, spec, prefix):
        super().edit(spec, prefix)
        env["INCDIR"] = prefix.join("include")
        env["INSTALLDIR"] = prefix.join("lib")

    def patch(self):
        # Somehow defaults to C++1&
        filter_file(r'(CXXFLAGS \?=)', r'\1 --std=c++14', 'Makefile.gnu')
