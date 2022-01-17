from spack import *
from spack.pkg.builtin.cube import Cube as BuiltinCube


class Cube(BuiltinCube):
    __doc__ = BuiltinCube.__doc__

    def configure_args():
        configure_args = super().configure_args()

        if self.spec.satisfies('%intel'):
            configure_args.append('--with-nocross-compiler-suite=intel')
        elif self.spec.satisfies('%pgi'):
            configure_args.append('--with-nocross-compiler-suite=pgi')
        elif self.spec.satisfies('%clang'):
            configure_args.append('--with-nocross-compiler-suite=clang')

        return configure_args
