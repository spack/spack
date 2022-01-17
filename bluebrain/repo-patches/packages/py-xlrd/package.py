from spack import *
from spack.pkg.builtin.py_xlrd import PyXlrd as BuiltinPyXlrd


class PyXlrd(BuiltinPyXlrd):
    __doc__ = BuiltinPyXlrd.__doc__

    version('1.0.0', sha256='0ff87dd5d50425084f7219cb6f86bb3eb5aa29063f53d50bf270ed007e941069')
