# flake8: noqa
import os

from spack.package import *
from spack.pkg.builtin.gmsh import Gmsh as BuiltinGmsh


class Gmsh(BuiltinGmsh):
    __doc__ = BuiltinGmsh.__doc__

    version("4.12.2", sha256="13e09d9ca8102e5c40171d6ee150c668742b98c3a6ca57f837f7b64e1e2af48f")
    version("4.11.1", sha256="c5fe1b7cbd403888a814929f2fd0f5d69e27600222a18c786db5b76e8005b365")

    def setup_run_environment(self, env):
        sitedir = os.path.dirname(find(self.prefix, "gmsh.py")[0])
        env.prepend_path("PYTHONPATH", sitedir)
