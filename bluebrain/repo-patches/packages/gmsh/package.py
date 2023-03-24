# flake8: noqa
import os

from spack.package import *
from spack.pkg.builtin.gmsh import Gmsh as BuiltinGmsh


class Gmsh(BuiltinGmsh):
    __doc__ = BuiltinGmsh.__doc__

    def setup_run_environment(self, env):
        if os.path.isdir(self.prefix.lib):
            lib_dir = self.prefix.lib
        else:
            lib_dir = self.prefix.lib64
        env.prepend_path("PYTHONPATH", lib_dir)
