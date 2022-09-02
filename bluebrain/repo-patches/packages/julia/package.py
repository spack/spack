from spack.pkg.builtin.julia import Julia as BuiltinJulia


class Julia(BuiltinJulia):
    __doc__ = BuiltinJulia.__doc__

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib.julia)
