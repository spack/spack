from spack import *

class Libelf(Package):
    homepage = "http://www.mr511.de/software/english.html"
    url      = "http://www.mr511.de/software/libelf-0.8.13.tar.gz"
    md5      = "4136d7b4c04df68b686570afa26988ac"

    def install(self, prefix):
        configure("--prefix=%s" % prefix,
                  "--disable-dependency-tracking",
                  "--disable-debug")
        make()
        make("install")
