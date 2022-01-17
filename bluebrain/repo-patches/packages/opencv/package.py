from spack import *
from spack.pkg.builtin.opencv import Opencv as BuiltinOpencv


class Opencv(BuiltinOpencv):
    __doc__ = BuiltinOpencv.__doc__

    version('4.5.4',    sha256='c20bb83dd790fc69df9f105477e24267706715a9d3c705ca1e7f613c7b3bad3d')
    version('4.5.3',    sha256='77f616ae4bea416674d8c373984b20c8bd55e7db887fd38c6df73463a0647bab')
