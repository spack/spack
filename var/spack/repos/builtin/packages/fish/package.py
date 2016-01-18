from spack import *

class Fish(Package):
    """fish is a smart and user-friendly command line shell for OS X, Linux, and
    the rest of the family.
    """

    homepage = "http://fishshell.com/"
    url      = "http://fishshell.com/files/2.2.0/fish-2.2.0.tar.gz"
    list_url = homepage

    version('2.2.0', 'a76339fd14ce2ec229283c53e805faac48c3e99d9e3ede9d82c0554acfc7b77a')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
