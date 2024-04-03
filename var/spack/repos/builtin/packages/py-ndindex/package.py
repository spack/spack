# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNdindex(PythonPackage):
    """A Python library for manipulating indices of ndarrays."""

    homepage = "https://quansight-labs.github.io/ndindex/"
    pypi = "ndindex/ndindex-1.7.tar.gz"

    license("MIT")

    version(
        "1.7",
        sha256="4c0555d352ac9947b0f022562aea9f5d57fa06743ea069669138f75a88b42884",
        url="https://pypi.org/packages/7e/6e/bc00eed30c09815d815fce51f4f921c603b188ad6c3c9887662eabea4c64/ndindex-1.7-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.5:1.7")
