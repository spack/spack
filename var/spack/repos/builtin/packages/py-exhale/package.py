# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExhale(PythonPackage):
    """Automatic C++ library api documentation generation: breathe doxygen in
    and exhale it out."""

    homepage = "https://github.com/svenevs/exhale"
    pypi = "exhale/exhale-0.3.6.tar.gz"

    maintainers("svenevs")

    license("BSD-3-Clause")

    version(
        "0.3.6",
        sha256="d9fee839d34014c4a953d2f6c7df8f6c2f3ef74dc255363bb63d1d6dd13444a6",
        url="https://pypi.org/packages/fc/09/125aa09435419df3044e55d5d7976fbc29fb9529c0cc2138f1057c9b7452/exhale-0.3.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.3.2:0.3.6")
        depends_on("py-beautifulsoup4", when="@0.2.4:")
        depends_on("py-breathe@4.32:", when="@0.3:0.3.6")
        depends_on("py-docutils@0.12:", when="@0.3:0.3.6")
        depends_on("py-lxml")
        depends_on("py-six")
        depends_on("py-sphinx@3.0.0:4", when="@0.3:0.3.6")
