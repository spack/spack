from spack.pkg.builtin.py_pip import PyPip as BuiltinPyPip


class PyPip(BuiltinPyPip):
    __doc__ = BuiltinPyPip.__doc__

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec.prefix.bin)
