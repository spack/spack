from spack import *

class Czmq(Package):
    """ A C interface to the ZMQ library """
    homepage = "http://czmq.zeromq.org"
    url      = "https://github.com/zeromq/czmq/archive/v3.0.2.tar.gz"

    version('3.0.2', '23e9885f7ee3ce88d99d0425f52e9be1', url='https://github.com/zeromq/czmq/archive/v3.0.2.tar.gz')

    depends_on('zeromq')

    def install(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
        configure("--prefix=%s" % prefix)

        make()
        make("install")

