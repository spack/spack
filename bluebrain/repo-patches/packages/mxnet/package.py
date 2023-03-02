import os

from spack.package import *
from spack.pkg.builtin.mxnet import Mxnet as BuiltinMxnet


class Mxnet(BuiltinMxnet):
    __doc__ = BuiltinMxnet.__doc__

    def patch(self):
        filter_file(r"-Werror", "", "3rdparty/intgemm/CMakeLists.txt")

    def setup_build_environment(self, env):
        super().setup_build_environment(env)
        if "intel-oneapi-mkl" in self.spec:
            # Without this, the build can't find MKL
            # Without MKL, it tries to use OpenBLAS
            # We insist on intel-oneapi-mkl as BLAS provider in packages.yaml
            env.set("MKL_ROOT", os.path.dirname(self.spec["intel-oneapi-mkl"].headers[0]))

    def cmake_args(self):
        args = super().cmake_args()

        if "intel-oneapi-mkl" in self.spec:
            # If we don't set it explicitly, it is blank for some reason,
            # resulting in a failed attempt to install mkldnn to /mkldnn
            # It is possible that this may be necessary even without intel-oneapi-mkl,
            # but we'll solve that if we see it failing.
            args.append(self.define("CMAKE_INSTALL_INCLUDEDIR", "include"))
        return args
