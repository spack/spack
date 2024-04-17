# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCondaInject(PythonPackage):
    """Helper functions for injecting a conda environment into the current python environment."""

    pypi = "conda_inject/conda_inject-1.3.1.tar.gz"

    license("MIT")

    version(
        "1.3.1",
        sha256="0a106bb0ef3553e82b6e7ef343162305c44dad7789c1909eed1abe83548c7fc6",
        url="https://pypi.org/packages/bd/4e/97d9e1758c6d505ca61daf2a24d736b14b52d8538d161d539046690802fc/conda_inject-1.3.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.9:3")
        depends_on("py-pyyaml@6.0:")
