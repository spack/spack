from spack import *

class LibjsonC(Package):
    """ A JSON implementation in C """
    homepage = "https://github.com/json-c/json-c/wiki"
    url      = "https://s3.amazonaws.com/json-c_releases/releases/json-c-0.11.tar.gz"

    version('0.11', 'aa02367d2f7a830bf1e3376f77881e98')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
