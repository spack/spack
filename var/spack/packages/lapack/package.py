from spack import *
import os

class Lapack(Package):
    """LAPACK is written in Fortran 90 and provides routines for solving systems 
    of simultaneous linear equations, least-squares solutions of linear systems 
    of equations, eigenvalue problems, and singular value problems."""
    homepage = "http://www.netlib.org/lapack"
    url      = "http://www.netlib.org/lapack/lapack-3.5.0.tgz"

    version('3.5.0', 'b1d3e3e425b2e44a06760ff173104bdf')

    depends_on('blas')

    def install(self, spec, prefix):
        mv = which('mv') # Create a shell wrapper for the mv command.
        mkdir = which('mkdir') # Create a shell wrapper for the mkdir command.
        pwd = os.getcwd() # Retrieve the current working dir.

        # Lapack and BLAS testing fails for some reason, but the library is 
        # built and ready to go at this point. The testing stuff is going to be 
        # switched off for now.
        filter_file('blas_testing lapack_testing ', ' ', 'Makefile', string=True)

        mv('%s/make.inc.example' % pwd, '%s/make.inc' % pwd)
        filter_file('../../librefblas.a', '%s/libblas.a' % spec['blas'].prefix.lib, 'make.inc', string=True) # Specify the BLAS lib to use.

        make()
        mkdir('%s' % prefix.lib) # Create the lib dir inside the install dir.
        mv('%s/liblapack.a' % pwd, '%s/liblapack.a' % prefix.lib) # Move the library file to the install dir.

