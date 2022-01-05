from spack import *
from spack.pkg.builtin.cudnn import Cudnn as BuiltinCudnn


class Cudnn(BuiltinCudnn):
    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('LD_LIBRARY_PATH', self.spec.prefix.lib64)
