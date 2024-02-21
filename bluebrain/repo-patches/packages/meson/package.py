from spack.package import *
from spack.pkg.builtin.meson import Meson as BuiltinMeson


class Meson(BuiltinMeson):
    __doc__ = BuiltinMeson.__doc__

    patch("pgmath.patch", when="target=aarch64:")
