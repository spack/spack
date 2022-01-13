from spack import *
from spack.pkg.builtin.eztrace import Eztrace as BuiltinEztrace


class Eztrace(BuiltinEztrace):
    depends_on('binutils')
