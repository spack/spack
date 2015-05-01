from spack import *

class Uncrustify(Package):
    """Source Code Beautifier for C, C++, C#, ObjectiveC, D, Java, Pawn and VALA"""

    homepage = "http://uncrustify.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/uncrustify/uncrustify/uncrustify-0.61/uncrustify-0.61.tar.gz"

    version('0.61', 'b6140106e74c64e831d0b1c4b6cf7727')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
