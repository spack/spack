from spack import *
from spack.pkg.builtin.cubew import Cubew as BuiltinCubew


class Cubew(BuiltinCubew):
    def configure_args(self):
        configure_args = super().configure_args()

        if spec.satisfies('%intel'):
            configure_args.append('--with-nocross-compiler-suite=intel')
        elif spec.satisfies('%pgi'):
            configure_args.append('--with-nocross-compiler-suite=pgi')
        elif spec.satisfies('%clang'):
            configure_args.append('--with-nocross-compiler-suite=clang')

        return configure_args
