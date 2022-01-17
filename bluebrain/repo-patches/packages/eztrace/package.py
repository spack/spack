from spack import *
from spack.pkg.builtin.eztrace import Eztrace as BuiltinEztrace


class Eztrace(BuiltinEztrace):
    __doc__ = BuiltinEztrace.__doc__

    depends_on('binutils')
