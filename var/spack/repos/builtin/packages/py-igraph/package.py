# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIgraph(PythonPackage):
    """Python interface to the igraph high performance graph library,
    primarily aimed at complex network research and analysis."""

    homepage = "https://github.com/igraph/python-igraph"
    pypi = "igraph/igraph-0.10.6.tar.gz"

    version("0.10.6", sha256="76f7aad294514412f835366a7d9a9c1e7a34c3e6ef0a6c3a1a835234323228e8")

    depends_on("arpack-ng")
    depends_on("cmake")
    depends_on("gmp")
    depends_on("glpk+gmp@4.57:")
    depends_on("libxml2")
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-texttable@1.6.2:", type=("build", "run"))

    def setup_build_environment(self, env):
        args = """
-DUSE_CCACHE=OFF -DBUILD_SHARED_LIBS=OFF
-DIGRAPH_ENABLE_LTO=AUTO -DIGRAPH_GLPK_SUPPORT=ON
-DIGRAPH_GRAPHML_SUPPORT=ON -DIGRAPH_USE_INTERNAL_ARPACK=OFF
-DIGRAPH_USE_INTERNAL_BLAS=ON -DIGRAPH_USE_INTERNAL_LAPACK=ON
-DIGRAPH_USE_INTERNAL_GLPK=OFF -DIGRAPH_USE_INTERNAL_GMP=OFF
-DIGRAPH_USE_INTERNAL_PLFIT=ON
"""
        env.set("IGRAPH_CMAKE_EXTRA_ARGS", args)