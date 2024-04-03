# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebcolors(PythonPackage):
    """Working with color names and values formats defined by HTML and CSS."""

    homepage = "https://pypi.org/project/webcolors/"
    pypi = "webcolors/webcolors-1.11.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.11.1",
        sha256="b8cd5d865a25c51ff1218f0c90d0c0781fc64312a49b746b320cf50de1648f6e",
        url="https://pypi.org/packages/12/05/3350559de9714b202e443a9e6312937341bd5f79f4e4f625744295e7dd17/webcolors-1.11.1-py3-none-any.whl",
    )
