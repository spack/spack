# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyPycairo(PythonPackage):
    """Pycairo is a set of Python bindings for the cairo graphics library."""

    homepage = "https://www.cairographics.org/pycairo/"
    pypi = "pycairo/pycairo-1.17.1.tar.gz"
    git = "https://github.com/pygobject/pycairo.git"

    version("1.24.0", sha256="1444d52f1bb4cc79a4a0c0fe2ccec4bd78ff885ab01ebe1c0f637d8392bcafb6")
    version("1.20.0", sha256="5695a10cb7f9ae0d01f665b56602a845b0a8cb17e2123bfece10c2e58552468c")
    version("1.18.1", sha256="70172e58b6bad7572a3518c26729b074acdde15e6fee6cbab6d3528ad552b786")
    version("1.17.1", sha256="0f0a35ec923d87bc495f6753b1e540fd046d95db56a35250c44089fbce03b698")

    depends_on("python@3.8:", when="@1.23:", type=("build", "run"))
    depends_on("python@3.6:3", when="@1.20:1.22", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:3.7", when="@1.18.1:1.19", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    # https://github.com/pygobject/pycairo/blob/main/docs/getting_started.rst
    depends_on("pkgconfig", type="build")
    # version requirements from setup.py
    depends_on("cairo@1.15.10: +pdf", when="@1.20:")
    depends_on("cairo@1.13.1: +pdf", when="@:1.18.1")

    @run_after("install")
    def post_install(self):
        src = self.prefix.lib + "/pkgconfig/py3cairo.pc"
        dst = self.prefix.lib + "/pkgconfig/pycairo.pc"
        if os.path.exists(src) and not os.path.exists(dst):
            copy(src, dst)
