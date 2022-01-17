from spack import *
from spack.pkg.builtin.py_pyrsistent import PyPyrsistent as BuiltinPyPyrsistent


class PyPyrsistent(BuiltinPyPyrsistent):
    __doc__ = BuiltinPyPyrsistent.__doc__

    version('0.16.0', sha256='28669905fe725965daa16184933676547c5bb40a5153055a8dee2a4bd7933ad3')
