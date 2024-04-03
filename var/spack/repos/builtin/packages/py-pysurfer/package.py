# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysurfer(PythonPackage):
    """Cortical neuroimaging visualization in Python."""

    homepage = "https://github.com/nipy/PySurfer"
    pypi = "pysurfer/pysurfer-0.11.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.11.0",
        sha256="44cb286f015d18911094645b23180b0216193daa41911bc7e08675539a91b816",
        url="https://pypi.org/packages/66/01/231b0f66bc88b5ea232f3bf339807d3ef19a75a8fda59d1618c14168d7f0/pysurfer-0.11.0-py3-none-any.whl",
    )

    variant("save_movie", default=False, description="Enable save_movie support")

    with default_args(type="run"):
        depends_on("py-matplotlib", when="@0.10:0.11.0,0.11.2:")
        depends_on("py-mayavi", when="@0.10:0.11.0,0.11.2:")
        depends_on("py-nibabel@1.2:", when="@0.10:0.11.0,0.11.2:")
        depends_on("py-numpy", when="@0.10:0.11.0,0.11.2:")
        depends_on("py-scipy", when="@0.10:0.11.0,0.11.2:")
