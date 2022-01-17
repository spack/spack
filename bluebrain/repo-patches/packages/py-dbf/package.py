from spack import *
from spack.pkg.builtin.py_dbf import PyDbf as BuiltinPyDbf


class PyDbf(BuiltinPyDbf):
    __doc__ = BuiltinPyDbf.__doc__

    version('0.97.11', sha256='8aa5a73d8b140aa3c511a3b5b204a67d391962e90c66b380dd048fcae6ddbb68')
