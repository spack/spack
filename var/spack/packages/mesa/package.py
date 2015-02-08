from spack import *

class Mesa(Package):
    """Mesa is an open-source implementation of the OpenGL 
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "ftp://ftp.freedesktop.org/pub/mesa/10.4.4/MesaLib-10.4.4.tar.gz"

    version('10.4.4', '8d863a3c209bf5116b2babfccccc68ce')

    depends_on("py-mako")
    depends_on("flex")
    depends_on("bison")
    depends_on("libdrm")
    depends_on("dri2proto")
    depends_on("libxcb")
    depends_on("libxshmfence")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure("--prefix=%s" % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
