import os

from spack import *
from spack.pkg.builtin.totalview import Totalview as BuiltinTotalview


class Totalview(BuiltinTotalview):
    __doc__ = BuiltinTotalview.__doc__

    version('2021.1.16',
            sha256='4c51c7b6ab6b6afa7635ba2e9fc3b0ef833806f775a0ad0da26b13d6320625dd')

    resource(
        name='x86_64',
        url='file://{0}/totalview_2020.3.11_linux_x86-64.tar'.format(os.getcwd()),
        destination='.',
        sha256='129e991d3ce4df9f9f04adbf79b62d3c2706d7732ec305f3d3c97a6b4d1f5a13',
        when='@2021.1.16 target=x86_64:')
