# Install with:
#	   spack diy --skip-patch everytrace@devel +fortran +mpi ^openmpi

from spack import *
import llnl.util.tty as tty
import os

class Everytrace(CMakePackage):
	"""Get stack trace EVERY time a program exits."""

	homepage = "https://github.com/citibeth/everytrace"
	url		 = "https://github.com/citibeth/everytrace/tarball/0.1.0"

	version('0.1.0', '295b10b2bd1b40712b6475dbb124b0ce')

	variant('mpi', default=True, description='Enables MPI parallelism')
	variant('fortran', default=True, description='Enable use with Fortran programs')

	depends_on('mpi', when='+mpi')
	depends_on('cmake')

	def config_args(self, spec, prefix):
		return [
			'-DUSE_MPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
			'-DUSE_FORTRAN=%s' % ('YES' if '+fortran' in spec else 'NO')]
