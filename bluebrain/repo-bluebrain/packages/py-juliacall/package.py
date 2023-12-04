# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJuliacall(PythonPackage):
    """Python and Julia in harmony."""

    homepage = "https://github.com/JuliaPy/PythonCall.jl"
    pypi = "juliacall/juliacall-0.9.15.tar.gz"

    maintainers("tristan0x")

    version("0.9.15", sha256="08163ae1290dda155cdabdccc4035a4cf0c8e361522a5b3f8e6532401b4f29cc")

    depends_on("py-wheel", type="build")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-juliapkg@0.1.8:,:0.2", type=["build", "run"])
