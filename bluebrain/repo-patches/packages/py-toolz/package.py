from spack import *
from spack.pkg.builtin.py_toolz import PyToolz as BuiltinPyToolz


class PyToolz(BuiltinPyToolz):
    version('0.11.1', sha256='c7a47921f07822fe534fb1c01c9931ab335a4390c782bd28c6bcc7c2f71f3fbf')
