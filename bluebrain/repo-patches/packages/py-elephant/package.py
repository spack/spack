from spack import *
from spack.pkg.builtin.py_elephant import PyElephant as BuiltinPyElephant


class PyElephant(BuiltinPyElephant):
    __doc__ = BuiltinPyElephant.__doc__

    version('0.6.4', sha256='b8c5f2c00ad3249e1fe428d0b8a1dbcaee4a69464481f5f8fd55d2f7f22c45a3')
