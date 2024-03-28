# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpherical(PythonPackage):
    """Evaluate and transform D matrices, 3-j symbols, and (scalar or
    spin-weighted) spherical harmonics"""

    homepage = "https://github.com/moble/spherical"
    pypi = "spherical/spherical-1.0.10.tar.gz"

    maintainers("nilsvu", "moble")

    license("MIT")

    version(
        "1.0.10",
        sha256="8e58ea85ef6c0f00770ce2d4ad886b9d00eea34f289a7fd75b351c9bc03cf202",
        url="https://pypi.org/packages/a8/bc/2e9fae0b2e5f0f91225a53a270ca8ef62ca33506ae7a4d0b41fc70c08d8a/spherical-1.0.10-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3.11", when="@1.0.12:1.0.13")
        depends_on("python@:3.10", when="@1.0.11")
        depends_on("python@:3.9", when="@1.0.6:1.0.10")
        depends_on("py-black@20.8-beta1:", when="@:1.0.10")
        depends_on("py-numba@0.50.0:", when="@:1.0.10,1.0.12:1.0.13")
        depends_on("py-numpy@1.13.0:1", when="@:1.0.10,1.0.12:1.0.13")
        depends_on("py-quaternionic@1:", when="@1.0.10:1.0.13")
        depends_on("py-spinsfast@104.2020:", when="@1.0.6: platform=linux")
        depends_on("py-spinsfast@104.2020:", when="@1.0.6: platform=freebsd")
        depends_on("py-spinsfast@104.2020:", when="@1.0.6: platform=darwin")
        depends_on("py-spinsfast@104.2020:", when="@1.0.6: platform=cray")
