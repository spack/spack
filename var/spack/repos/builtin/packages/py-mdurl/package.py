# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMdurl(PythonPackage):
    """Markdown URL utilities."""

    homepage = "https://github.com/executablebooks/mdurl"
    pypi = "mdurl/mdurl-0.1.2.tar.gz"

    license("MIT")

    version(
        "0.1.2",
        sha256="84008a41e51615a49fc9966191ff91509e3c40b939176e643fd50a5c2196b8f8",
        url="https://pypi.org/packages/b3/38/89ba8ad64ae25be8de66a6d463314cf1eb366222074cfda9ee839c56a4b4/mdurl-0.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.1.1:")
