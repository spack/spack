from spack import *

class Patchelf(Package):
    """PatchELF is a small utility to modify the dynamic linker and RPATH of ELF executables."""

    homepage = "https://nixos.org/patchelf.html"
    url      = "http://nixos.org/releases/patchelf/patchelf-0.8/patchelf-0.8.tar.gz"
    list_url = "http://nixos.org/releases/patchelf/"
    list_depth = 2

    version('0.8', '407b229e6a681ffb0e2cdd5915cb2d01')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
