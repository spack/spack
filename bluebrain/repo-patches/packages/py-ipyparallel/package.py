from spack.package import *
from spack.pkg.builtin.py_ipyparallel import PyIpyparallel as BuiltinPyIpyparallel


class PyIpyparallel(BuiltinPyIpyparallel):
    __doc__ = BuiltinPyIpyparallel.__doc__

    version("8.4.1", sha256="670bbe05755381742e1ea01177dc428ff8f3e94af1f0d5642c9d19f37ca8289b")

    depends_on("py-hatchling", type=("build", "run"), when="@8.4:")
