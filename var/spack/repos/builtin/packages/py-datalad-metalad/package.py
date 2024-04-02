# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladMetalad(PythonPackage):
    """DataLad extension for semantic metadata handling"""

    homepage = "https://github.com/datalad/datalad-metalad/"
    pypi = "datalad_metalad/datalad_metalad-0.2.1.tar.gz"

    license("MIT")

    version(
        "0.4.17",
        sha256="7b361fb5ce419ba4599f5492a7435bebc306aec85d113ae2e4a3a7babe5a96d0",
        url="https://pypi.org/packages/08/5b/1606571a8a0a1760904872d51c627e7364c71d18a75890542408e385e590/datalad_metalad-0.4.17-py3-none-any.whl",
    )
    version(
        "0.4.5",
        sha256="c6a4fec45a3fe33dc59710f61ef5b8d2bee0e5fa601aff6ae810a706776c398e",
        url="https://pypi.org/packages/e4/a2/5a4622e6afd3df47e2590fe75a934ced626cf3240fc4d464b21489f60174/datalad_metalad-0.4.5-py3-none-any.whl",
    )
    version(
        "0.2.1",
        sha256="40b072d8fdf97ca6d820e2e4c836b762df1de340f637180ee1fdd8338f2a57c3",
        url="https://pypi.org/packages/8b/ba/2d7a77a57e6048b2d98acfd40241ca7ff376be20430c764de468784acb9a/datalad_metalad-0.2.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.4.9:")
        depends_on("py-datalad@0.18:", when="@0.4.11:")
        depends_on("py-datalad@0.15.6:", when="@0.3:0.4.5")
        depends_on("py-datalad@0.12.3:", when="@0.2.1:0.2")
        depends_on("py-datalad-deprecated", when="@0.4.17:")
        depends_on("py-datalad-metadata-model@0.3.10:", when="@0.4.12:")
        depends_on("py-datalad-metadata-model@0.3.5:", when="@0.4.5:0.4.9")
        depends_on("py-pytest", when="@0.4.11:")
        depends_on("py-pyyaml", when="@0.3:")
        depends_on("py-six", when="@0.3.1:0.4.17")
