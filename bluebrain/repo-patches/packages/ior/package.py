from spack import *
from spack.pkg.builtin.ior import Ior as BuiltinIor


class Ior(BuiltinIor):
    __doc__ = BuiltinIor.__doc__

    variant('ime',   default=False, description='support IO with IME backend')

    def configure_args(self):
        config_args = super().configure_args()
        if '+ime' in self.spec:
            config_args.append('--with-ime')
        else:
            config_args.append('--without-ime')
        return config_args
