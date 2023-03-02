from spack.package import *
from spack.pkg.builtin.py_pyshacl import PyPyshacl as BuiltinPyPyshacl


class PyPyshacl(BuiltinPyPyshacl):
    __doc__ = BuiltinPyPyshacl.__doc__

    def patch(self):
        if self.spec.satisfies("@0.17.2:0.20.0"):
            filter_file("\^5.2.3,<7", ">=5.2.3,<7", "pyproject.toml")
