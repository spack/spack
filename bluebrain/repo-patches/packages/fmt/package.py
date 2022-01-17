from spack.pkg.builtin.fmt import Fmt as BuiltinFmt


class Fmt(BuiltinFmt):
    __doc__ = BuiltinFmt.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.extend([
            '-DFMT_DOC=OFF',
            '-DFMT_TEST=OFF'
        ])
        return args
