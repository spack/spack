# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLangcodes(PythonPackage):
    """Tools for labeling human languages with IETF language tags"""

    homepage = "https://github.com/rspeer/langcodes"
    pypi = "langcodes/langcodes-3.3.0.tar.gz"

    license("MIT")

    version(
        "3.3.0",
        sha256="4d89fc9acb6e9c8fdef70bcdf376113a3db09b67285d9e1d534de6d8818e7e69",
        url="https://pypi.org/packages/fe/c3/0d04d248624a181e57c2870127dfa8d371973561caf54333c85e8f9133a2/langcodes-3.3.0-py3-none-any.whl",
    )
