from spack import *

class PyPypar(Package):
    """Pypar is an efficient but easy-to-use module that allows programs written in Python to run in parallel on multiple processors and communicate using MPI."""
    homepage = "http://code.google.com/p/pypar/"
    url      = "https://pypar.googlecode.com/files/pypar-2.1.5_108.tgz"

    version('2.1.5_108', '7a1f28327d2a3b679f9455c843d850b8', url='https://pypar.googlecode.com/files/pypar-2.1.5_108.tgz')
    extends('python')
    depends_on('mpi')

    def install(self, spec, prefix):
        with working_dir('source'):
            python('setup.py', 'install', '--prefix=%s' % prefix)
