from spack import *


class Patchelf(Package):
    """PatchELF is a small utility to modify the dynamic linker and RPATH of ELF executables."""

    homepage = "https://nixos.org/patchelf.html"
    def url_for_version(self, version):
        return "http://nixos.org/releases/patchelf/" \
            + "patchelf-%s/patchelf-%s.tar.gz" % (version, version)

    list_url = "http://nixos.org/releases/patchelf/"
    list_depth = 2

    version('0.9', '3c265508526760f233620f35d79c79fc')
    version('0.8', '407b229e6a681ffb0e2cdd5915cb2d01')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
