from spack.package import *
from spack.pkg.builtin.py_aiohttp import PyAiohttp as BuiltinPyAiohttp


class PyAiohttp(BuiltinPyAiohttp):
    __doc__ = BuiltinPyAiohttp.__doc__

    version("3.8.3", sha256="3828fb41b7203176b82fe5d699e0d845435f2374750a44b480ea6b930f6be269")
