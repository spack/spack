from spack.package import *
from spack.pkg.builtin.py_pytz import PyPytz as BuiltinPyPytz


class PyPytz(BuiltinPyPytz):
    __doc__ = BuiltinPyPytz.__doc__

    version("2022.7.1", sha256="01a0681c4b9684a28304615eba55d1ab31ae00bf68ec157ec3708a8182dbbcd0")
