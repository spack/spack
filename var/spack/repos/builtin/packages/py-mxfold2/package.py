# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMxfold2(PythonPackage):
    """MXfold2: RNA secondary structure prediction using deep
    learning with thermodynamic integration"""

    homepage = "https://github.com/keio-bioinformatics/mxfold2"
    url = "https://github.com/keio-bioinformatics/mxfold2/releases/download/v0.1.1/mxfold2-0.1.1.tar.gz"

    maintainers("dorton21")

    license("MIT")

    version(
        "0.1.1",
        sha256="8343dce235b16e782485cd269f41a08a185339f60f07f1912aa4cf145194cfc7",
        url="https://pypi.org/packages/44/a7/df1df576b2d706ceebb600d84703279d5b25d28ee5ec98861cf84c437207/mxfold2-0.1.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3")
        depends_on("py-numpy@1.18.0:1")
        depends_on("py-torch@1.4:1")
        depends_on("py-torchvision")
        depends_on("py-tqdm@4.40:")
        depends_on("py-wheel@0.35.1:0.35")
