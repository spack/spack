from spack import *
from spack.pkg.builtin.py_sympy import PySympy as BuiltinPySympy


class PySympy(BuiltinPySympy):
    __doc__ = BuiltinPySympy.__doc__

    version('1.9', sha256='c7a880e229df96759f955d4f3970d4cabce79f60f5b18830c08b90ce77cd5fdc')
