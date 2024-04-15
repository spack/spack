# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymatreader(PythonPackage):
    """Convenient reader for Matlab mat files."""

    homepage = "https://gitlab.com/obob/pymatreader"
    pypi = "pymatreader/pymatreader-0.0.30.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.0.30",
        sha256="d5719dd9b4d018c7ec59c69ed1320d15eb5957eb071e8d01d9b4f6468779cc25",
        url="https://pypi.org/packages/11/b1/9d2db885e5bfbd6b552090f4d0fb80d05f9c555f9b6f4e37135d164304a7/pymatreader-0.0.30-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-future", when="@0.0.27:0.0.30")
        depends_on("py-h5py", when="@0.0.27:")
        depends_on("py-numpy", when="@0.0.27:")
        depends_on("py-scipy@:1.7.0-rc2,1.7.1:", when="@0.0.27:")
        depends_on("py-xmltodict", when="@0.0.27:")
