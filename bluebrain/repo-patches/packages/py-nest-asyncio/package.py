from spack import *
from spack.pkg.builtin.py_nest_asyncio import PyNestAsyncio as BuiltinPyNestAsyncio


class PyNestAsyncio(BuiltinPyNestAsyncio):
    __doc__ = BuiltinPyNestAsyncio.__doc__

    version('1.5.1', sha256='afc5a1c515210a23c461932765691ad39e8eba6551c055ac8d5546e69250d0aa')
