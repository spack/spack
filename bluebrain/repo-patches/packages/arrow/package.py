from spack.package import *
from spack.pkg.builtin.arrow import Arrow as BuiltinArrow


class Arrow(BuiltinArrow):
    __doc__ = BuiltinArrow.__doc__

    def cmake_args(self):
        args = super().cmake_args()

        if not self.spec.satisfies("^re2"):
            args.append(self.define("ARROW_WITH_RE2", False))
        if not self.spec.satisfies("^utf8proc"):
            args.append(self.define("ARROW_WITH_UTF8PROC", False))

        return args
