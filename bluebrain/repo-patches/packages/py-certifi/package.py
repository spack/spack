from spack import *
from spack.pkg.builtin.py_certifi import PyCertifi as BuiltinPyCertifi


class PyCertifi(BuiltinPyCertifi):
    __doc__ = BuiltinPyCertifi.__doc__

    patch('bbp_root_ca.patch', when='@2021.10.8')
