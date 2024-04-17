# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprojectMetadata(PythonPackage):
    """PEP 621 metadata parsing."""

    homepage = "https://github.com/FFY00/python-pyproject-metadata"
    pypi = "pyproject-metadata/pyproject-metadata-0.6.1.tar.gz"

    license("MIT")

    version(
        "0.7.1",
        sha256="28691fbb36266a819ec56c9fa1ecaf36f879d6944dfde5411e87fc4ff793aa60",
        url="https://pypi.org/packages/c4/cb/4678dfd70cd2f2d8969e571cdc1bb1e9293c698f8d1cf428fadcf48d6e9f/pyproject_metadata-0.7.1-py3-none-any.whl",
    )
    version(
        "0.6.1",
        sha256="36577274efd87df1bedb6fb335620cf7f4959d5457ef39881a7710c5b8c356a9",
        url="https://pypi.org/packages/87/d4/beeb6ecb90df146a0d8e23599133d4298a0ae9a1ab1547146216965b2551/pyproject_metadata-0.6.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.5:")
        depends_on("py-packaging@19:", when="@0.5:0.6,0.7.1:")
