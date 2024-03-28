# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMake(PythonPackage):
    """Create project layout from jinja2 templates"""

    homepage = "https://github.com/fholmer/make"
    git = "https://github.com/fholmer/make.git"

    version(
        "0.1.6.post2",
        sha256="307991f0d24668b7785a9abade301ba6c2d004460e90c59baf19b47c16b8ed39",
        url="https://pypi.org/packages/71/8b/af4b541d2a6e1ea2021dc95f5fd75fc5679462e5b06b155eed65b25cc2eb/make-0.1.6.post2-py3-none-any.whl",
    )
    version(
        "0.1.6",
        sha256="b4dcd40dcb2cdd7de24dd9c32c57aff8ba7eb758400145376cdb07b4957a525d",
        url="https://pypi.org/packages/1b/c3/c956ba456c4397714a6dbc0bb3acc180399e736390bc5d1491b70920ef58/make-0.1.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jinja2")
        depends_on("py-jinja2-time", when="@0.1.3:")
