from spack import *

class Mesa(Package):
    """Mesa is an open-source implementation of the OpenGL
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "ftp://ftp.freedesktop.org/pub/mesa/older-versions/8.x/8.0.5/MesaLib-8.0.5.tar.gz"
    # url      = "ftp://ftp.freedesktop.org/pub/mesa/10.4.4/MesaLib-10.4.4.tar.gz"

    # version('10.4.4', '8d863a3c209bf5116b2babfccccc68ce')
    version('8.0.5', 'cda5d101f43b8784fa60bdeaca4056f2')

    # mesa 7.x, 8.x, 9.x
    depends_on("libdrm@2.4.33")
    depends_on("llvm@3.0")
    depends_on("libxml2")

    # patch("llvm-fixes.patch") # using newer llvm

    # mesa 10.x
    # depends_on("py-mako")
    # depends_on("flex")
    # depends_on("bison")
    # depends_on("dri2proto")
    # depends_on("libxcb")
    # depends_on("libxshmfence")


    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
