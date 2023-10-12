# flake8: noqa
import os

from spack.package import *
from spack.pkg.builtin.gmsh import Gmsh as BuiltinGmsh


class Gmsh(BuiltinGmsh):
    __doc__ = BuiltinGmsh.__doc__

    version("4.11.1", sha256="c5fe1b7cbd403888a814929f2fd0f5d69e27600222a18c786db5b76e8005b365")

    def setup_run_environment(self, env):
        if os.path.isdir(self.prefix.lib):
            lib_dir = self.prefix.lib
        else:
            lib_dir = self.prefix.lib64
        env.prepend_path("PYTHONPATH", lib_dir)
