from spack import *

class PyMpi4py(Package):
    """This package provides Python bindings for the Message Passing Interface (MPI) standard. It is implemented on top of the MPI-1/MPI-2 specification and exposes an API which grounds on the standard MPI-2 C++ bindings."""
    homepage = "https://pypi.python.org/pypi/mpi4py"
    url      = "https://pypi.python.org/packages/source/m/mpi4py/mpi4py-1.3.1.tar.gz"

    version('1.3.1', 'dbe9d22bdc8ed965c23a7ceb6f32fc3c')
    extends('python')
    depends_on('py-setuptools')
    depends_on('mpi')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
