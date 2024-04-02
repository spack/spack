# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPykml(PythonPackage):
    """pyKML is a Python package for parsing and authoring KML documents.
    It is based on the lxml.objectify API which provides Pythonic access to
    XML documents.
    """

    pypi = "pykml/pykml-0.1.3.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.2.0",
        sha256="bd4e259527a88c3b3d0d264c133b8b05bfc457efca37467f7f891b6be937d60e",
        url="https://pypi.org/packages/b8/22/8b3e7aec303a3d11bc62de04d863cf2092d7a722ade35809f7f6232df164/pykml-0.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-lxml@3.3.6:", when="@0.2:")
