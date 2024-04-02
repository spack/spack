# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDalib(PythonPackage):
    """Trans-Learn is a Transfer Learning library based on pure PyTorch with high
    performance and friendly API."""

    homepage = "https://github.com/thuml/Domain-Adaptation-Lib"
    pypi = "dalib/dalib-0.2.tar.gz"

    maintainers("meyersbs")

    version(
        "0.2",
        sha256="b4e97b20c065316b2404fd7d9da316c3c0b1ce971a6e2f7ab86dc683d8d58c66",
        url="https://pypi.org/packages/8d/eb/f1728a4f4e50e939ae506acbfdc3d794ea6487e0ab35e3a6672d3946bad7/dalib-0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy")
        depends_on("py-qpsolvers@1.4:", when="@0.2:")
        depends_on("py-torch@1.4:")
        depends_on("py-torchvision@0.5:")
