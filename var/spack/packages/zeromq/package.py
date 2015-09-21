from spack import *

class Zeromq(Package):
    """ The ZMQ networking/concurrency library and core API """
    homepage = "http://zguide.zeromq.org/"
    url      = "http://download.zeromq.org/zeromq-4.1.2.tar.gz"

    version('4.1.2', '159c0c56a895472f02668e692d122685')
    version('4.1.1', '0a4b44aa085644f25c177f79dc13f253')
    version('4.0.7', '9b46f7e7b0704b83638ef0d461fd59ab')
    version('4.0.6', 'd47dd09ed7ae6e7fd6f9a816d7f5fdf6')
    version('4.0.5', '73c39f5eb01b9d7eaf74a5d899f1d03d')

    depends_on("libsodium")

    def install(self, spec, prefix):
        configure("--with-libsodium","--prefix=%s" % prefix)

        make()
        make("install")
