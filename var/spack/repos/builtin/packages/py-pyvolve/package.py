# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyvolve(PythonPackage):
    """Pyvolve is an open-source Python module for simulating sequences
    along a phylogenetic tree according to continuous-time Markov models
    of sequence evolution"""

    homepage = "https://github.com/sjspielman/pyvolve"
    pypi = "Pyvolve/Pyvolve-1.1.0.tar.gz"

    version(
        "1.1.0",
        sha256="c09c90824f93b3985ee738a513f5137bef13660b13678e9f3c3dc7e0eeeccb51",
        url="https://pypi.org/packages/7e/7c/c7952e984f4a5b58b11f17550bd53ef3a7426381db5c66b518a50e1d0bc8/Pyvolve-1.1.0-py3-none-any.whl",
    )
    version(
        "1.0.3",
        sha256="613f589a6c9a11ff3446d0b447494321e992004e0039b87fe4049ac94e1ef59e",
        url="https://pypi.org/packages/21/d9/2a665b85ccf0a7bdfcf76f77fea7a69d5aef3206dd3426e6d458ba40ff5e/Pyvolve-1.0.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-biopython", when="@0.9.2:")
        depends_on("py-numpy@1.20.0:", when="@1.1:")
        depends_on("py-numpy@1.7:", when="@0.9.2:1.0")
        depends_on("py-scipy", when="@0.9.2:")
