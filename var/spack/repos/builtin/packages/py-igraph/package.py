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

    variant("matplotlib", default=False, description="Enable plotting with Matplotlib")

    depends_on("cmake", type="build")
    depends_on("igraph+shared@0.10.6", when="@0.10.6")
    depends_on("pkgconfig", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-texttable@1.6.2:", type=("build", "run"))
    depends_on("py-matplotlib@3.5", type="run", when="+matplotlib")

    def setup_build_environment(self, env):
        env.set("IGRAPH_USE_PKG_CONFIG", "1")
