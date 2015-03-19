from spack import *
from subprocess import call
import sys
import glob

class Lapack(Package):
    """
    Netlib implementation of Lapack. If we end up having more Lapack libraries, we should
    turn it into a virtual dependency. 
    """
    homepage = "http://www.netlib.org/lapack/"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')

    # Doesn't always build correctly in parallel
    parallel = False

    # virtual
    depends_on("blas")

    def install(self, spec, prefix):
        # CMake could be used if the build becomes more complex

        call(['cp', 'make.inc.example', 'make.inc'])

        # Retrieves name of package that satisifies 'blas' virtual dependency
        blas_name = next(m for m in ('netlib_blas', 'atlas') if m in spec)
        blas_spec = spec[blas_name]
        blas_object_path = blas_spec.prefix.lib + '/blas.a'

        # The blas dependency must provide a 'blas.a' - but this is not gauranteed right now
        # So maybe we should check if it exists first... maybe...
        make('BLASLIB="%s"' % blas_object_path)

        # Manual install since no method provided
        # Should probably be changed so only one external call is made
        # Can install be used on a list of files? 
        mkdirp(prefix.lib)
        for file in glob.glob('*.a'):
            install(file, prefix.lib)
