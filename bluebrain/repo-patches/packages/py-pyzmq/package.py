from spack import *
from spack.pkg.builtin.py_pyzmq import PyPyzmq as BuiltinPyPyzmq


class PyPyzmq(BuiltinPyPyzmq):
    __doc__ = BuiltinPyPyzmq.__doc__

    version('19.0.0', sha256='d197fc01dc67372066143e5e85dcd3a97ec759ceb76927b7de83cda05eb06006')
    version('18.1.1', sha256='b79afea8701970f0da15218abf9c2c6a39ab3dd8daaef25b868f55f9d9304687')
