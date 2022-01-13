from spack import *
from spack.pkg.builtin.arrow import Arrow as BuiltinArrow


class Arrow(BuiltinArrow):
    patch('https://github.com/apache/arrow/commit/140f6087b526991248a6e05bdcf16996fbc4421f.patch',
          sha256='ebd5b69d6ae950f2af641699212f5d1de838acfd402c149f20ccc8d45caf3c46',
          when='@4.0.1')
