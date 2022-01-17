from spack import *
from spack.pkg.builtin.libwebsockets import Libwebsockets as BuiltinLibwebsockets


class Libwebsockets(BuiltinLibwebsockets):
    __doc__ = BuiltinLibwebsockets.__doc__

    variant('libuv', default=False, description='Build with libuv support')

    version('3.1.0', 'db948be74c78fc13f1f1a55e76707d7baae3a1c8f62b625f639e8f2736298324')
    version('3.0.1', 'cb0cdd8d0954fcfd97a689077568f286cdbb44111883e0a85d29860449c47cbf')

    depends_on('libuv', when='+libuv')

    def cmake_args(self):
        args = ['-DLWS_WITH_SHARED=ON', '-DLWS_WITH_STATIC=OFF',
                '-DLWS_LINK_TESTAPPS_DYNAMIC=ON']
        if 'libuv' in self.spec:
            args += ['-DLWS_WITH_LIBUV=ON']

        return args
