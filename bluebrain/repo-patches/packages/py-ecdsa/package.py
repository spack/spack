from spack import *
from spack.pkg.builtin.py_ecdsa import PyEcdsa as BuiltinPyEcdsa


class PyEcdsa(BuiltinPyEcdsa):
    version('0.14.1', sha256='64c613005f13efec6541bb0a33290d0d03c27abab5f15fbab20fb0ee162bdd8e')
