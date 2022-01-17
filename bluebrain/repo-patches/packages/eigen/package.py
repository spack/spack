from spack import *
from spack.pkg.builtin.eigen import Eigen as BuiltinEigen


class Eigen(BuiltinEigen):
    __doc__ = BuiltinEigen.__doc__

    # BBP mirrored version with CUDA fixes from CERN (needs until 3.5 release)
    version('3.5a1', sha256='bb43c3d0b5673405c6e40acf5a10d7b853c494a1270bdf197633ba56ca58b715',
            url="https://github.com/BlueBrain/eigen/archive/refs/tags/v3.5-alpha.1.tar.gz")
