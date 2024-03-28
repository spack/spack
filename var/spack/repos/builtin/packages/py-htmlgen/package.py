# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHtmlgen(PythonPackage):
    """Library to generate HTML from classes."""

    homepage = "https://github.com/srittau/python-htmlgen"
    url = "https://github.com/srittau/python-htmlgen/archive/v1.2.2.tar.gz"

    license("MIT")

    version(
        "1.2.2",
        sha256="c375f7b18914fec8b8c25927d35d19cd0a42f1a193009272713d814731b53c73",
        url="https://pypi.org/packages/bd/b6/a7a7d009485af769b3464423785a8a2690a9458fe703bd98a7c8c0fbff04/htmlgen-1.2.2-py3-none-any.whl",
    )
