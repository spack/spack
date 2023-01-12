from spack.package import *
from spack.pkg.builtin.py_lazy import PyLazy as BuiltinPyLazy


class PyLazy(BuiltinPyLazy):
    __doc__ = BuiltinPyLazy.__doc__

    version("1.4", sha256="2c6d27a5ab130fb85435320651a47403adcb37ecbcc501b0c6606391f65f5b43")
