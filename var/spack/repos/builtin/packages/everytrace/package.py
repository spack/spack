# Install with:
#	   spack diy --skip-patch everytrace@devel +fortran +mpi ^openmpi

from spack import *
import llnl.util.tty as tty
import os

class Everytrace(CMakePackage):
	"""Get stack trace EVERY time a program exits."""

	homepage = "https://github.com/citibeth/everytrace"
	url		 = "https://github.com/citibeth/everytrace/tarball/dev"

	version('devel', '0123456789abcdef0123456789abcdef')

	variant('mpi', default=True, description='Enables MPI parallelism')
	variant('fortran', default=True, description='Enable use with Fortran programs')

	depends_on('mpi', when='+mpi')
	depends_on('cmake')

	def config_args(self, spec, prefix):
		return [
			'-DUSE_MPI=%s' % ('YES' if '+mpi' in spec else 'NO'),
			'-DUSE_FORTRAN=%s' % ('YES' if '+fortran' in spec else 'NO')]
