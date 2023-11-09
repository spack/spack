# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lemon(CMakePackage):
    """LEMON stands for Library for Efficient Modeling and Optimization in
    Networks. It is a C++ template library providing efficient implementations
    of common data structures and algorithms with focus on combinatorial
    optimization tasks connected mainly with graphs and networks."""

    homepage = "https://lemon.cs.elte.hu/trac/lemon"
    url = "https://lemon.cs.elte.hu/pub/sources/lemon-1.3.1.tar.gz"

    version("1.3.1", sha256="71b7c725f4c0b4a8ccb92eb87b208701586cf7a96156ebd821ca3ed855bad3c8")

    variant("coin", default=False, description="Enable Coin")
    variant("ilog", default=False, description="Enable ILOG")
    variant("glpk", default=True, description="build with glpk support")
    variant(
        "lp_backend",
        default="glpk",
        description="Set default LP solver backend",
        values=("glpk", "cplex", "clp"),
        multi=False,
    )
    variant(
        "mip_backend",
        default="glpk",
        description="Set default LP solver backend",
        values=("glpk", "cplex", "clp"),
        multi=False,
    )

    depends_on("glpk", when="+glpk")
    depends_on("glpk", when="lp_backend=glpk")
    depends_on("cplex", when="lp_backend=cplex")
    depends_on("clp", when="lp_backend=clp")
    depends_on("glpk", when="mip_backend=glpk")
    depends_on("cplex", when="mip_backend=cplex")
    depends_on("clp", when="mip_backend=clp")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.extend(
            [
                "-DLEMON_ENABLE_COIN={0}".format("YES" if "+coin" in spec else "NO"),
                "-DLEMON_ENABLE_ILOG={0}".format("YES" if "+ilog" in spec else "NO"),
                "-DLEMON_ENABLE_GLPK={0}".format("YES" if "+glpk" in spec else "NO"),
                "-DLEMON_DEFAULT_LP={0}".format(spec.variants["lp_backend"].value.upper()),
                "-DLEMON_DEFAULT_MIP={0}".format(spec.variants["mip_backend"].value.upper()),
            ]
        )
        return args
