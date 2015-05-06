from spack import *
from subprocess import call
import glob

class Lapack(Package):
    """
    Netlib implementation of Lapack. If we end up having different lapack implementations, we should
    turn it into a virtual dependency.
    """
    homepage = "http://www.netlib.org/lapack/"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')

    # Parallel is unpredictable - only builds sometimes
    parallel = False

    # virtual
    depends_on("blas")

    def install(self, spec, prefix):
	# CMake could be used if the build becomes more complex

	call(['cp', 'make.inc.example', 'make.inc'])
	blas = spec['blas']
	# blas_path = new_path(blas.prefix.lib, 'blas_path')
	
	# The blas dependency must provide a 'blas.a' - but this is not gauranteed right now
	# So maybe we should check if it exists first... maybe...
        make('BLASLIB="%s/%s"' % (blas.prefix.lib, 'blas.a'))
	
	# Manual install since no method provided
	# Should probably be changed so only one external call is made
	# TODO: find out if install can be used on multiple files
	mkdirp(prefix.lib)
	for file in glob.glob('*.a'):
		install(file, prefix.lib)
