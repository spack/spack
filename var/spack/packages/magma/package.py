from spack import *
import os
from subprocess import call

class Magma(Package):
    """a dense linear algebra library similar to LAPACK but for heterogeneous/hybrid architectures"""
    homepage = "http://icl.cs.utk.edu/magma/index.html"
    url      = "http://icl.cs.utk.edu/projectsfiles/magma/downloads/magma-1.6.2.tar.gz"

    # Install from sources
    if os.environ.has_key("MORSE_MAGMA_TAR") and os.environ.has_key("MORSE_MAGMA_TAR_MD5"):
        version('local', '%s' % os.environ['MORSE_MAGMA_TAR_MD5'],
                url = "file://%s" % os.environ['MORSE_MAGMA_TAR'])
    else:
        version('1.6.2', 'ba22d397a28a957c090b43ba895cb735')
        version('1.6.1', 'ae0fe7fefe2f27847b2f5a48b6fab429')
        version('1.6.0', '10c01eec8763878c85abb83274f65426')
        version('1.5.0', '18074e2e5244924730063fe0f694abca')
        version('1.4.1', '19af5b2a682f43049ed3318cb341cf88')

    # depends_on("cblas")
    # depends_on("lapack")
    # depends_on("cuda")

    def install(self, spec, prefix):
        spack_root=os.environ['SPACK_ROOT']
        print spack_root+"/var/spack/packages/magma/make.inc.mkl-gcc"
        call(["cp", spack_root+"/var/spack/packages/magma/make.inc.mkl-gcc", "."])
        call(["ln", "-s", "make.inc.mkl-gcc", "make.inc"])
        make("-i")
        call(["make", "--ignore-errors", "install", "prefix=%s" % prefix])
