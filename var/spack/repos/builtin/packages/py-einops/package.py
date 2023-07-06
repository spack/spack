# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEinops(PythonPackage):
    """Flexible and powerful tensor operations for readable and reliable code.

    Supports numpy, pytorch, tensorflow, and others."""

    homepage = "https://github.com/arogozhnikov/einops"
    pypi = "einops/einops-0.3.2.tar.gz"

    version("0.6.1", sha256="f95f8d00f4ded90dbc4b19b6f98b177332614b0357dde66997f3ae5d474dc8c8")
    version("0.6.0", sha256="6f6c78739316a2e3ccbce8052310497e69da092935e4173f2e76ec4e3a336a35")
    version("0.5.0", sha256="8b7a83cffc1ea88e306df099b7cbb9c3ba5003bd84d05ae44be5655864abb8d3")
    version("0.3.2", sha256="5200e413539f0377f4177ef00dc019968f4177c49b1db3e836c7883df2a5fe2e")

    depends_on("py-hatchling@1.10:", when="@0.5:", type="build")
    depends_on("py-setuptools", when="@:0.4", type="build")
