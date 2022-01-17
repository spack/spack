from spack import *
from spack.pkg.builtin.py_sh import PySh as BuiltinPySh


class PySh(BuiltinPySh):
    __doc__ = BuiltinPySh.__doc__

    version('1.13.1', sha256='97a3d2205e3c6a842d87ebbc9ae93acae5a352b1bc4609b428d0fd5bb9e286a3')
