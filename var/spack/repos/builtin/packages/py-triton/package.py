# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTriton(PythonPackage):
    """A language and compiler for custom Deep Learning operations."""

    homepage = "https://github.com/openai/triton"
    url = "https://github.com/openai/triton/archive/refs/tags/v2.1.0.tar.gz"

    license("MIT")

    version("2.1.0", sha256="4338ca0e80a059aec2671f02bfc9320119b051f378449cf5f56a1273597a3d99")

    depends_on("py-setuptools@40.8:", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("py-filelock", type=("build", "run"))

    build_directory = "python"
