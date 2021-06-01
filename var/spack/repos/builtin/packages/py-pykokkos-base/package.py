# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# ----------------------------------------------------------------------------

from spack import *


class PyPykokkosBase(CMakePackage, PythonPackage):
    """Minimal set of bindings for Kokkos interoperability with Python
    (initialize, finalize, View, DynRankView, Kokkos-tools)"""

    homepage = "https://github.com/kokkos/pykokkos-base.git"
    git = "https://github.com/kokkos/pykokkos-base.git"
    maintainers = ["jrmadsen"]

    version("main", branch="main", submodules=False)
    version(
        "0.0.5", commit="45f6e892c007ab124fabb3a545f4744537eafb55", submodules=False
    )
    version(
        "0.0.4", commit="2efe1220d0128d3f2d371c9ed5234c4978d73a77", submodules=False
    )
    version(
        "0.0.3", commit="4fe4421ac624ba2efe1eee265153e690622a18a5", submodules=False
    )

    variant(
        "layouts",
        default=True,
        description="Build Kokkos View/DynRankView with layout variants",
    )
    variant(
        "memory_traits",
        default=True,
        description="Build Kokkos View/DynRankView with memory trait variants",
    )
    variant(
        "view_ranks",
        default="4",
        description="Max Kokkos View dimensions",
        values=("1", "2", "3", "4", "5", "6", "7"),
        multi=False,
    )

    extends("python")
    depends_on("cmake@3.16:", type="build")
    depends_on("py-pybind11", type="build")
    depends_on("kokkos@3.4.00:", type=("build", "run"))
    depends_on("python@3:", type=("build", "run"))

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DENABLE_INTERNAL_KOKKOS=OFF",
            "-DENABLE_INTERNAL_PYBIND11=OFF",
            "-DPYTHON_EXECUTABLE={0}".format(spec["python"].command.path),
            "-DPython3_EXECUTABLE={0}".format(spec["python"].command.path),
            "-DENABLE_VIEW_RANKS={0}".format(spec.variants["view_ranks"].value),
        ]

        for dep in ("layouts", "memory_traits"):
            args.append(
                "-DENABLE_{0}={1}".format(
                    dep.upper(), "ON" if "+{0}".format(dep) in spec else "OFF"
                )
            )

        return args
