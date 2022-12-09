from spack.package import *
from spack.pkg.builtin.libuv_julia import LibuvJulia as BuiltinLibuvJulia


class LibuvJulia(BuiltinLibuvJulia):
    __doc__ = BuiltinLibuvJulia.__doc__

    depends_on("automake@1.16:", type="build")
