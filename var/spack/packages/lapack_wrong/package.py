from spack import *
<<<<<<< HEAD
from subprocess import call
=======
import sys
>>>>>>> 1b75b34eb648a187ed300848422e5125c804b734
import glob

class Lapack(Package):
    """
<<<<<<< HEAD
    Netlib implementation of Lapack. If we end up having different lapack implementations, we should
    turn it into a virtual dependency.
=======
    Netlib implementation of Lapack. If we end up having more Lapack libraries, we should
    turn it into a virtual dependency. 
>>>>>>> 1b75b34eb648a187ed300848422e5125c804b734
    """
    homepage = "http://www.netlib.org/lapack/"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')

<<<<<<< HEAD
    # Parallel is unpredictable - only builds sometimes
    parallel = False

    # virtual
    depends_on("netlib_blas")

    def install(self, spec, prefix):
	# CMake could be used if the build becomes more complex

	call(['cp', 'make.inc.example', 'make.inc'])
	blas = spec['netlib_blas']
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
=======
    # Doesn't always build correctly in parallel
    parallel = False

    # virtual
    depends_on("blas")

    def install(self, spec, prefix):
        # CMake could be used if the build becomes more complex

        symlink('make.inc.example', 'make.inc')

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
>>>>>>> 1b75b34eb648a187ed300848422e5125c804b734
