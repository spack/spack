from spack.package import *
from spack.pkg.builtin.py_torch import PyTorch as BuiltinPyTorch


class PyTorch(BuiltinPyTorch):
    __doc__ = BuiltinPyTorch.__doc__

    version("1.13.1", tag="v1.13.1", submodules=True)

    # Dependencies found in requirements.txt
    depends_on("py-sympy", when="@1.13:", type=("build", "run"))
    depends_on("py-filelock", when="@1.13:", type=("build", "run"))
    depends_on("py-networkx", when="@1.13:", type=("build", "run"))
    depends_on("py-jinja2", when="@1.13:", type=("build", "run"))

    # Build fails without this one marked as a link dependency!
    depends_on("glog", type=("build", "link", "run"))

    depends_on("cuda@:11", when="@1.13:+cuda", type=("build", "link", "run"))

    def setup_build_environment(self, env):
        super().setup_build_environment(env)

        # Avoid ImportError: no module named site
        env.unset("PYTHONHOME")
