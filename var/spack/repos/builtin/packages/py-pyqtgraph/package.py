# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqtgraph(PythonPackage):
    """PyQtGraph is a pure-python graphics and GUI library intended for use in mathematics,
    scientific, and engineering applications"""

    homepage = "http://www.pyqtgraph.org/"
    pypi = "pyqtgraph/pyqtgraph-0.13.3.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version(
        "0.13.3",
        sha256="fdcc04ac4b32a7bedf1bf3cf74cbb93ab3ba5687791712bbfa8d0712377d2f2b",
        url="https://pypi.org/packages/61/57/0a096b8949d0ee5ca32de180f19240ddd5a81015a27c6f2e7342b9044d45/pyqtgraph-0.13.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.13:0.13.3")
        depends_on("py-numpy@1.20.0:", when="@0.13:0.13.3")

    # This dependency listed in README.md ...
