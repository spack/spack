from spack.pkg.builtin.cuda import Cuda as BuiltinCuda


class Cuda(BuiltinCuda):
    __doc__ = BuiltinCuda.__doc__

    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        env.append_path("LD_LIBRARY_PATH", self.prefix.extras.CUPTI.lib64)
