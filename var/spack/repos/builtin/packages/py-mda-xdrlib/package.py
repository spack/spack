# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMdaXdrlib(PythonPackage):
    """A stand-alone XDRLIB module extracted from CPython 3.10.8"""

    homepage = "https://github.com/MDAnalysis/mda-xdrlib"
    pypi = "mda_xdrlib/mda_xdrlib-0.2.0.tar.gz"

    maintainers("RMeli")

    license("0BSD")

    version(
        "0.2.0",
        sha256="0d1757b339f5db2d017a89ddaae06a82cd7a2cce26b8063df9f52b64e933fb47",
        url="https://pypi.org/packages/4f/4b/5fe3a00833a9f9775b3c237624a6212798167278ffe10fe0de04f58612d0/mda_xdrlib-0.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@:0.0.0,0.2:")
