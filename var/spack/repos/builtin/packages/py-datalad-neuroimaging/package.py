# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladNeuroimaging(PythonPackage):
    """DataLad extension package for neuro/medical imaging"""

    homepage = "https://github.com/datalad/datalad-neuroimaging"
    pypi = "datalad_neuroimaging/datalad_neuroimaging-0.3.1.tar.gz"

    license("MIT")

    version(
        "0.3.3",
        sha256="484b6ed3911129fcb9d692af6acbd29de6c3010848eb4dc4b2de7fed9bb0d501",
        url="https://pypi.org/packages/07/c4/4d6591e0b72dbd744ebe76c743ead79a500637a6d0778c199624951489c5/datalad_neuroimaging-0.3.3-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="7d33f7e9c0d6450bbf7a9fc0521ca036ba1801970e48efff088d1096c6a9cc02",
        url="https://pypi.org/packages/bb/9d/b50c4972202c9386da65467e71b7152668447fe19db7acaa80ec959b0a5a/datalad_neuroimaging-0.3.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.3.2:0.3.4")
        depends_on("py-datalad@0.16.7:", when="@0.3.2:")
        depends_on("py-datalad@0.12.0:", when="@0.3.1")
        depends_on("py-datalad-deprecated@0.2.7:", when="@0.3.3:")
        depends_on("py-datalad-metalad@0.4.5:", when="@0.3.2:")
        depends_on("py-nibabel", when="@:0.1.3,0.1.5:0.1,0.2.1,0.3.1:")
        depends_on("py-pandas", when="@:0.1.3,0.1.5:0.1,0.2.1,0.3.1:")
        depends_on("py-pybids@0.15.1:", when="@0.3.2:")
        depends_on("py-pybids@0.9.2:", when="@0.3.1")
        depends_on("py-pydicom", when="@:0.1.3,0.1.5:0.1,0.2.1,0.3.1:")
