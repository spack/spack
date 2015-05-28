from spack import *

class Fastmath(Package):
    """Dummy groupinstall package that installs all packages in the fastmath suite."""

    homepage = "http://redmine.scorec.rpi.edu/projects/fastmath"
    url      = "http://www.netlib.org/blas/blas.tgz"

    version('1.0', '5e99e975f7a1e3ea6abcad7c6e7e42e6')

    depends_on('blas')
    depends_on('lapack')

    def install(self, spec, prefix):
        pwd()
