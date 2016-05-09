from spack import *

class Libuv(Package):
    """Multi-platform library with a focus on asynchronous IO"""
    homepage = "http://libuv.org"
    url      = "https://github.com/libuv/libuv/archive/v1.9.0.tar.gz"

    version('1.9.0', '14737f9c76123a19a290dabb7d1cd04c')

    depends_on('automake')
    depends_on('autoconf')
    depends_on('libtool')

    def install(self, spec, prefix):
        bash = which("bash")
        bash('autogen.sh')
        configure('--prefix=%s' % prefix)

        make()
        make("check")
        make("install")
