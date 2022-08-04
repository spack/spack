# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMeson(PythonPackage):
    """A high performance build system.

    Meson is a cross-platform build system designed to be both as fast and as user
    friendly as possible. It supports many languages and compilers, including GCC,
    Clang, PGI, Intel, and Visual Studio. Its build definitions are written in a simple
    non-Turing complete DSL.
    """

    homepage = "https://mesonbuild.com/"
    pypi = "meson/meson-0.62.2.tar.gz"

    version("0.62.2", sha256="a7669e4c4110b06b743d57cc5d6432591a6677ef2402139fe4f3d42ac13380b0")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
