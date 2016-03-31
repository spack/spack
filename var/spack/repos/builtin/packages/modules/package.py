from spack import *

class Modules(Package):
    """ The Environment Modules package provides for the dynamic modification of a user's environment via modulefiles. """

    homepage = "http://modules.sf.net"
    url      = "http://downloads.sourceforge.net/project/modules/Modules/modules-3.2.10/modules-3.2.10.tar.gz"

    version('3.2.10', '8b097fdcb90c514d7540bb55a3cb90fb')

    depends_on("tcl")

    def install(self, spec, prefix):

	options = ['--prefix=%s' % prefix, 
                   '--disable-debug',
                   '--disable-dependency-tracking',
                   '--disable-silent-rules',
                   '--disable-versioning', 
                   '--datarootdir=%s' % prefix.share,
                   'CPPFLAGS=-DUSE_INTERP_ERRORLINE']

        configure(*options)
        make()
        make("install")
