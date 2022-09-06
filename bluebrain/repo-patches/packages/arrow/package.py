from spack.package import *
from spack.pkg.builtin.arrow import Arrow as BuiltinArrow


class Arrow(BuiltinArrow):
    __doc__ = BuiltinArrow.__doc__

    version('9.0.0', sha256='bb187b4b0af8dcc027fffed3700a7b891c9f76c9b63ad8925b4afb8257a2bb1b')
    version('8.0.0', sha256='19ece12de48e51ce4287d2dee00dc358fbc5ff02f41629d16076f77b8579e272')
    version('7.0.0', sha256='57e13c62f27b710e1de54fd30faed612aefa22aa41fa2c0c3bacd204dd18a8f3')
    version('6.0.1', sha256='826a7dfb246d47862d43b620e0e579f90a4df4c5e571613651dc6397d1e4a435')

    patch('https://github.com/apache/arrow/commit/140f6087b526991248a6e05bdcf16996fbc4421f.patch',
          sha256='ebd5b69d6ae950f2af641699212f5d1de838acfd402c149f20ccc8d45caf3c46',
          when='@4.0.1')

    def cmake_args(self):
        args = super().cmake_args()

        for dep in ('snappy', 'zlib', 'zstd'):
            args.append("-DARROW_WITH_{0}=ON".format(dep.upper()))

        return args
