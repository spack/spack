from spack import *
from spack.pkg.builtin.py_pip import PyPip as BuiltinPyPip


class PyPip(BuiltinPyPip):
    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec.prefix.bin)
