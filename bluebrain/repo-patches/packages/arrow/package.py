from spack import *
from spack.pkg.builtin.arrow import Arrow as BuiltinArrow


class Arrow(BuiltinArrow):
    __doc__ = BuiltinArrow.__doc__

    version('6.0.1', sha256='826a7dfb246d47862d43b620e0e579f90a4df4c5e571613651dc6397d1e4a435')

    patch('https://github.com/apache/arrow/commit/140f6087b526991248a6e05bdcf16996fbc4421f.patch',
          sha256='ebd5b69d6ae950f2af641699212f5d1de838acfd402c149f20ccc8d45caf3c46',
          when='@4.0.1')

    def cmake_args(self):
        args = super().cmake_args()

        for dep in ('snappy', 'zlib', 'zstd'):
            args.append("-DARROW_WITH_{0}=ON".format(dep.upper()))

        return args
