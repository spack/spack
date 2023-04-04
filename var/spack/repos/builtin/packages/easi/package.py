# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Easi(CMakePackage):
    """easi is a library for the Easy Initialization of models
    in three (or less or more) dimensional domains.
    """

    homepage = "https://easyinit.readthedocs.io"
    git = "https://github.com/SeisSol/easi.git"

    maintainers("ravil-mobile", "Thomas-Ulrich", "krenzland", "ThrudPrimrose")

    version("develop", branch="master")
    version("1.2.0", tag="v1.2.0")
    version("1.1.2", tag="v1.1.2")

    variant("asagi", default=True, description="build with ASAGI support")
    variant(
        "jit",
        default="impalajit,lua",
        description="build with JIT support",
        values=("impalajit", "impalajit-llvm", "lua"),
        multi=True,
    )

    depends_on("asagi +mpi +mpi3", when="+asagi")
    depends_on("yaml-cpp@0.6.2")

    depends_on("impalajit@llvm-1.0.0", when="jit=impalajit-llvm")
    depends_on("lua@5.3.2", when="jit=lua")
    depends_on("impalajit", when="jit=impalajit")

    conflicts("jit=impalajit", when="jit=impalajit-llvm")
    conflicts("jit=impalajit-llvm", when="jit=impalajit")

    conflicts("jit=impalajit", when="target=aarch64:")
    conflicts("jit=impalajit", when="target=ppc64:")
    conflicts("jit=impalajit", when="target=ppc64le:")
    conflicts("jit=impalajit", when="target=riscv64:")

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("ASAGI", "asagi"))
        spec = self.spec
        if "jit=impalajit" in spec or "jit=impalajit-llvm" in spec:
            args.append(self.define("IMPALAJIT", True))
            backend_type = "llvm" if "jit=impalajit-llvm" in spec else "original"
            args.append(self.define("IMPALAJIT_BACKEND", backend_type))
        else:
            args.append(self.define("IMPALAJIT", False))

        if "jit=lua" in spec:
            args.append(self.define("LUA", True))

        return args
