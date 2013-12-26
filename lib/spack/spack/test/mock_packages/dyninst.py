from spack import *

class Dyninst(Package):
    homepage = "https://paradyn.org"
    url      = "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.1.2/DyninstAPI-8.1.2.tgz"
    list_url = "http://www.dyninst.org/downloads/dyninst-8.x"

    versions = {
        '8.1.2' : 'bf03b33375afa66fe0efa46ce3f4b17a',
        '8.1.1' : '1f8743e3a5662b25ce64a7edf647e77d' }

    depends_on("libelf")
    depends_on("libdwarf")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
