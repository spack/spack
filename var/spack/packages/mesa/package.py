from spack import *

class Mesa(Package):
    """Mesa is an open-source implementation of the OpenGL 
    specification - a system for rendering interactive 3D graphics."""

    homepage = "http://www.mesa3d.org"
    url      = "ftp://ftp.freedesktop.org/pub/mesa/older-versions/7.x/7.11.2/MesaLib-7.11.2.tar.gz"
    # url      = "ftp://ftp.freedesktop.org/pub/mesa/10.4.4/MesaLib-10.4.4.tar.gz"

    # version('10.4.4', '8d863a3c209bf5116b2babfccccc68ce')
    version('7.11.2', 'b9e84efee3931c0acbccd1bb5a860554')

    depends_on("py-mako")
    depends_on("flex")
    depends_on("bison")
    depends_on("libdrm")
    depends_on("dri2proto")
    depends_on("libxcb")
    depends_on("libxshmfence")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
