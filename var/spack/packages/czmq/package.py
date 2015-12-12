from spack import *
import os

class Czmq(Package):
    """ A C interface to the ZMQ library """
    homepage = "http://czmq.zeromq.org"
    url      = "https://github.com/zeromq/czmq/archive/v3.0.2.tar.gz"

    version('3.0.2', '23e9885f7ee3ce88d99d0425f52e9be1', url='https://github.com/zeromq/czmq/archive/v3.0.2.tar.gz')

    depends_on('libtool')
    depends_on('automake')
    depends_on('autoconf')
    depends_on('pkg-config')
    depends_on('zeromq')

    def install(self, spec, prefix):
        bash = which("bash")
        # Work around autogen.sh oddities
        # bash("./autogen.sh")
        mkdirp("config")
        autoreconf = which("autoreconf")
        autoreconf("--install", "--verbose", "--force",
        "-I", "config",
        "-I", os.path.join(spec['pkg-config'].prefix, "share", "aclocal"),
        "-I", os.path.join(spec['automake'].prefix, "share", "aclocal"),
        "-I", os.path.join(spec['libtool'].prefix, "share", "aclocal"),
        )
        configure("--prefix=%s" % prefix)

        make()
        make("install")

