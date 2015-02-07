from spack import *

class Libdrm(Package):
    """A userspace  library for  accessing the  DRM, direct
    rendering  manager, on  Linux,  BSD and  other  operating 
    systems that support the  ioctl interface."""

    homepage = "http://dri.freedesktop.org/libdrm/" # no real website...
    url      = "http://dri.freedesktop.org/libdrm/libdrm-2.4.59.tar.gz"

    version('2.4.59', '105ac7af1afcd742d402ca7b4eb168b6')

    # FIXME: Add dependencies if this package requires them.
    # depends_on("foo")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
