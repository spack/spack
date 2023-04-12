from spack.package import *
from spack.pkg.builtin.nvhpc import Nvhpc as BuiltinNvhpc


class Nvhpc(BuiltinNvhpc):
    __doc__ = BuiltinNvhpc.__doc__
    # Otherwise module load nvhpc leaves us with a prehistoric binutils
    depends_on("binutils", type="run")
