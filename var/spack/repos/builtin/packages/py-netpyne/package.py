# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetpyne(PythonPackage):
    """Netpyne: A python package to facilitate the development,
    parallel simulation, optimization and analysis of multiscale
    biological neuronal networks in NEURON."""

    homepage = "http://www.netpyne.org/"
    url = "https://github.com/suny-downstate-medical-center/netpyne/archive/refs/tags/v1.0.3.1.tar.gz"
    git = "https://github.com/suny-downstate-medical-center/netpyne.git"

    license("MIT")

    version(
        "1.0.3.1",
        sha256="898b08da4c100512a7c26e7f6b29dcdf90b2d4f4eae1934819d37803cad15774",
        url="https://pypi.org/packages/42/65/e13d4d2f7d7f700a9375c9d9a91f8754e1443c8039e22edc0ea20a435f24/netpyne-1.0.3.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-bokeh", when="@0.9.8:")
        depends_on("py-future")
        depends_on("py-lfpykit", when="@1.0.2:")
        depends_on("py-matplotlib@:3.5.1", when="@1.0.3:1.0.4.1")
        depends_on("py-matplotlib-scalebar")
        depends_on("py-numpy")
        depends_on("py-pandas", when="@0.9.8:")
        depends_on("py-schema", when="@1.0.1:")
        depends_on("py-scipy")
