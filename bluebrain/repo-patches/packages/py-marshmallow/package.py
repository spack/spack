from spack.package import *
from spack.pkg.builtin.py_marshmallow import PyMarshmallow as BuiltinPyMarshmallow


class PyMarshmallow(BuiltinPyMarshmallow):
    __doc__ = BuiltinPyMarshmallow.__doc__

    version("3.19.0", sha256="90032c0fd650ce94b6ec6dc8dfeb0e3ff50c144586462c389b81a07205bedb78")
